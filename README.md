# InvoiceMind

Outil de bureau Windows qui scanne automatiquement les factures PDF du dossier courant, extrait les champs clés via l'IA, et génère un rapport Excel structuré — en un double-clic.

Conçu pour les services comptables français, avec prise en charge des trois taux de TVA (5,5 % / 10 % / 20 %).

---

## Fonctionnement

```
InvoiceMind.exe
  ├── Scan du dossier courant → collecte tous les *.pdf
  ├── Extraction du texte brut (pdfplumber)
  ├── Analyse et structuration des champs (Gemini 2.0 Flash)
  └── Génération du rapport Excel (openpyxl)
```

---

## Stack technique

| Rôle | Outil |
|---|---|
| Extraction texte PDF | `pdfplumber` |
| Analyse IA des factures | Google Gemini API (`google-generativeai`) |
| Modèle IA | `gemini-2.0-flash` |
| Génération Excel | `openpyxl` |
| Packaging Windows | `PyInstaller` |

**Langage** : Python 3.11+  
**Plateforme cible** : Windows 10/11 (exécutable `.exe` autonome)

---

## Format du rapport Excel

Nom du fichier généré : `invoices_YYYYMMDD_HHMMSS.xlsx`

| Colonne | Champ |
|---|---|
| A | Société |
| B | N° Facture |
| C | Date Facture |
| D | Date Échéance |
| E | TVA 5.5% |
| F | TVA 10% |
| G | TVA 20% |
| H | Total TTC |

- En-tête en gras, fond bleu (`#4472C4`), texte blanc
- Colonnes montants formatées en `€`
- Dernière ligne : totaux calculés automatiquement (formule SUM)

---

## Structure du projet

```
invoicemind/
├── main.py                  # Point d'entrée
├── requirements.txt
└── src/
    ├── models.py            # Dataclass Invoice
    ├── pdf_reader.py        # Extraction texte via pdfplumber
    ├── extractor.py         # Appel Gemini API, retour JSON structuré
    └── excel_writer.py      # Génération du fichier Excel
```

---

## Installation & développement

```bash
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine du projet :

```
GEMINI_API_KEY=votre_clé_api
```

Lancer en mode développement :

```bash
python main.py
```

---

## Packaging Windows

```bash
pyinstaller --onefile --name InvoiceMind main.py
```

Génère `dist/InvoiceMind.exe` — fichier unique, aucune dépendance externe requise.

**Utilisation** : placer `InvoiceMind.exe` dans le dossier contenant les PDF, double-cliquer, le rapport Excel est créé automatiquement.
