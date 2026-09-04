from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
from pypdf import PdfReader, PdfWriter


ROOT = Path(r"C:\Users\emman\Documents\GitHub\automation-tech")
SOURCE = ROOT / "tmp" / "pdfs" / "syllabus-source.pdf"
NEW_PAGES = ROOT / "tmp" / "pdfs" / "documentation-pages.pdf"
OUTPUT = ROOT / "output" / "pdf" / "Emmanual-Januarie-Automation-Controls-Syllabus.pdf"

PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#091A29")
NAVY_2 = colors.HexColor("#102E42")
TEAL = colors.HexColor("#159E9A")
BLUE = colors.HexColor("#276E99")
AMBER = colors.HexColor("#D58B25")
INK = colors.HexColor("#14232D")
SLATE = colors.HexColor("#4C6170")
MUTED = colors.HexColor("#758793")
PALE = colors.HexColor("#EAF3F6")
PALE_BLUE = colors.HexColor("#E7F0F6")
PALE_AMBER = colors.HexColor("#FFF3DD")
GRID = colors.HexColor("#D4E0E6")
WHITE = colors.white

ss = getSampleStyleSheet()
ss.add(ParagraphStyle(name="CoverKicker", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=TEAL, alignment=TA_CENTER))
ss.add(ParagraphStyle(name="CoverTitle", fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=WHITE, alignment=TA_CENTER))
ss.add(ParagraphStyle(name="CoverSub", fontName="Helvetica", fontSize=10.2, leading=15, textColor=colors.HexColor("#CAD8E0"), alignment=TA_CENTER))
ss.add(ParagraphStyle(name="Kicker", fontName="Helvetica-Bold", fontSize=7.2, leading=9, textColor=TEAL))
ss.add(ParagraphStyle(name="H1", fontName="Helvetica-Bold", fontSize=18, leading=21, textColor=INK, spaceAfter=3))
ss.add(ParagraphStyle(name="H2", fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=INK, spaceBefore=3, spaceAfter=2))
ss.add(ParagraphStyle(name="H3", fontName="Helvetica-Bold", fontSize=7.4, leading=8.8, textColor=BLUE))
ss.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=7.6, leading=10.0, textColor=INK, spaceAfter=3))
ss.add(ParagraphStyle(name="Small", fontName="Helvetica", fontSize=6.6, leading=8.0, textColor=INK))
ss.add(ParagraphStyle(name="Tiny", fontName="Helvetica", fontSize=5.7, leading=6.8, textColor=INK))
ss.add(ParagraphStyle(name="Label", fontName="Helvetica-Bold", fontSize=6.3, leading=7.4, textColor=SLATE))
ss.add(ParagraphStyle(name="Head", fontName="Helvetica-Bold", fontSize=5.8, leading=6.7, textColor=WHITE))
ss.add(ParagraphStyle(name="Cell", fontName="Helvetica", fontSize=5.7, leading=6.8, textColor=INK))
ss.add(ParagraphStyle(name="CardTitle", fontName="Helvetica-Bold", fontSize=11.5, leading=13, textColor=WHITE))


def P(text, style="Body"):
    return Paragraph(str(text), ss[style])


def section_bar(title, amber=False):
    bg = PALE_AMBER if amber else PALE_BLUE
    accent = AMBER if amber else TEAL
    table = Table([[P(title.upper(), "H3")]], colWidths=[174*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg), ("LINEBEFORE", (0,0), (0,-1), 2, accent),
        ("BOX", (0,0), (-1,-1), 0.25, GRID), ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6), ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    return table


def callout(title, text, amber=False):
    bg = PALE_AMBER if amber else PALE_BLUE
    accent = AMBER if amber else TEAL
    table = Table([[P(f"<b>{title}</b><br/>{text}", "Small")]], colWidths=[174*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg), ("LINEBEFORE", (0,0), (0,-1), 2, accent),
        ("BOX", (0,0), (-1,-1), 0.25, GRID), ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7), ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return table


def check_grid(items, style="Small", columns=2):
    groups = [[] for _ in range(columns)]
    for i, item in enumerate(items):
        groups[i % columns].append(item)
    rows = []
    for i in range(max(len(g) for g in groups)):
        rows.append([P("[ ] " + g[i], style) if i < len(g) else "" for g in groups])
    table = Table(rows, colWidths=[174*mm/columns]*columns)
    table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 1.2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1.2),
    ]))
    return table


