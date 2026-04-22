import json
import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

from src.models import Invoice

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = (
    "Tu es un expert-comptable spécialisé dans les factures françaises. "
    "Analyse le texte de la facture fourni et extrais les informations suivantes. "
    "Réponds UNIQUEMENT avec un objet JSON valide, sans texte supplémentaire.\n\n"
    "Champs à extraire :\n"
    "- company_name : nom de la société émettrice de la facture (string)\n"
    "- invoice_number : numéro de facture (string)\n"
    "- invoice_date : date de la facture au format DD/MM/YYYY (string)\n"
    "- due_date : date d'échéance de paiement au format DD/MM/YYYY (string, \"\" si absente)\n"
    "- tax_5_5 : montant de la TVA à 5,5% en euros (number, 0 si absente)\n"
    "- tax_10 : montant de la TVA à 10% en euros (number, 0 si absente)\n"
    "- tax_20 : montant de la TVA à 20% en euros (number, 0 si absente)\n"
    "- total_amount : montant total TTC en euros (number)\n\n"
    "Si un champ est introuvable, utilise \"\" pour les strings et 0 pour les numbers."
)


def extract_invoice_data(text: str, source_file: str) -> Invoice:
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(
        model_name=MODEL,
        generation_config={"response_mime_type": "application/json"},
    )

    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTexte de la facture :\n\n{text}")
    data: dict = json.loads(response.text)

    return Invoice(
        source_file=source_file,
        company_name=str(data.get("company_name", "")),
        invoice_number=str(data.get("invoice_number", "")),
        invoice_date=str(data.get("invoice_date", "")),
        due_date=str(data.get("due_date", "")),
        tax_5_5=float(data.get("tax_5_5", 0) or 0),
        tax_10=float(data.get("tax_10", 0) or 0),
        tax_20=float(data.get("tax_20", 0) or 0),
        total_amount=float(data.get("total_amount", 0) or 0),
    )
