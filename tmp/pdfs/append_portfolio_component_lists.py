from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tmp" / "pdfs" / "portfolio_college_original.pdf"
SUPPLEMENT = ROOT / "tmp" / "pdfs" / "portfolio_component_supplement.pdf"
OUTPUT = ROOT / "output" / "pdf" / "02_Junior_Automation_Controls_Portfolio_Projects_COLLEGE_EDITION.pdf"

NAVY = colors.HexColor("#193B5B")
BLUE = colors.HexColor("#2B679B")
PALE_BLUE = colors.HexColor("#E9F1F8")
PALE_ALT = colors.HexColor("#F5F8FB")
GRID = colors.HexColor("#AFC7DC")
TEXT = colors.HexColor("#263746")
MUTED = colors.HexColor("#5E6D7B")
AMBER = colors.HexColor("#D6901B")
PALE_AMBER = colors.HexColor("#FFF4DC")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="DocTitle",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=23,
    leading=27,
    textColor=NAVY,
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="H2Blue",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=15.5,
    leading=18,
    textColor=BLUE,
    spaceBefore=6,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="H3Blue",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=13,
    textColor=BLUE,
    spaceBefore=3,
    spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="BodySmall",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.6,
    leading=11.2,
    textColor=TEXT,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.4,
    leading=12.4,
    textColor=TEXT,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Tiny",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=7.2,
    leading=9.0,
    textColor=TEXT,
))
styles.add(ParagraphStyle(
    name="TinyBold",
    parent=styles["Tiny"],
    fontName="Helvetica-Bold",
))
styles.add(ParagraphStyle(
    name="CalloutLabel",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=8.8,
    leading=11,
    textColor=BLUE,
    spaceAfter=4,
))


def P(text, style="BodySmall"):
    return Paragraph(text, styles[style])


def bullets(items, style="BodySmall"):
    return [P(f"[ ] {item}", style) for item in items]


