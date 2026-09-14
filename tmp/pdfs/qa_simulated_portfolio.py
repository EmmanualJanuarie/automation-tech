from pathlib import Path
import re
import pdfplumber

pdf_path = Path(r"C:\Users\emman\Documents\GitHub\automation-tech\output\pdf\02_Junior_Automation_Controls_Portfolio_Projects_COLLEGE_EDITION.pdf")
with pdfplumber.open(pdf_path) as pdf:
    pages = [(page.extract_text() or "").strip() for page in pdf.pages]

text = "\n".join(pages)
checks = {
    "page_count": len(pages),
    "blank_pages": [i + 1 for i, value in enumerate(pages) if not value],
    "replacement_characters": text.count("\ufffd"),
    "project_heading_numbers": sorted(set(re.findall(r"Project ([1-9])", text, re.I))),
    "project_1_title": bool(re.search(r"Project 1\s*-\s*Industrial Motor\s*&\s*Conveyor\s+Control Simulation", text, re.I)),
    "project_2_title": bool(re.search(r"Project 2\s*-\s*Automated Process\s*&\s*Instrumentation Simulation", text, re.I)),
    "project_3_title": bool(re.search(r"Project 3\s*-\s*SCADA, Historian\s*&\s*Communications Simulation", text, re.I)),
    "project_4_title": bool(re.search(r"Project 4\s*-\s*Integrated Remote/Offshore\s+Process Package Simulation", text, re.I)),
    "software_simulation": "software simulation" in text.lower(),
    "ignition": "Ignition" in text,
    "s7_plcsim": "S7-PLCSIM" in text,
    "factory_io": "Factory I/O" in text,
    "opc_ua": "OPC UA" in text,
    "modbus": "Modbus" in text,
    "wireshark": "Wireshark" in text,
    "rubric": "rubric" in text.lower(),
    "challenge": "challenge" in text.lower(),
    "no_project_5": "PROJECT 5" not in text,
    "no_hobby_terms": not re.search(r"\b(hobby|breadboard|battery)\b", text, re.I),
    "no_diy_term": not re.search(r"\bDIY\b", text, re.I),
}
for key, value in checks.items():
    print(f"{key}: {value}")

for i, value in enumerate(pages, 1):
    print(f"page_{i:02d}_chars: {len(value)}")