def compact_table(headers, rows, widths, style="Cell", pad=3):
    data = [[P(h, "Head") for h in headers]]
    data += [[P(v, style) if v != "" else "" for v in row] for row in rows]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0,0), (-1,0), NAVY_2), ("GRID", (0,0), (-1,-1), 0.3, GRID),
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), pad),
        ("RIGHTPADDING", (0,0), (-1,-1), pad), ("TOPPADDING", (0,0), (-1,-1), pad),
        ("BOTTOMPADDING", (0,0), (-1,-1), pad),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            commands.append(("BACKGROUND", (0,r), (-1,r), PALE))
    table.setStyle(TableStyle(commands))
    return table


ACTUAL_PAGE_NUMBERS = [None, 3, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]


def footer(canvas, doc):
    canvas.saveState()
    actual = ACTUAL_PAGE_NUMBERS[doc.page-1]
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.45)
    canvas.line(20*mm, PAGE_H-16*mm, PAGE_W-20*mm, PAGE_H-16*mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 5.6)
    canvas.drawString(20*mm, PAGE_H-12.7*mm, "EMMANUAL JANUARIE | PRACTICAL AUTOMATION AND CONTROLS SYLLABUS")
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.4)
    canvas.line(20*mm, 13*mm, 48*mm, 13*mm)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W-20*mm, 11.5*mm, f"PAGE {actual}")
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    canvas.setStrokeColor(colors.HexColor("#15394B"))
    canvas.setLineWidth(0.35)
    for x in range(14,201,10):
        canvas.line(x*mm,16*mm,x*mm,PAGE_H-16*mm)
    for y in range(16,287,10):
        canvas.line(14*mm,y*mm,PAGE_W-14*mm,y*mm)
    canvas.setFillColor(NAVY)
    canvas.rect(21*mm,44*mm,PAGE_W-42*mm,PAGE_H-88*mm,fill=1,stroke=0)
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.2)
    canvas.line(55*mm,61*mm,PAGE_W-55*mm,61*mm)
    canvas.line(55*mm,PAGE_H-61*mm,PAGE_W-55*mm,PAGE_H-61*mm)
    canvas.restoreState()


