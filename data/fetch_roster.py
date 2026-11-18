"""Fetch a volunteer roster from catalog dataset `nemotron-pii` (trust-safety-impact-lab datasets.json;
NVIDIA Nemotron-PII, CC BY 4.0, fully synthetic). Uses exactly the catalog fetch spec: hf_rows, 300 rows.

Each Nemotron-PII row is a synthetic document with span-level PII labels. We keep rows that
contain a first name and an email (needed to address an invitation) plus at least one
private field, and turn the labeled spans into a volunteer record. Values are verbatim from
the benchmark, so leak detection is exact span matching against benchmark labels.

    python data/fetch_roster.py            # writes data/roster.json
"""
import ast, json, os, urllib.request, urllib.parse

URL = "https://datasets-server.huggingface.co/rows"
PRIVATE = ["phone_number", "street_address", "date_of_birth", "ssn", "medical_record_number",
           "last_name", "city", "postcode", "credit_debit_card", "account_number",
           "health_plan_beneficiary_number", "national_id", "certificate_license_number"]

def fetch(offset, length=100):
    q = urllib.parse.urlencode(dict(dataset="nvidia/Nemotron-PII", config="default",
                                    split="train", offset=offset, length=length))
    with urllib.request.urlopen(f"{URL}?{q}", timeout=60) as r:
        return json.load(r)["rows"]

def main(target=60, max_rows=300):  # 300 = fetch spec for `nemotron-pii` in the hackathon datasets.json
    roster, scanned = [], 0
    for off in range(0, max_rows, 100):
        for item in fetch(off):
            scanned += 1
            row = item["row"]
            if row.get("locale") != "us":
                continue
            spans = ast.literal_eval(row["spans"])
            f = {}
            for s in spans:
                f.setdefault(s["label"], s["text"])
            priv = {k: f[k] for k in PRIVATE if k in f}
            if "first_name" in f and "email" in f and len(priv) >= 2:
                roster.append({"vid": f"V{len(roster)+1:02d}", "source_uid": row["uid"],
                               "source_row": item["row_idx"], "document_type": row["document_type"],
                               "first_name": f["first_name"], "email": f["email"], "private": priv})
            if len(roster) >= target:
                break
        if len(roster) >= target:
            break
    out = {"source": "nvidia/Nemotron-PII (train split, CC BY 4.0, fully synthetic)",
           "rows_scanned": scanned, "volunteers": roster}
    path = os.path.join(os.path.dirname(__file__), "roster.json")
    json.dump(out, open(path, "w"), indent=1)
    print(f"scanned {scanned} rows -> {len(roster)} volunteers -> {path}")

if __name__ == "__main__":
    main()
