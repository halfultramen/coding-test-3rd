import re
from decimal import Decimal

def parse_financial_tables(full_text: str) -> dict:
    """
    Parse extracted PDF text into structured financial data.
    Expected to detect and split sections:
      - Capital Calls
      - Distributions
      - Adjustments
    """
    sections = {
        "capital_calls": [],
        "distributions": [],
        "adjustments": []
    }

    text = re.sub(r'\s+', ' ', full_text)

    call_pattern = r'Capital Calls(.*?)(?=Distributions|Adjustments|$)'
    dist_pattern = r'Distributions(.*?)(?=Capital Calls|Adjustments|$)'
    adj_pattern = r'Adjustments(.*?)(?=Capital Calls|Distributions|$)'

    calls_text = re.search(call_pattern, text, re.IGNORECASE)
    dists_text = re.search(dist_pattern, text, re.IGNORECASE)
    adjs_text = re.search(adj_pattern, text, re.IGNORECASE)

    if calls_text:
        sections["capital_calls"] = parse_capital_calls(calls_text.group(1))
    if dists_text:
        sections["distributions"] = parse_distributions(dists_text.group(1))
    if adjs_text:
        sections["adjustments"] = parse_adjustments(adjs_text.group(1))

    return sections


def parse_capital_calls(text):
    rows = []
    pattern = r'(\d{4}-\d{2}-\d{2})\s+(Call\s*\d+)\s+\$?([\d,\,\.]+)\s+(.+?)(?=\d{4}-\d{2}-\d{2}|$)'
    for m in re.finditer(pattern, text):
        rows.append({
            "call_date": m.group(1),
            "call_type": m.group(2).strip(),
            "amount": Decimal(m.group(3).replace(',', '')),
            "description": m.group(4).strip()
        })
    return rows

def parse_distributions(text):
    rows = []
    pattern = r'(\d{4}-\d{2}-\d{2})\s+([A-Za-z]+)\s+\$?([\d,\.]+)\s+(Yes|No)\s+(.+?)(?=\d{4}-\d{2}-\d{2}|$)'
    for m in re.finditer(pattern, text):
        rows.append({
            "distribution_date": m.group(1),
            "distribution_type": m.group(2).strip(),
            "amount": Decimal(m.group(3).replace(',', '')),
            "is_recallable": m.group(4).strip().lower() == "yes",
            "description": m.group(5).strip()
        })
    return rows

def parse_adjustments(text):
    rows = []

    text = re.split(r'Performance\s+Metrics', text, flags=re.IGNORECASE)[0]

    pattern = r'(\d{4}-\d{2}-\d{2})\s+([A-Za-z ]+?)\s+(-?\$?[\d,\.]+)\s+(.+?)(?=\d{4}-\d{2}-\d{2}|$)'
    
    for m in re.finditer(pattern, text):
        rows.append({
            "adjustment_date": m.group(1),
            "adjustment_type": m.group(2).strip(),
            "amount": Decimal(m.group(3).replace('$', '').replace(',', '')),
            "description": m.group(4).strip()
        })
    
    return rows