DOCS = {
    "P&ID": {
        "purpose": "Process and instrumentation representation.",
        "learn": ["Equipment, piping, flow direction, valves, instruments, and control loops", "Instrument tags, line references, legends, boundaries, and revision status", "Difference between process intent and physical wiring detail"],
        "activity": "Draw the Automated Tank / Filling System P&ID, then expand it for the Water Treatment Plant.",
        "exercise": "Trace the level-control loop from tank to transmitter, PLC/controller, valve, and process response.",
        "case": "A valve is shown on the HMI but missing from the P&ID. Decide which document or implementation is wrong and record the resolution.",
        "quality": ["Symbols are consistent", "Tags are unique", "Flow direction is clear", "Control loops are traceable", "Revision is shown"],
    },
    "I/O List": {
        "purpose": "Maps field devices to PLC inputs and outputs.",
        "learn": ["Tag, description, I/O type, address/channel, signal, range, units, normal state, and fail state", "DI, DO, AI, and AO classification", "Spare points, cabinet/module reference, and software-tag relationship"],
        "activity": "Create the conveyor I/O list first; extend the format for the tank and flagship projects.",
        "exercise": "Classify Start, overload, level transmitter, valve command, running feedback, and speed reference.",
        "case": "A level transmitter is wired to AI channel 3 while the list shows channel 2. Trace the mismatch and update the controlled record.",
        "quality": ["One row per point", "Address matches PLC", "Range and units match", "Normal/fail state defined", "Spares identified"],
    },
    "Instrument List": {
        "purpose": "Documents instruments, tags, ranges, and signals.",
        "learn": ["Tag, service, instrument type, location, range, units, signal, power, and fail behavior", "Technology and process-connection notes", "Cross-reference to P&ID, I/O, loop, datasheet, and calibration record"],
        "activity": "Build an instrument register for level, pressure, temperature, and flow in the tank project.",
        "exercise": "Specify a plausible tag, range, units, signal, and fault state for four instruments.",
        "case": "The replacement pressure transmitter is ranged 0-16 bar while the instrument list and PLC expect 0-10 bar. Determine every document and configuration affected.",
        "quality": ["Tags match P&ID", "Ranges match scaling", "Signals match I/O", "Service is clear", "Changes are traceable"],
    },
    "Electrical Schematic": {
        "purpose": "Represents power, protection, and control circuits.",
        "learn": ["Power source, protection, disconnects, contactors, overloads, coils, contacts, loads, and references", "Control voltage versus power voltage", "Wire numbers, terminal references, device tags, and page cross-references"],
        "activity": "Create a 24 VDC control schematic and a conceptual DOL/VFD interface schematic.",
        "exercise": "Trace the complete energizing path for the motor contactor and identify five test points.",
        "case": "The PLC output is true, but the contactor coil is off. Use the schematic to isolate fuse, stop chain, overload, interface relay, and coil possibilities.",
        "quality": ["Supply and return shown", "Protection identified", "Contacts cross-referenced", "Wire/terminal IDs present", "Safe-state intent visible"],
    },
    "Wiring Diagram": {
        "purpose": "Defines terminal, conductor, panel, and field connections.",
        "learn": ["From/to connection, terminal number, conductor ID, cable/core, shield, color, and destination", "Panel terminals, marshalling, field junctions, and I/O channels", "Shield termination and spare-core documentation awareness"],
        "activity": "Create a point-to-point wiring diagram for one sensor, one transmitter, one solenoid, and one motor feedback.",
        "exercise": "Follow a level-transmitter loop from field terminals to the PLC analog channel without skipping a connection.",
        "case": "The field cable core is landed on terminal TB2-14, but the drawing states TB2-13. Record as-found condition and correct the authorized source of truth.",
        "quality": ["Every endpoint identified", "Terminal numbers unique", "Cable/core IDs present", "Shield path shown", "I/O channel agrees"],
    },
    "Loop Diagram": {
        "purpose": "Traces an instrument loop from field to control system.",
        "learn": ["Field instrument, junction box, marshalling, barrier/isolator awareness, PLC/DCS channel, power, and return", "Terminal, cable/core, signal direction, shield, and grounding information", "Relationship between loop, I/O list, instrument list, and scaling"],
        "activity": "Draw a complete 4-20 mA level-transmitter loop for the tank project.",
        "exercise": "Mark where voltage/current checks would be taken under qualified supervision and state expected readings.",
        "case": "PLC input reads 0 mA after maintenance. Use the loop drawing to order checks from supply through every termination to the input channel.",
        "quality": ["End-to-end path complete", "Power source identified", "All terminals shown", "Signal and shield clear", "Channel and range match"],
    },
    "Control Narrative": {
        "purpose": "Defines operating sequence and control intent.",
        "learn": ["Scope, initial state, modes, start conditions, normal sequence, stop sequence, faults, reset, and recovery", "Commands, feedback, permissives, interlocks, alarms, and trips", "Clear shall-style statements and testable behavior"],
        "activity": "Write the conveyor narrative, then write the tank Auto/Manual and high-high response narrative.",
        "exercise": "Convert one paragraph into numbered, testable requirements with no ambiguous words such as normally or as needed.",
        "case": "PLC stops the pump on high-high level, but the narrative mentions only an alarm. Resolve the design inconsistency before testing.",
        "quality": ["Initial state defined", "Mode ownership clear", "Conditions testable", "Fault/reset behavior included", "Matches PLC and C&E"],
    },
    "Cause & Effect": {
        "purpose": "Maps initiating events to required system responses.",
        "learn": ["Cause rows, effect columns, action symbols, delays, latching, reset, and notes", "Alarm, trip, inhibit, close, stop, and safe-state responses", "Traceability to narrative, alarms, PLC logic, and tests"],
        "activity": "Create a matrix for E-stop, overload, high-high level, bad transmitter signal, valve failure, and network loss.",
        "exercise": "For each cause, identify immediate effects, delayed effects, alarms, reset conditions, and recovery tests.",
        "case": "The matrix says high-high level stops the inlet pump, but the PLC also closes the outlet valve. Determine whether the logic or document is incorrect.",
        "quality": ["Every cause measurable", "Effects unambiguous", "Delays recorded", "Latch/reset stated", "FAT tests reference rows"],
    },
    "Alarm List": {
        "purpose": "Records priority, setpoint, delay, message, and response.",
        "learn": ["Tag, message, condition, setpoint, units, delay, deadband, priority, latch, acknowledgement reset, and operator response", "Alarm versus event versus trip", "Acknowledgement, return-to-normal, and rationalization awareness"],
        "activity": "Create conveyor, tank, communication, and flagship alarm lists.",
        "exercise": "Write clear messages and operator actions for high level, high-high trip, overload, bad PV, start failure, and comms loss.",
        "case": "A level alarm chatters around its setpoint and floods the history. Add justified deadband or delay and test that protection is not weakened.",
        "quality": ["Message identifies problem", "Priority justified", "Setpoint/units correct", "Delay/deadband documented", "Action is useful"],
    },
    "Network Diagram": {
        "purpose": "Shows control devices, links, protocols, and addressing.",
        "learn": ["PLC, HMI, SCADA, switches, remote I/O, drives, instruments, and engineering workstation", "Media, port, link, IP address, subnet, VLAN awareness, protocol, and device role", "Boundary, ownership, firewall, and time-source awareness"],
        "activity": "Draw the SCADA Process Control System and flagship network architecture.",
        "exercise": "Add an IP schedule and verify same-subnet communication for each required connection.",
        "case": "A replacement PLC is assigned an address already used by the HMI. Show how the diagram and IP schedule help identify and prevent the conflict.",
        "quality": ["All devices named", "Links and media clear", "Addresses documented", "Protocols labeled", "Failure boundaries visible"],
    },
    "Test Procedure": {
        "purpose": "Records preconditions, steps, expectations, and evidence.",
        "learn": ["Test ID, requirement reference, preconditions, action, expected result, actual result, status, evidence, tester, and date", "Normal, abnormal, recovery, regression, and communication-loss tests", "NOT TESTED, PASS, FAIL, blocked, and retest handling"],
        "activity": "Create and execute FAT procedures for conveyor, tank, SCADA, and flagship projects.",
        "exercise": "Write one normal, one fault, one recovery, and one regression test for a pump start sequence.",
        "case": "A test is marked PASS without an actual result or screenshot. Correct the record and decide whether the test must be repeated.",
        "quality": ["Expected result objective", "Actual result recorded", "Evidence linked", "Status honest", "Failed tests retested"],
    },
    "Troubleshooting Report": {
        "purpose": "Records symptoms, investigation, cause, action, and verification.",
        "learn": ["Problem, symptoms, expected state, initial checks, evidence, isolation, root cause, correction, verification, result, and remaining risk", "Timestamped PLC, HMI, trend, network, and measurement evidence", "Difference between symptom, root cause, and contributing condition"],
        "activity": "Write at least ten reports across electrical, PLC, instrument, process, SCADA, and network faults.",
        "exercise": "Convert a vague statement such as fixed wiring into an evidence-based maintenance report.",
        "case": "Pump will not start after maintenance because Local/Remote feedback remains Local. Document the full diagnosis without blaming the operator.",
        "quality": ["Expected state stated", "Checks ordered", "Cause proven", "Action specific", "Verification repeatable"],
    },
    "Change Log": {
        "purpose": "Tracks revision, reason, author, date, and approval.",
        "learn": ["Revision, date, description, reason, affected files/tags, author, checker/approver, test reference, backup, and rollback", "Draft, review, approved, issued, and obsolete status awareness", "Consistency across PLC, HMI, drawings, lists, and reports"],
        "activity": "Maintain one project change log from the first baseline through final FAT closure.",
        "exercise": "Record a transmitter-range change and list every affected artifact and retest.",
        "case": "PLC scaling is changed from 0-16 bar to 0-10 bar, but HMI range and alarm limits are not updated. Use the change log to control the full change.",
        "quality": ["Reason is clear", "Affected items complete", "Backup recorded", "Approval/status visible", "Retest reference included"],
    },
}


