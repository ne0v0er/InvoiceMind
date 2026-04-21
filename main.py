import sys
from pathlib import Path

from src.excel_writer import write_excel
from src.extractor import extract_invoice_data
from src.models import Invoice
from src.pdf_reader import extract_text


def main() -> None:
    current_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path.cwd()

    pdf_files = sorted(current_dir.glob("*.pdf"))

    if not pdf_files:
        print("Aucun fichier PDF trouvé dans ce dossier.")
        input("\nAppuyez sur Entrée pour quitter...")
        return

    print(f"InvoiceMind — {len(pdf_files)} fichier(s) PDF trouvé(s)\n")

    invoices: list[Invoice] = []
    errors: list[str] = []

    for i, pdf_path in enumerate(pdf_files, start=1):
        print(f"[{i}/{len(pdf_files)}] {pdf_path.name} ...", end=" ", flush=True)
        try:
            text = extract_text(pdf_path)
            if not text:
                raise ValueError("PDF vide ou non lisible")
            invoice = extract_invoice_data(text, pdf_path.name)
            invoices.append(invoice)
            print("OK")
        except Exception as exc:
            print(f"ERREUR ({exc})")
            errors.append(pdf_path.name)

    if not invoices:
        print("\nAucune facture n'a pu être traitée.")
        input("\nAppuyez sur Entrée pour quitter...")
        return

    print(f"\nGénération du fichier Excel ({len(invoices)} facture(s))...")
    output_path = write_excel(invoices, current_dir)
    print(f"Fichier créé : {output_path.name}")

    if errors:
        print(f"\nFichiers ignorés ({len(errors)}) : {', '.join(errors)}")

    input("\nAppuyez sur Entrée pour quitter...")


if __name__ == "__main__":
    main()