def box(label, text, amber=False):
    bg = PALE_AMBER if amber else PALE_BLUE
    edge = AMBER if amber else BLUE
    contents = [P(label.upper(), "CalloutLabel"), P(text, "Body")]
    t = Table([[contents]], colWidths=[176 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.7, edge),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def data_table(headers, rows, widths, font_size=7.3, leading=8.7):
    header = [Paragraph(f"<b>{h}</b>", ParagraphStyle(
        name=f"Hdr{h}", parent=styles["TinyBold"], textColor=WHITE,
        fontSize=font_size, leading=leading,
    )) for h in headers]
    body_style = ParagraphStyle(
        name=f"TableBody{len(rows)}{font_size}", parent=styles["Tiny"],
        fontSize=font_size, leading=leading,
    )
    data = [header] + [[Paragraph(str(cell), body_style) for cell in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for idx in range(1, len(data)):
        commands.append(("BACKGROUND", (0, idx), (-1, idx), WHITE if idx % 2 else PALE_ALT))
    t.setStyle(TableStyle(commands))
    return t


def header_footer(canvas, doc):
    page_number = 17 + doc.page
    w, h = A4
    canvas.saveState()
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.6)
    canvas.line(18 * mm, h - 15.5 * mm, w - 18 * mm, h - 15.5 * mm)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(NAVY)
    canvas.drawString(18 * mm, h - 11.5 * mm, "COLLEGE EDITION PORTFOLIO")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(w - 18 * mm, h - 11.5 * mm, "JUNIOR AUTOMATION & CONTROLS TECHNICIAN")
    canvas.line(18 * mm, 16.5 * mm, w - 18 * mm, 16.5 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(18 * mm, 11.5 * mm, "Emmanual Januarie - Development Programme")
    canvas.drawRightString(w - 18 * mm, 11.5 * mm, f"Page {page_number}")
    canvas.restoreState()


def section_title(title, subtitle=None):
    items = [P(title, "DocTitle")]
    if subtitle:
        items.append(P(subtitle, "Body"))
    return items


def build_supplement():
    SUPPLEMENT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(SUPPLEMENT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=22 * mm, bottomMargin=21 * mm,
        title="Portfolio Hardware Integration and Reuse Supplement",
        author="Emmanual Januarie",
        subject="Component lists for Junior Automation and Controls portfolio projects",
    )
    story = []

    # Page 18
    story += section_title(
        "Hardware procurement and reuse strategy",
        "A staged, 24 VDC-first component plan for Projects 1-4. Buy the shared bench once, then add only the process hardware required by each project.",
    )
    story.append(box(
        "Safety boundary",
        "The required portfolio can be completed with extra-low-voltage 24 VDC equipment. Do not expose mains terminals, energize a three-phase motor/VFD, build a safety-rated circuit, or pressurize a process unless a competent person has designed, installed and supervised that work. A mushroom pushbutton connected only to a standard PLC is a training input - it is not a validated emergency-stop safety function.",
        amber=True,
    ))
    story.append(Spacer(1, 7))
    story.append(P("System architecture", "H2Blue"))
    arch_rows = [
        ("Power", "Certified external 24 VDC supply or professionally enclosed DIN-rail supply; individually fused branches."),
        ("Control", "Siemens S7-1200 DC/DC/DC PLC; add a compatible analog module for 4-20 mA work."),
        ("Field layer", "Standardize on 24 VDC, 3-wire PNP sensors where practical; document every pinout."),
        ("Actuation", "Use interposing relays or correctly rated low-voltage drivers; add suppression across DC coils."),
        ("Supervision", "Laptop with TIA Portal/PLCSIM and Ignition; a physical HMI is optional."),
        ("Evidence", "Labelled terminal plan, I/O list, schematics, photos, test sheets, fault log and backups."),
    ]
    story.append(data_table(["Layer", "Baseline decision"], arch_rows, [35 * mm, 141 * mm], 8.0, 10.0))
    story.append(P("Buying rules", "H2Blue"))
    story.extend(bullets([
        "Confirm the exact PLC article number, generation and supported TIA Portal version before paying.",
        "Check voltage, output type, load current, inrush current, sensor wiring and common/reference arrangement.",
        "Choose spare I/O and terminal capacity; do not size the system to the final channel.",
        "Buy one representative device first, bench-test it, then duplicate only after the interface is proven.",
        "Record supplier, article number, datasheet revision, warranty and measured commissioning result.",
    ]))
    story.append(box(
        "Recommended controller baseline",
        "Example: SIMATIC S7-1200 CPU 1212C DC/DC/DC, 6ES7212-1AE40-0XB0 (8 digital inputs, 6 transistor outputs and 2 onboard 0-10 V analog inputs), plus SM 1231 AI, 6ES7231-4HD32-0XB0 for four voltage/current inputs including 4-20 mA. Treat these as a coherent example, not an instruction to mix generations or incompatible modules.",
    ))
    story.append(PageBreak())

    # Page 19
    story += section_title("Master reusable component list - control bench", "Required quantities are the practical minimum for one learner bench. Alternatives are acceptable when they meet the stated interface and safety requirements.")
    core_a = [
        ("PLC CPU", "1", "24 VDC Siemens S7-1200 DC/DC/DC; Ethernet; at least 8 DI, 6 DO, 2 AI", "P1-P4", "Buy first; verify TIA compatibility"),
        ("Analog input", "1", "4-channel differential voltage/current; supports 0/4-20 mA", "P2-P4", "Required for real transmitters"),
        ("24 VDC supply", "1", "Certified, regulated, current-limited; target at least 4 A after load calculation", "P1-P4", "External enclosed adapter is safest for solo work"),
        ("DC protection", "1 set", "Branch fuses or electronic protection; disconnect; labelled distribution", "P1-P4", "Protect PLC, field and actuator branches separately"),
        ("Ethernet switch", "1", "Unmanaged 5-port, 24 VDC industrial or reputable bench unit", "P1-P4", "PLC, laptop, SCADA and future device"),
        ("DIN rail / base", "1", "Stable, ventilated baseboard or enclosure; wire duct optional", "P1-P4", "No exposed mains terminals"),
        ("Terminal blocks", "30+", "Feed-through, fused, disconnect/test and protective-earth types as needed", "P1-P4", "Add 20% spare positions"),
        ("Interposing relays", "4", "24 VDC coil, contacts rated for the actual load; LED/test lever useful", "P1-P4", "Use suppression; never exceed contact rating"),
        ("Pushbuttons", "4", "22 mm momentary: Start, Stop, Reset and acknowledge/jog", "P1-P4", "At least one NC Stop contact"),
        ("Selector switches", "2", "Maintained 2/3-position: Auto/Manual and Local/Remote", "P1-P4", "Label positions clearly"),
        ("Pilot lights", "4", "24 VDC red, amber, green and blue/white", "P1-P4", "Power, run, warning and fault"),
        ("E-stop device", "1", "Dual-channel mushroom device for training/interface demonstration", "P1-P4", "Not safety-rated when wired only to standard PLC"),
    ]
    story.append(data_table(["Component", "Qty", "Minimum specification", "Reuse", "Procurement note"], core_a, [29*mm, 12*mm, 71*mm, 18*mm, 46*mm], 6.9, 8.2))
    story.append(Spacer(1, 6))
    story.append(box(
        "Power-supply example",
        "A reputable DIN-rail example is Mean Well HDR-100-24N (24 V, 4.2 A), but its mains input must be enclosed and installed by a competent person. Recalculate capacity from measured loads; the model name is not a substitute for a power budget.",
        amber=True,
    ))
    story.append(PageBreak())

    # Page 20
    story += section_title("Master reusable component list - field, tools and evidence")
    core_b = [
        ("Photoelectric sensors", "2", "24 VDC PNP, light/dark selectable if possible", "P1, P4", "Object detection and injected faults"),
        ("Inductive sensor", "1", "24 VDC PNP, normally open, suitable target distance", "P1, P4", "Metal target/proximity demonstration"),
        ("Limit switch", "2", "Mechanical roller/plunger, one changeover contact", "P1, P2, P4", "Position and overtravel scenarios"),
        ("Analog simulator", "1", "0-10 V potentiometer module or protected 10 kOhm potentiometer", "P1-P4", "Commission logic before a transmitter"),
        ("4-20 mA source", "1", "Loop simulator/source with clear source/sink modes", "P2-P4", "Prefer fused/protected terminals"),
        ("Digital multimeter", "1", "DC V, resistance, continuity and DC mA with fused current input", "P1-P4", "Know lead position before every current test"),
        ("Wiring kit", "1 set", "0.5-0.75 mm2 control wire, ferrules, jumpers, cable markers, glands", "P1-P4", "Colour-code consistently"),
        ("Hand tools", "1 set", "Ferrule crimper, stripper, cutters and insulated screwdrivers", "P1-P4", "Use correct ferrule/crimp size"),
        ("Patch/test leads", "1 set", "Shrouded leads and labelled low-voltage patch leads", "P1-P4", "Avoid improvised exposed conductors"),
        ("Spare devices", "1 set", "One relay, fuse set, sensor and terminal jumpers", "P4", "Supports substitution troubleshooting"),
        ("Laptop", "1", "Ethernet/USB, TIA Portal/PLCSIM-compatible; able to run Ignition", "P1-P4", "Back up software and licences"),
        ("Evidence storage", "1", "Versioned local folder plus second backup location", "P1-P4", "Source, PDFs, photos, test results and exports"),
    ]
    story.append(data_table(["Component", "Qty", "Minimum specification", "Reuse", "Use note"], core_b, [31*mm, 12*mm, 70*mm, 20*mm, 43*mm], 6.9, 8.2))
    story.append(P("Optional purchases - only after a demonstrated need", "H2Blue"))
    optional_rows = [
        ("Physical HMI", "Optional; Ignition Perspective on the laptop can provide the required interface and evidence."),
        ("Real VFD + three-phase motor", "Not required. Use simulated ready/run/speed/fault I/O unless supervised by a competent person."),
        ("Safety relay", "Only if completing a separately designed and validated safety circuit under competent supervision."),
        ("24 VDC UPS/buffer", "Useful for Project 4 power-event testing, but simulated power-quality evidence is acceptable."),
        ("HART communicator/modem", "Not required; document HART awareness and use 4-20 mA bench calibration evidence."),
    ]
    story.append(data_table(["Item", "Decision"], optional_rows, [48*mm, 128*mm], 7.5, 9.4))
    story.append(PageBreak())

    # Page 21
    story += section_title("Project 1 component deployment", "Industrial Motor & Conveyor Control Panel | Build window: 5 October-15 November 2026")
    p1 = [
        ("Core bench", "PLC, PSU, DC protection, switch, terminals, relays, buttons, selectors, lamps, training E-stop", "Shared", "Build and label the permanent control station"),
        ("Geared DC motor", "1 x 24 VDC, low-current geared motor with guarded coupling", "P1, P4", "Choose speed/torque for a small trainer"),
        ("Motor interface", "1 x rated DC motor driver or relay/contactor interface with suppression", "P1, P4", "PLC output must not drive motor directly"),
        ("Conveyor mock-up", "1 small belt/roller rig or guarded rotating target", "P1", "A stationary sensor target board is acceptable"),
        ("Photoelectric sensors", "2 x 24 VDC PNP", "P1, P4", "Entry and exit/object tracking"),
        ("Inductive sensor", "1 x 24 VDC PNP", "P1, P4", "Speed/proximity or metal-part test"),
        ("Limit switch", "1 x changeover", "P1, P4", "Guard/position permissive simulation"),
        ("VFD interface simulator", "Potentiometer, switches and lamps representing ready/run/fault/speed reference", "P1, P4", "Required baseline instead of a live VFD"),
        ("Loads", "2-4 x 24 VDC lamps or small protected loads", "P1-P4", "Prove output mapping before actuators"),
    ]
    story.append(data_table(["Group", "Quantity / specification", "Reuse", "Project role"], p1, [37*mm, 74*mm, 23*mm, 42*mm], 7.2, 8.8))
    story.append(P("Commissioning sequence", "H2Blue"))
    story.extend(bullets([
        "Cold checks: verify terminal numbers, polarity, continuity, fuses, relay suppression and protective separation.",
        "Power PLC only; prove input LEDs and force no outputs. Then test pilot-light loads before connecting the motor.",
        "Prove Start/Stop, controlled restart, Auto/Manual, Local/Remote, jam timer and fault reset.",
        "Inject stuck sensor, missing object, motor feedback loss, VFD-fault simulation and power-cycle recovery.",
        "Capture as-built schematic, I/O list, normal/fault/recovery results and a short narrated demonstration.",
    ]))
    story.append(box(
        "Do not buy by default",
        "A real VFD and three-phase motor add cost and electrical risk without being necessary to prove PLC sequencing, interfaces or troubleshooting. The simulated VFD interface is the required portfolio baseline.",
        amber=True,
    ))
    story.append(PageBreak())

    # Page 22
    story += section_title("Project 2 component deployment", "Automated Tank, Pump & Instrumentation Skid | Build window: 16 November-27 December 2026")
    p2 = [
        ("Core bench", "PLC, analog module, PSU, protection, relays, terminals, selectors and lamps", "Shared", "Reuse the Project 1 control bench"),
        ("Reservoirs", "2 x clear, stable, low-volume plastic tanks with lids", "P2, P4", "Source and process/return tank"),
        ("Pumps", "2 x low-voltage 24 VDC pumps", "P2, P4", "Duty/standby or fill/transfer service"),
        ("Pump interfaces", "2 x rated relay/driver channels with suppression", "P2, P4", "Separate motor current from PLC outputs"),
        ("Tubing/fittings", "1 set: tubing, clamps, tees, manual valves and check valves", "P2, P4", "Match material and size; use drip tray"),
        ("Level switches", "2 x low-voltage float switches", "P2, P4", "Low-low and high-high independent protection"),
        ("Level transmitter", "1 x 4-20 mA, water-compatible, suitable range", "P2-P4", "May begin with signal simulator"),
        ("Pressure transmitter", "1 x 4-20 mA, low-pressure, water-compatible", "P2-P4", "Range must suit pump shutoff pressure"),
        ("Flow device", "1 x pulse or 4-20 mA low-flow water sensor", "P2-P4", "Document K-factor/range and scaling"),
        ("Control valve", "1 x 24 VDC solenoid or low-voltage motorized valve", "P2, P4", "Use rated driver and flyback suppression"),
        ("Containment", "Drip tray, absorbent material and cable elevation", "P2, P4", "Keep water below and away from electronics"),
    ]
    story.append(data_table(["Group", "Quantity / specification", "Reuse", "Project role"], p2, [34*mm, 77*mm, 23*mm, 42*mm], 6.9, 8.3))
    story.append(P("Commissioning and safe-process checks", "H2Blue"))
    story.extend(bullets([
        "Perform a dry I/O simulation first; then leak-test unpowered with electronics physically separated.",
        "Confirm transmitter loop wiring and scaling at 4, 12 and 20 mA before connecting wet instrumentation.",
        "Prove low-low trip, high-high trip, duty/standby changeover, valve fail state and restart permissives.",
        "Record pump current, fill/empty time and sensor repeatability; never exceed a device's pressure rating.",
    ]))
    story.append(box(
        "Cost-control option",
        "Buy one real 4-20 mA transmitter first and use the loop simulator for the other process variables. Add a second transmitter only after the first loop is correctly wired, scaled and calibrated.",
    ))
    story.append(PageBreak())

    # Page 23
    story += section_title("Project 3 component deployment", "SCADA/HMI, Historian & Industrial Communications | Build window: 28 December 2026-24 January 2027")
    p3 = [
        ("Core process rig", "PLC and selected Project 2 sensors/actuators", "Shared", "Provides live tags and credible process behaviour"),
        ("Laptop/PC", "1 x Ethernet-capable machine running Ignition and engineering tools", "P1-P4", "Use a dedicated project backup folder"),
        ("Ethernet switch", "1 x 5-port 24 VDC switch", "P1-P4", "Separate training LAN preferred"),
        ("Patch cables", "4 x tested Cat5e/Cat6 cables", "P1-P4", "Label both ends and keep one spare"),
        ("RS-485 adapter", "1 x isolated USB-to-RS-485 adapter", "P3, P4", "Isolation preferred for troubleshooting"),
        ("Modbus RTU device", "1 x documented 24 VDC remote I/O or sensor", "P3, P4", "Choose public register map and configurable address"),
        ("Termination/bias kit", "120 ohm termination plus documented biasing as required", "P3, P4", "Install only at correct bus locations"),
        ("Optional second Ethernet device", "Modbus TCP remote I/O, gateway or another controller", "P3, P4", "Not required if a simulator is used"),
        ("Database", "Local supported SQL database or Ignition historian configuration", "P3, P4", "Software item; back up schema/config"),
    ]
    story.append(data_table(["Group", "Quantity / specification", "Reuse", "Project role"], p3, [37*mm, 74*mm, 23*mm, 42*mm], 7.1, 8.7))
    story.append(P("Network evidence to produce", "H2Blue"))
    story.extend(bullets([
        "Address plan with device name, IP, subnet, protocol, port, node ID and ownership.",
        "Ignition device connection, tags, quality states, alarm priorities, trends and historical retrieval.",
        "Modbus RTU frame settings: baud, parity, stop bits, address, register, data type and byte/word order.",
        "Fault tests: unplugged cable, duplicate/wrong IP, stopped PLC, wrong serial settings, stale data and recovery.",
        "Packet capture or diagnostic screenshots with timestamps and a plain-language root-cause explanation.",
    ]))
    story.append(box(
        "Software choice",
        "Ignition Maker Edition is appropriate for this personal, non-commercial learning portfolio and includes Perspective, OPC UA, historian and supported device drivers. A physical HMI is optional; the laptop can host the required interface.",
    ))
    story.append(PageBreak())

    # Page 24
    story += section_title("Project 4 component deployment", "Offshore / Remote Process Package Troubleshooting & Commissioning Simulation | Build window: 25 January-28 February 2027")
    p4 = [
        ("Complete bench", "Reuse PLC, process rig, networking, indicators and software", "P1-P3", "Project 4 is a commissioning exercise, not a new shopping cycle"),
        ("Fault-injection box", "1 x labelled switch/patch box with protected open/short/substitution points", "P4", "Use only on extra-low-voltage circuits"),
        ("Disconnect terminals", "4-8 x knife/disconnect or test terminal positions", "P4", "Create repeatable, documented field faults"),
        ("Spare sensor", "1 x compatible PNP proximity/photoelectric sensor", "P4", "Substitution and proof-of-repair"),
        ("Spare relay", "1 x matching 24 VDC relay and base", "P4", "Coil/contact fault isolation"),
        ("Spare fuses", "Correct type/rating for every protected branch", "P1-P4", "Never uprate a fuse to clear a symptom"),
        ("Portable backup", "1 x USB drive or equivalent second storage location", "P4", "PLC, HMI, database, drawings and test pack"),
        ("Calibration aids", "Reuse DMM and 4-20 mA simulator; add leads/adapters if needed", "P2-P4", "Record as-found/as-left values"),
        ("Optional DC buffer", "24 VDC UPS/buffer sized for PLC/network load", "P4", "Optional brownout/ride-through demonstration"),
    ]
    story.append(data_table(["Group", "Quantity / specification", "Origin", "Project role"], p4, [36*mm, 75*mm, 23*mm, 42*mm], 7.1, 8.7))
    story.append(P("Minimum fault library", "H2Blue"))
    faults = [
        ("Electrical", "Blown branch fuse, loose/open input, failed relay coil, missing 24 V common."),
        ("Instrumentation", "4 mA underrange, 20 mA overrange, reversed loop polarity, incorrect scaling."),
        ("Control", "Permissive missing, stale latch, bad mode ownership, restart not inhibited."),
        ("Network", "Wrong IP/subnet, wrong Modbus node/baud/parity, unplugged cable, stale SCADA data."),
        ("Process", "Low-low level, no-flow with pump command, valve fail-to-open, duty pump unavailable."),
    ]
    story.append(data_table(["Layer", "Faults to inject and diagnose"], faults, [35*mm, 141*mm], 7.8, 9.7))
    story.append(Spacer(1, 6))
    story.append(box(
        "Procurement gate",
        "Do not buy new Project 4 hardware until the fault matrix identifies a capability that the reused bench cannot safely simulate. The quality of evidence, diagnosis and restoration matters more than hardware volume.",
        amber=True,
    ))
    story.append(PageBreak())

    # Page 25
    story += section_title("Reuse matrix and staged buying plan", "A filled cell shows the expected use of an item. P4 intentionally reuses nearly the whole bench.")
    matrix = [
        ("PLC + analog module", "X", "X", "X", "X"),
        ("24 VDC power/protection/terminals", "X", "X", "X", "X"),
        ("Buttons/selectors/lamps/relays", "X", "X", "X", "X"),
        ("Photoelectric/inductive/limit sensors", "X", "-", "-", "X"),
        ("24 VDC geared motor/interface", "X", "-", "-", "X"),
        ("0-10 V and 4-20 mA simulators", "X", "X", "X", "X"),
        ("Tanks/pumps/tubing/valve", "-", "X", "X", "X"),
        ("Process transmitters/flow device", "-", "X", "X", "X"),
        ("Ethernet switch/cables", "X", "X", "X", "X"),
        ("RS-485 adapter + Modbus device", "-", "-", "X", "X"),
        ("Laptop: TIA + Ignition", "X", "X", "X", "X"),
        ("Fault box, spares and test terminals", "-", "-", "-", "X"),
    ]
    story.append(data_table(["Component group", "P1", "P2", "P3", "P4"], matrix, [104*mm, 18*mm, 18*mm, 18*mm, 18*mm], 7.6, 9.2))
    story.append(P("Staged acquisition gates", "H2Blue"))
    stages = [
        ("Before 5 Oct 2026", "Core control bench + Project 1 sensors/motor", "PLC powers up; every DI/DO proven with safe test loads; software connects; drawings match wiring."),
        ("Before 16 Nov 2026", "Project 2 wet-process hardware", "Dry simulation passes; one 4-20 mA loop correctly wired/scaled; leak test plan and containment ready."),
        ("Before 28 Dec 2026", "Project 3 serial/network additions", "Stable PLC Ethernet link; address plan complete; selected Modbus device has an official register map."),
        ("Before 25 Jan 2027", "Project 4 fault-injection/spares only", "Fault matrix reviewed; buy only missing capability; all injected faults remain at safe extra-low voltage."),
    ]
    story.append(data_table(["Purchase point", "Buy / release", "Gate before further spending"], stages, [39*mm, 55*mm, 82*mm], 7.3, 9.0))
    story.append(Spacer(1, 6))
    story.append(box(
        "Budget priority",
        "Spend first on a compatible PLC/analog path, sound power distribution, safe wiring, measurement tools and documented sensors. Mechanical polish and optional vendor hardware come only after the control system is reliable and evidenced.",
    ))
    story.append(PageBreak())

    # Page 26
    story += section_title("Compatibility, receiving and official references", "Use this page before ordering and again when each item arrives.")
    story.append(P("Pre-order compatibility checklist", "H2Blue"))
    compat = [
        ("PLC ecosystem", "Exact CPU/module generation, TIA Portal support, expansion compatibility, firmware, memory card/licence needs."),
        ("Digital I/O", "PNP/NPN convention, sourcing/sinking, output type, per-channel/group current, common terminals and inrush."),
        ("Analog I/O", "0-10 V versus 4-20 mA, active/passive loop, two-/three-/four-wire transmitter, isolation and input impedance."),
        ("Power", "Input supply, 24 V tolerance, steady/inrush load, branch fuse ratings, conductor size, earth and enclosure."),
        ("Networking", "Ethernet/serial interface, connector, IP support, Modbus register map, termination, baud/parity and isolation."),
        ("Mechanical/process", "Port/thread size, tubing material, wetted materials, pressure/temperature range, mounting and leak containment."),
    ]
    story.append(data_table(["Check", "What must match"], compat, [38*mm, 138*mm], 7.6, 9.4))
    story.append(P("Receiving inspection", "H2Blue"))
    story.extend(bullets([
        "Photograph label and condition; record supplier, exact article number, serial/firmware and datasheet revision.",
        "Check for counterfeit warning signs, damage, missing plugs/bases and mismatch between listing and product label.",
        "Do resistance/continuity and polarity checks unpowered; energize one protected branch at a time.",
        "Run a simple acceptance test, record measured values, and update the component register and spare list.",
    ]))
    story.append(P("Official procurement references - verified 12 September 2026", "H2Blue"))
    refs = [
        ("Siemens CPU 1212C", "https://mall.industry.siemens.com/mall/en/gb/Catalog/Product/6ES72121AE400XB0"),
        ("Siemens SM 1231 AI", "https://mall.industry.siemens.com/goos/catalog/Pages/mmpdata.ashx?MLFB1=6ES7231-4HD32-0XB0&lang=en"),
        ("Mean Well HDR-100 series", "https://www.meanwell.com/Upload/PDF/HDR-100/HDR-100-SPEC.PDF"),
        ("Ignition Maker Edition", "https://inductiveautomation.com/ignition/maker-edition"),
        ("Ignition Maker manual", "https://docs.inductiveautomation.com/docs/8.3/other-editions/ignition-maker-edition"),
    ]
    story.append(data_table(["Reference", "Official URL"], refs, [45*mm, 131*mm], 7.0, 8.6))
    story.append(Spacer(1, 6))
    story.append(box(
        "Final purchasing caution",
        "Availability, regional article numbers, licences and product generations can change. Re-open the official datasheet and confirm the exact seller listing immediately before purchase. Prefer authorized distributors and keep invoices and datasheets with the portfolio evidence pack.",
        amber=True,
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def merge_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    source_reader = PdfReader(str(SOURCE))
    supplement_reader = PdfReader(str(SUPPLEMENT))
    writer = PdfWriter()
    for page in source_reader.pages:
        writer.add_page(page)
    for page in supplement_reader.pages:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Junior Automation & Controls Technician Portfolio Projects - College Edition",
        "/Author": "Emmanual Januarie",
        "/Subject": "Portfolio roadmap with reusable hardware component lists for Projects 1-4",
        "/Keywords": "automation, controls, PLC, instrumentation, portfolio, component list, procurement",
    })
    with OUTPUT.open("wb") as handle:
        writer.write(handle)


if __name__ == "__main__":
    build_supplement()
    merge_pdf()
    print(OUTPUT)