def doc_card(name, height_mode="full"):
    d = DOCS[name]
    width = 174*mm
    title = Table([[P(name, "CardTitle"), P("PURPOSE", "Head"), P(d["purpose"], "Small")]], colWidths=[48*mm,20*mm,106*mm])
    title.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), NAVY_2), ("BACKGROUND", (1,0), (1,0), TEAL),
        ("BACKGROUND", (2,0), (2,0), PALE_BLUE), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("BOX", (0,0), (-1,-1), 0.3, GRID),
    ]))
    learn_text = "<br/>".join("[ ] " + item for item in d["learn"])
    quality_text = "<br/>".join("[ ] " + item for item in d["quality"])
    rows = [
        [P("LEARN TO INCLUDE", "Label"), P(learn_text, "Small")],
        [P("PRACTICAL ACTIVITY", "Label"), P(d["activity"], "Small")],
        [P("EXERCISE", "Label"), P(d["exercise"], "Small")],
        [P("CASE STUDY", "Label"), P(d["case"], "Small")],
        [P("QUALITY CHECK", "Label"), P(quality_text, "Small")],
        [P("EVIDENCE", "Label"), P("[ ] Draft  [ ] Reviewed version  [ ] Final PDF/source  [ ] Screenshot or test reference  [ ] Revision entry", "Small")],
    ]
    body = Table(rows, colWidths=[34*mm,140*mm])
    body.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.white), ("BACKGROUND", (0,3), (-1,3), PALE_AMBER),
        ("BOX", (0,0), (-1,-1), 0.35, GRID), ("INNERGRID", (0,0), (-1,-1), 0.25, GRID),
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5), ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return [title, body]


