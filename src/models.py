from dataclasses import dataclass, field


@dataclass
class Invoice:
    source_file: str
    company_name: str = ""
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: str = ""
    tax_5_5: float = 0.0
    tax_10: float = 0.0
    tax_20: float = 0.0
    total_amount: float = 0.0