story = []

# Replacement cover
story += [
    Spacer(1,53*mm), P("7 SEPTEMBER 2026 - 31 MARCH 2027", "CoverKicker"), Spacer(1,7),
    P("PRACTICAL AUTOMATION<br/>AND CONTROLS SYLLABUS", "CoverTitle"), Spacer(1,8),
    P("15 technical modules plus an integrated Engineering Documentation Curriculum", "CoverSub"),
    Spacer(1,7), P("Activities | Exercises | Case Studies | Projects | Documentation | Testing", "CoverSub"),
    Spacer(1,20*mm), P("Emmanual Januarie", "CoverSub"), Spacer(1,5*mm),
    P("Target: Junior / Trainee Automation, Controls, PLC, Instrumentation, and SCADA roles", "CoverSub"),
    Spacer(1,20*mm), P("17 hours per week | PC-first practical work | Evidence before claims", "CoverKicker"), PageBreak(),
]

# Replacement page 3
story += [P("Program map: technical modules plus documentation", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
module_rows = [
    ["1-2", "7-20 Sep", "Electrical foundations, components, control circuits, and schematics", "Schematic and wiring foundations"],
    ["3-5", "21 Sep-1 Nov", "PLC hardware, I/O, Ladder Logic, modes, sequencing, and faults", "I/O list, narrative, C&E, tests"],
    ["6-8", "2 Nov-13 Dec", "Motors/VFDs, sensors, instrumentation, 4-20 mA, and scaling", "Instrument list, wiring, loop diagram"],
    ["9-10", "14 Dec-10 Jan", "Process control, valves, PID concepts, HMI/SCADA, alarms, and trends", "P&ID, narrative, alarm list"],
    ["11-12", "11-31 Jan", "Industrial networking, communications, SCADA integration, and history", "Network diagram and integration tests"],
    ["13-14", "1-28 Feb", "Troubleshooting, change control, and flagship integrated project", "Full document set and FAT pack"],
    ["15", "1-31 Mar", "Portfolio, interviews, evidence audit, and targeted applications", "Published documentation library"],
]
story += [compact_table(["Modules", "Dates", "Technical focus", "Documentation output"], module_rows, [18*mm,31*mm,76*mm,49*mm], "Cell", 3.2), Spacer(1,6)]
story += [callout("Integrated documentation curriculum", "Pages 55-63 teach the purpose, minimum content, creation activity, exercise, case study, evidence, and quality check for P&IDs, lists, schematics, wiring, loops, narratives, cause-and-effect, alarms, networks, tests, troubleshooting reports, and change logs."), Spacer(1,6)]
story += [section_bar("Documentation learning rule"), check_grid([
    "Create the first draft when its source content is learned", "Update it whenever the design or configuration changes",
    "Cross-check tags, ranges, addresses, alarms, and effects", "Issue a reviewed PDF plus editable source",
    "Record revision, reason, date, and author", "Use the final document during testing and troubleshooting",
], "Small"), PageBreak()]

# Page 55 - roadmap
story += [P("Engineering Documentation Curriculum", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += [P("Documentation is not separate from the technical work. Each document must be created from the project content, checked against related documents, used during testing or troubleshooting, and revised when the system changes.", "Body")]
roadmap = [
    ["P&ID", "Modules 7-9", "Tank process", "Module 14 flagship"],
    ["I/O List", "Module 3", "PLC I/O mini-project", "Every later PLC project"],
    ["Instrument List", "Module 7", "Measurement-chain study", "Tank and flagship"],
    ["Electrical Schematic", "Module 2", "24 VDC control", "Motor/VFD and flagship"],
    ["Wiring Diagram", "Modules 2-3", "Sensor/output wiring", "Analog loop and flagship"],
    ["Loop Diagram", "Module 8", "4-20 mA laboratory", "Tank and flagship"],
    ["Control Narrative", "Module 5", "Conveyor", "Tank and flagship"],
    ["Cause & Effect", "Module 5", "Conveyor faults", "Tank and flagship"],
    ["Alarm List", "Modules 9-10", "Tank/HMI", "SCADA and flagship"],
    ["Network Diagram", "Module 11", "Communications lab", "SCADA and flagship"],
    ["Test Procedure", "Module 4 onward", "Logic-pattern tests", "FAT for every project"],
    ["Troubleshooting Report", "Module 1 onward", "One fault per module", "Ten-report portfolio pack"],
    ["Change Log", "Module 4 onward", "PLC revision record", "Every project baseline"],
]
story += [compact_table(["Document", "First learn/create", "First application", "Final application"], roadmap, [39*mm,35*mm,50*mm,50*mm], "Cell", 2.8), Spacer(1,6)]
story += [callout("Friday connection", "Use every C - Documentation Friday to create or revise the document assigned to the current module. Use every D - Integration Friday to cross-check it against PLC, HMI, instruments, network configuration, and test results."), PageBreak()]

# Page 56 - document control
story += [P("Engineering document control foundation", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += [callout("Goal", "Learn to make documents that another technician can identify, understand, verify, and use. A technically correct drawing with no revision or source control can still create maintenance risk.", False), Spacer(1,5)]
story += [section_bar("Every controlled document should show"), check_grid([
    "Document title and type", "Project or system name", "Document number or filename standard", "Revision",
    "Date", "Author/drawn by", "Checked/reviewed by placeholder", "Approval/status placeholder",
    "Page or sheet number", "Legend, units, and abbreviations", "Source/editable file", "Change description",
], "Small")]
story += [Spacer(1,5), section_bar("Required activities")]
activities = [
    ["1", "Create a title-block template", "Use the same identity fields on drawings, lists, narratives, and reports."],
    ["2", "Create a numbering convention", "Example categories: PID, IO, INST, ELEC, WIR, LOOP, CN, CE, ALM, NET, TEST, TR, CL."],
    ["3", "Create a revision workflow", "Draft -> self-check -> reviewed placeholder -> issued for training -> superseded."],
    ["4", "Build a document register", "Track document number, title, project, current revision, status, date, and link."],
    ["5", "Run a consistency audit", "Choose one tag and verify it across every related document and software layer."],
]
story += [compact_table(["No.", "Activity", "Required result"], activities, [10*mm,48*mm,116*mm], "Cell", 3.2), Spacer(1,5)]
story += [section_bar("Document-control case study", True), P("A pump tag is P-101 on the P&ID, M-101 in the I/O list, and PUMP_1 in the PLC. The HMI shows Raw Water Pump. Create a tag-resolution record, select one controlled equipment tag, update affected documents, preserve software-friendly tag names, and record the revision.", "Small"), Spacer(1,5)]
story += [check_grid(["Tag resolution recorded", "Affected documents listed", "Revision reason written", "Old version retained", "Cross-check completed", "Final PDF and source saved"], "Small"), PageBreak()]

# Page 57 P&ID
story += [P("Process and instrumentation documentation", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("P&ID")
story += [Spacer(1,6), callout("Module connection", "Create the tank P&ID during Modules 7-9. Use it to derive the instrument list, I/O list, control narrative, cause-and-effect, alarm list, PLC logic, HMI process flow, and test procedure. Expand it for the Module 14 water-treatment project."), PageBreak()]

# Page 58 lists
story += [P("Equipment data and PLC mapping documents", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("I/O List")
story += [Spacer(1,7)] + doc_card("Instrument List")
story += [PageBreak()]

# Page 59 electrical and wiring
story += [P("Electrical and connection documents", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("Electrical Schematic")
story += [Spacer(1,7)] + doc_card("Wiring Diagram")
story += [PageBreak()]

# Page 60 loops and narrative
story += [P("Instrument-loop and functional documents", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("Loop Diagram")
story += [Spacer(1,7)] + doc_card("Control Narrative")
story += [PageBreak()]

# Page 61 C&E and alarms
story += [P("Protective response and alarm documents", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("Cause & Effect")
story += [Spacer(1,7)] + doc_card("Alarm List")
story += [PageBreak()]

# Page 62 network
story += [P("Industrial network documentation", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("Network Diagram")
story += [Spacer(1,6), callout("Module connection", "Create the first network diagram in Module 11, use it for the Module 12 SCADA integration tests, and expand it for the Module 14 flagship. The diagram must match the IP schedule, protocol map, PLC/HMI/SCADA configuration, and communication-failure tests."), Spacer(1,5)]
story += [section_bar("Required companion tables"), check_grid(["IP address schedule", "Device and firmware register", "Protocol and port map", "PLC/SCADA tag map", "Communication test record", "Backup and recovery location"], "Small"), PageBreak()]

# Page 63 test, report, change
story += [P("Testing, troubleshooting, and change records", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += doc_card("Test Procedure")
story += [Spacer(1,5)] + doc_card("Troubleshooting Report")
story += [Spacer(1,5)] + doc_card("Change Log")
story += [PageBreak()]

# Page 64 references and final gate
story += [P("Documentation completion gate and references", "H1"), HRFlowable(width="100%", thickness=1.1, color=TEAL, spaceAfter=5)]
story += [section_bar("Portfolio documentation library complete when"), check_grid([
    "Every required document has a controlled title block", "Tags agree across drawings, lists, PLC, and HMI",
    "Ranges, units, signals, addresses, and setpoints agree", "Narrative and cause-and-effect match implemented logic",
    "Alarm list matches HMI configuration and tests", "Network diagram matches address and protocol maps",
    "Test procedures contain expected and actual results", "Unperformed steps remain NOT TESTED",
    "Troubleshooting reports prove cause and verification", "Change log records every portfolio revision",
    "Editable source and final PDF are stored", "Every document can be explained in an interview",
], "Small"), Spacer(1,7)]
refs = [
    ["Adsyst - Graduate / Junior Control Systems Technician", "PLC, SCADA, HMI, VSD, instrumentation, design, testing, and project lifecycle", "https://careers.adsyst.co.uk/job/886184"],
    ["Amcor - Controls Technician", "Electrical/PLC/HMI faults, drawings, networks, VFDs, sensors, safety, and records", "https://amcor.wd5.myworkdayjobs.com/en-US/Amcor_External_Career_Site/job/Controls-Technician_REQ_90979"],
    ["South African public procurement examples", "Technician roles may specify electrical, instrumentation, trade, software, or OEM qualification routes", "https://www.etenders.gov.za/"],
]
story += [section_bar("Role-alignment references"), compact_table(["Reference", "Why used", "URL"], refs, [49*mm,78*mm,47*mm], "Tiny", 3.2), Spacer(1,7)]
story += [callout("Scope note", "This syllabus teaches junior-level documentation practice for personal simulation projects. It is not a formal drafting qualification, engineering approval, site authorization, trade test, or substitute for employer standards and supervised field experience.", True)]

doc = SimpleDocTemplate(str(NEW_PAGES), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=21*mm, bottomMargin=18*mm)
doc.build(story, onFirstPage=cover, onLaterPages=footer)

source = PdfReader(str(SOURCE))
new = PdfReader(str(NEW_PAGES))
if len(source.pages) != 55:
    raise ValueError(f"Expected 55 source pages, found {len(source.pages)}")
if len(new.pages) != 12:
    raise ValueError(f"Expected 12 replacement/appendix pages, found {len(new.pages)}")

writer = PdfWriter()
writer.add_page(new.pages[0])
writer.add_page(source.pages[1])
writer.add_page(new.pages[1])
for page_index in range(3, 54):
    writer.add_page(source.pages[page_index])
for page_index in range(2, 12):
    writer.add_page(new.pages[page_index])
writer.add_metadata({
    "/Title": "Practical Automation and Controls Syllabus with Engineering Documentation Curriculum",
    "/Author": "Emmanual Januarie",
})
with open(OUTPUT, "wb") as stream:
    writer.write(stream)

final = PdfReader(str(OUTPUT))
print(f"Created {OUTPUT}")
print(f"Pages: {len(final.pages)}")
