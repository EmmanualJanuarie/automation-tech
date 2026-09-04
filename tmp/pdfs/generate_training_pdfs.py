from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#15324B")
BLUE = colors.HexColor("#187C91")
TEAL = colors.HexColor("#20A39E")
GOLD = colors.HexColor("#E9B44C")
INK = colors.HexColor("#23313D")
MUTED = colors.HexColor("#617282")
PALE = colors.HexColor("#EAF4F5")
PALE_GOLD = colors.HexColor("#FFF6DE")
LINE = colors.HexColor("#CBD9DE")
WHITE = colors.white
LIGHT = colors.HexColor("#F6F9FA")
RED = colors.HexColor("#A63D40")


def ptext(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


styles = getSampleStyleSheet()
S = {
    "cover_kicker": ParagraphStyle(
        "cover_kicker", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=TEAL, spaceAfter=7,
    ),
    "cover_title": ParagraphStyle(
        "cover_title", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=29, leading=32, textColor=NAVY, spaceAfter=12,
    ),
    "cover_sub": ParagraphStyle(
        "cover_sub", parent=styles["Normal"], fontName="Helvetica",
        fontSize=13, leading=18, textColor=MUTED, spaceAfter=10,
    ),
    "h1": ParagraphStyle(
        "h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=20, leading=24, textColor=NAVY, spaceAfter=10,
    ),
    "h2": ParagraphStyle(
        "h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=16, textColor=BLUE, spaceBefore=8, spaceAfter=5,
    ),
    "h3": ParagraphStyle(
        "h3", parent=styles["Heading3"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=NAVY, spaceBefore=5, spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "body", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9, leading=12.2, textColor=INK, spaceAfter=4,
    ),
    "small": ParagraphStyle(
        "small", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=7.5, leading=9.5, textColor=INK, spaceAfter=2,
    ),
    "tiny": ParagraphStyle(
        "tiny", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=6.7, leading=8.2, textColor=INK,
    ),
    "label": ParagraphStyle(
        "label", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=7.5, leading=9, textColor=TEAL, spaceAfter=2,
    ),
    "quote": ParagraphStyle(
        "quote", parent=styles["BodyText"], fontName="Helvetica-Oblique",
        fontSize=9, leading=13, leftIndent=8, textColor=NAVY,
    ),
    "table_head": ParagraphStyle(
        "table_head", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=7.5, leading=9, textColor=WHITE,
    ),
    "table": ParagraphStyle(
        "table", parent=styles["Normal"], fontName="Helvetica",
        fontSize=7.1, leading=9, textColor=INK,
    ),
    "table_bold": ParagraphStyle(
        "table_bold", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=7.2, leading=9, textColor=NAVY,
    ),
    "center": ParagraphStyle(
        "center", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=INK,
    ),
}


def P(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, S[style])


def bullets(items: Iterable[str], style: str = "body") -> list:
    out = []
    for item in items:
        out.append(P(f"- {ptext(item)}", style))
    return out


def checklist(items: Iterable[str], style: str = "body") -> list:
    return [P(f"[ ] {ptext(item)}", style) for item in items]


def info_box(title: str, body: str, tone: str = "blue") -> Table:
    bg = PALE if tone == "blue" else PALE_GOLD
    accent = TEAL if tone == "blue" else GOLD
    data = [[P(ptext(title).upper(), "label")], [P(body, "body")]]
    t = Table(data, colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, accent),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


class TrainingDoc(BaseDocTemplate):
    def __init__(self, path: Path, title: str, code: str):
        self.doc_title = title
        self.doc_code = code
        super().__init__(
            str(path), pagesize=A4,
            leftMargin=18 * mm, rightMargin=18 * mm,
            topMargin=18 * mm, bottomMargin=17 * mm,
            title=title, author="Emmanual Januarie",
            subject="Junior Automation and Controls Technician Development",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="main")
        self.addPageTemplates(PageTemplate(id="all", frames=frame, onPage=self._decorate))

    def _decorate(self, canvas, doc):
        page = canvas.getPageNumber()
        canvas.saveState()
        if page > 1:
            canvas.setStrokeColor(LINE)
            canvas.setLineWidth(0.5)
            canvas.line(18 * mm, 284 * mm, 192 * mm, 284 * mm)
            canvas.setFont("Helvetica-Bold", 7)
            canvas.setFillColor(NAVY)
            canvas.drawString(18 * mm, 287 * mm, self.doc_code)
            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(MUTED)
            canvas.drawRightString(192 * mm, 287 * mm, "EMMANUAL JANUARIE")
        canvas.setStrokeColor(LINE)
        canvas.line(18 * mm, 12 * mm, 192 * mm, 12 * mm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 8 * mm, "Personal training plan - simulation evidence must be labelled honestly")
        canvas.drawRightString(192 * mm, 8 * mm, f"PAGE {page}")
        canvas.restoreState()


def cover_story(title: str, subtitle: str, kicker: str, meta: list[str], accent_text: str):
    return [
        Spacer(1, 22 * mm),
        P(ptext(kicker.upper()), "cover_kicker"),
        P(ptext(title), "cover_title"),
        P(ptext(subtitle), "cover_sub"),
        Spacer(1, 8 * mm),
        info_box("Design promise", ptext(accent_text), "gold"),
        Spacer(1, 18 * mm),
        Table([[P(ptext(x), "body")] for x in meta], colWidths=[160 * mm], style=[
            ("LINEBEFORE", (0, 0), (0, -1), 2, TEAL),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]),
        Spacer(1, 28 * mm),
        P("Prepared for Emmanual Januarie", "h2"),
        P("Study period: 7 September 2026 to 31 March 2027", "body"),
        P("Workload: 17 hours per full week", "body"),
    ]


@dataclass
class Module:
    num: int
    title: str
    dates: str
    weeks: int
    objective: str
    topics: list[str]
    activities: list[str]
    exercises: list[str]
    case_title: str
    situation: str
    evidence: str
    tasks: list[str]
    deliverables: list[str]
    role_value: str


modules = [
    Module(1, "Electrical fundamentals and safe work boundaries", "7-13 Sep 2026", 1,
           "Build the electrical vocabulary, calculations, schematic-reading habits, and safety boundaries needed before PLC or field work.",
           ["Voltage, current, resistance, power, energy, AC/DC, polarity and frequency", "Series and parallel circuits; open, short, overload and earth-fault concepts", "Electrical symbols, current-path tracing, test points and multimeter functions", "Isolation, LOTO awareness, test-before-touch and authorization limits"],
           ["Build a quantities map with symbol, unit, instrument and meaning", "Draw and calculate one series and one parallel 24 VDC circuit", "Predict then simulate normal, open and short-circuit behavior", "Write a safe-measurement checklist for an unknown low-voltage circuit"],
           ["Calculate current and power for 24 VDC across 240 ohms", "Explain why voltage can be present with no current", "Mark five safe test points on a control circuit"],
           "A control-panel indicator is dark", "Supply output is 24 VDC. Voltage before the fuse is 24 VDC and after it is 0 VDC. The indicator resistance is plausible.",
           "Power-supply reading, before/after-fuse readings, component resistance", ["Draw the expected current path", "Identify the most likely failed layer", "Name the next safe confirmation test", "State correction and recovery verification"],
           ["Calculation sheet", "Annotated circuit", "Expected-vs-actual table", "One-page fault report"], "Essential foundation for every automation, PLC, SCADA and instrumentation role."),
    Module(2, "Industrial components, control circuits and schematics", "14-20 Sep 2026", 1,
           "Recognize common control-panel components and trace command, protection and feedback paths through a basic motor-control circuit.",
           ["NO/NC states, relays, contactors, auxiliary contacts and terminal blocks", "Fuses, breakers, overloads, control versus power circuit", "Two-wire and three-wire control; seal-in circuits", "Fail-safe stops, interface relays, E-stop and safety-relay awareness"],
           ["Label a DOL start/stop schematic", "Build a state table for stopped, starting, running and overload", "Convert relay behavior into PLC input/logic/output terms", "Color-code command, protection and feedback paths"],
           ["Explain why Stop is commonly NC", "Trace Start press to latched run", "List three causes of motor-will-not-start"],
           "Contactor drops out when Start is released", "The coil energizes while Start is held. Stop and overload are healthy. The holding contact never changes state.",
           "Coil state, auxiliary-contact state, stop and overload states", ["Trace the seal-in path", "List two plausible root causes", "Design one test that distinguishes them", "Record verified recovery"],
           ["Motor-control schematic", "Component list", "State table", "Troubleshooting report"], "Directly supports panel reading, motor controls and PLC I/O troubleshooting."),
    Module(3, "PLC hardware, scan cycle, addressing and I/O", "21 Sep-4 Oct 2026", 2,
           "Understand where signals enter and leave a PLC, how the scan executes, and how to trace a signal end to end.",
           ["CPU, power, local/remote I/O and communications modules", "Input scan, program solve, output update and housekeeping", "Digital and analog I/O; physical addresses, tags and internal memory", "PNP/NPN awareness, module diagnostics, monitoring, forcing risk and backups"],
           ["Draw a PLC-field-HMI architecture", "Create a 12-point I/O list and tag standard", "Trace one input and one output through every layer", "Simulate a short pulse and relate it to scan time"],
           ["Classify Start, contactor, transmitter and valve command by I/O type", "Explain the scan cycle in five sentences", "List causes for sensor-on but PLC-input-off"],
           "Sensor LED is on but the PLC input is off", "The sensor is powered and detects the object. The input module LED is off, the PLC tag is false, and other channels work.",
           "Sensor LED, module LED, tag state, healthy neighboring channels", ["Separate device, wiring, module, tag and HMI possibilities", "Order checks from safest to most intrusive", "Select the likely boundary", "Define the pass/fail recovery test"],
           ["Architecture drawing", "I/O list", "Tag standard", "Signal-trace report", "Backup record"], "Core PLC and control-systems technician competency."),
    Module(4, "Ladder Logic core patterns", "5-11 Oct 2026", 1,
           "Read, write, comment and test maintainable Ladder Logic before building operating modes and sequences.",
           ["Rung evaluation, examine-on/off, coils and internal bits", "Seal-in, Set/Reset, one-shots and reset risks", "On-delay/off-delay timers, counters and comparisons", "Retentive behavior, duplicate coils, comments and written tests"],
           ["Write a start/stop rung from memory", "Build a five-second delayed output", "Build an object counter with one-shot and reset", "Write truth tables before running each routine"],
           ["Compare seal-in with Set/Reset", "Predict a timer when enable flickers", "Find and correct a duplicate-coil fault"],
           "One box is counted several times", "The photoeye remains true for 180 ms, the scan is about 10 ms, and the counter is enabled directly by the input.",
           "Input duration, scan estimate, counter enable logic", ["Explain the scan-related cause", "Choose an edge pattern", "Predict the corrected count", "Add a sensor-chatter test"],
           ["Commented routine library", "Truth tables", "Timer/counter tests", "Revision log"], "Demonstrates the minimum programming fluency expected in junior PLC roles."),
    Module(5, "Modes, permissives, interlocks, sequences and faults", "12 Oct-1 Nov 2026", 3,
           "Design predictable command ownership, ordered steps, fault handling and controlled recovery.",
           ["Command, status, feedback, permissive, interlock, alarm and trip", "Auto/Manual and Local/Remote ownership; transition behavior", "Sequence steps, transitions and state-machine awareness", "Start-failure timing, first-out fault, acknowledgement, reset and cause-and-effect"],
           ["Create a permissive summary and Boolean start condition", "Define ownership in every mode", "Build a three-step sequence", "Inject five faults and prove reset requires correction"],
           ["Classify low pressure as permissive, alarm or trip", "Design Auto-to-Manual transition behavior", "Explain acknowledgement versus reset"],
           "A conveyor stalls at transfer", "Step 3 is active. Safety and overload are healthy. Downstream Ready is false. No trip is active.",
           "Active step, safety state, overload state, readiness input", ["Explain why code changes are not the first action", "Trace Downstream Ready", "Define useful HMI diagnostics", "Write recovery and regression tests"],
           ["Sequence chart", "Control narrative", "Cause-and-effect", "PLC logic", "FAT results"], "A high-value competence across packaging, process and machine automation."),
    Module(6, "Motors, starters, protection and VFD fundamentals", "2-15 Nov 2026", 2,
           "Understand motor-control interfaces and distinguish PLC, starter, drive, motor and process faults safely.",
           ["Three-phase motor and nameplate fundamentals", "DOL/reversing starters, interlocks and overload feedback", "VFD run, direction, speed, ready, running and fault signals", "Hardwired, analog and network interfaces; ramps and stored-energy awareness"],
           ["Trace a PLC-to-DOL command and feedback loop", "Read and explain a sample motor nameplate", "Create a PLC-to-VFD signal map", "Build a motor faceplate and layer-based fault tree"],
           ["Explain command versus running feedback", "Calculate percent speed at 35 Hz of 50 Hz", "List reasons a healthy drive may not run"],
           "VFD has a run command but the motor does not turn", "PLC command is true and speed reference is 60 percent. The drive shows LOCAL and Ready is false.",
           "PLC command, speed reference, control source and Ready status", ["Identify the controlling layer", "Explain why PLC edits are inappropriate", "State the simulated correction", "Verify start, stop, speed and fault response"],
           ["Starter schematic", "VFD signal map", "PLC routine", "Faceplate", "Test record"], "Matches common technician duties around motors, drives and production downtime."),
    Module(7, "Sensors and measurement principles", "16-29 Nov 2026", 2,
           "Understand how physical conditions become trustworthy values and how selection, installation and process effects influence measurement.",
           ["Process-sensor-transmitter-PLC-HMI chain", "Temperature, pressure, level and flow technologies", "LRV, URV, range, span, accuracy, repeatability and response", "Open, short, frozen, noisy, drifting and implausible failures"],
           ["Draw four measurement chains", "Compare three technologies for one service", "Create an instrument list", "Classify six trends by likely failure symptom"],
           ["Select level technology for clean water and foaming service", "Calculate span for -1 to 9 bar", "Explain accurate instrument but poor measurement"],
           "Ultrasonic level jumps during filling", "The level is erratic only while the inlet valve is open. Communication is healthy; foam and turbulence form below the sensor.",
           "Trend behavior, communication quality, observed foam/turbulence", ["Separate electrical, configuration, installation and process causes", "Choose the likely cause", "Propose mitigations", "Define evidence of improvement"],
           ["Process sketch", "Instrument list", "Selection matrix", "Trend-based fault report"], "Strengthens instrumentation awareness without claiming calibration authorization."),
    Module(8, "Analog signals, 4-20 mA, scaling and calibration records", "30 Nov-13 Dec 2026", 2,
           "Convert raw signals into engineering units, recognize abnormal values and troubleshoot analog loops systematically.",
           ["4-20 mA live zero and transmitter wiring concepts", "Raw counts, current, percent and engineering-unit scaling", "Under/over-range, open loop, noise, shielding and filtering", "Zero/span, as-found/as-left records and HART awareness"],
           ["Create percent/current tables for two ranges", "Build a two-way scaling worksheet", "Simulate two transmitters and compare values", "Add abnormal-signal and plausibility alarms"],
           ["Convert 12 mA on a 0-10 bar range", "Convert 650 L/min to current for 0-1000 L/min", "Explain 0 mA versus valid 0 percent"],
           "Pressure display is consistently high", "A 0-10 bar transmitter gives about 12 mA at trusted 5 bar, while PLC scaling is configured for 0-16 bar.",
           "Transmitter range, current, trusted reference and PLC scaling", ["Calculate the correct value", "Identify the root cause", "Explain why recalibration is wrong", "Verify 0, 50 and 100 percent"],
           ["Loop diagram", "Scaling workbook", "PLC configuration", "Alarm tests", "Three-point verification"], "A core junior instrumentation and PLC integration skill."),
    Module(9, "Process control, valves, alarms and PID fundamentals", "14 Dec 2026-3 Jan 2027", 3,
           "Understand feedback-loop behavior so process symptoms, actuator faults and alarm responses can be interpreted correctly.",
           ["Process objective, PV, SP, MV/CV and disturbances", "Open/closed loop, Manual/Automatic and bumpless-transfer awareness", "Proportional, integral, derivative, lag, dead time, overshoot and saturation", "Valve action/fail position; alarm deadband, priority, trip and recovery"],
           ["Draw three feedback loops", "Interpret stable, overshoot, oscillation and saturation trends", "Create an alarm list with operator response", "Test Manual/Automatic level behavior and valve discrepancy"],
           ["Identify PV, SP and MV in a level loop", "Compare High alarm and High-High trip", "Write controlled restart after a trip"],
           "Tank reaches High-High while outlet is commanded open", "Outlet command is 100 percent, position feedback remains 5 percent, inlet flow continues, and communications are healthy.",
           "Command, position feedback, inlet flow, level trend and comms state", ["Identify the failed loop element", "State the protective action", "Choose diagnostic trends", "Write recovery verification"],
           ["P&ID", "Control narrative", "Alarm list", "Trend analysis", "Cause-and-effect row"], "Provides process literacy needed to troubleshoot beyond the PLC code."),
    Module(10, "HMI and SCADA design, alarms and trends", "4-10 Jan 2027", 1,
           "Present process state clearly and make mode, interlock, quality and communications problems visible to operators.",
           ["Overview, detail, alarm, trend and diagnostic displays", "Equipment faceplates, ownership, navigation and restrained color", "Alarm priority, acknowledgement and operator response", "Tag quality, timestamps, stale data, access and command confirmation"],
           ["Sketch a five-screen hierarchy", "Build a process overview and equipment faceplate", "Configure five alarms with responses", "Create a diagnostic trend with command, feedback, PV, SP and quality"],
           ["Choose overview versus maintenance information", "Specify behavior during comms loss", "Design confirmation for a high-impact command"],
           "A normal-looking value remains after PLC communications fail", "The network is removed. Level remains at 62 percent; timestamp stops; comms status is false but hidden.",
           "Last value, frozen timestamp, hidden comms status", ["Identify the display failure", "Define stale-data appearance", "Add status and alarm behavior", "Test loss and recovery"],
           ["Screen hierarchy", "Overview", "Faceplate", "Alarm tests", "Comms-loss screenshots"], "Directly supports junior SCADA and controls support work."),
    Module(11, "Industrial networking and control communications", "11-24 Jan 2027", 2,
           "Diagnose physical, link, addressing, protocol, mapping and application problems in the correct order.",
           ["Ethernet links, switches, topology, MAC, IPv4, subnet and gateway", "Ping, TCP/UDP and client/server awareness", "RS-485, Modbus RTU/TCP, registers, offsets, data types and byte order", "OPC UA concepts; Profinet/EtherNet-IP awareness; timeouts and stale data"],
           ["Draw PLC-HMI-SCADA-switch-VFD architecture", "Create an IP schedule and subnet checks", "Build a ten-point Modbus map", "Run timeout, bad-map and recovery tests"],
           ["Check whether two /24 addresses share a subnet", "Explain IP address versus register address", "List causes when ping works but data does not"],
           "SCADA can ping the PLC but tank level does not update", "Pump status updates. PLC level is 57.3 percent. The client reads 40011 while the map assigns level to 40010.",
           "Successful ping, working pump status, PLC value and conflicting register map", ["Name the working and failing layers", "Correct the mapping", "Verify type and scale", "Test timeout and recovery"],
           ["Network architecture", "IP schedule", "Protocol map", "Comms test record", "Fault report"], "Industrial networks are repeatedly requested in current control-system roles."),
    Module(12, "SCADA integration, diagnostics and historical data", "25-31 Jan 2027", 1,
           "Prove the complete process-to-PLC-to-network-to-SCADA path, including commands, alarms, trends, quality and recovery.",
           ["End-to-end tag lifecycle and naming", "Read/write permissions, confirmation and audit awareness", "Alarm/event path; scan, polling, trend and historian concepts", "Watchdogs, backup/export/restore and least-privilege awareness"],
           ["Integrate at least 20 tags", "Create a tag register with source, scale, access and quality", "Test five alarms end to end", "Break communication, restore it and record recovery"],
           ["Trace one operator command and feedback", "Specify read-only and read/write tags", "Write communications acceptance criteria"],
           "Values update but operator commands are rejected", "Status values update. Start has no effect. The Start tag is configured read-only; local physical start works.",
           "Healthy connection, read-only tag configuration, working local command", ["Separate network, access, PLC and field layers", "Correct the tag access", "Add confirmation and audit behavior", "Test allowed and denied commands"],
           ["Architecture", "Tag register", "Alarm tests", "Trends", "Command-path tests", "Recovery record"], "Builds credible end-to-end SCADA support capability."),
    Module(13, "Maintenance troubleshooting, testing and change control", "1-7 Feb 2027", 1,
           "Diagnose with evidence, preserve recoverability and document controlled changes and handovers.",
           ["Symptom, root cause, contributing condition and known-good state", "Layered trace: power-field-I/O-logic-output-actuator-process-HMI", "Monitoring, trends, alarms, forcing/bypass risks", "Backup, version, rollback, FAT/SAT, retest and escalation"],
           ["Build an expected-state table", "Create a check-basics-first fault flow", "Inject and diagnose ten faults", "Write a controlled-change and unresolved-handover template"],
           ["Separate symptom and cause in five examples", "Explain how forcing hides faults", "Write normal, fault and recovery tests"],
           "Pump will not start after maintenance", "Auto is selected but Start Permitted is false. E-stop, overload and level are healthy. Local/Remote feedback says Local.",
           "Permissive summary, selector feedback, healthy PLC/network", ["Define expected state", "Identify the blocking permissive", "Explain why bypass is wrong", "Restore, verify and hand over"],
           ["Ten fault reports", "Expected-state tables", "Change log", "Backup record", "Handover note"], "Troubleshooting discipline is the strongest transferable technician signal."),
    Module(14, "System integration, commissioning and lifecycle handover", "8-28 Feb 2027", 3,
           "Combine technical subsystems into a traceable, testable control solution without turning the syllabus into a portfolio module.",
           ["Requirements, scope, assumptions, exclusions and acceptance criteria", "Equipment modules, modes, commands, status, faults and safe states", "Interface control: tags, units, scaling, ownership and network-loss behavior", "FAT/SAT awareness, defect control, backups, cybersecurity hygiene and handover"],
           ["Freeze a small integration specification", "Audit one tag across drawings, PLC, HMI and SCADA", "Execute normal, mode, fault, comms-loss and recovery tests", "Prepare a concise technical handover and limitation statement"],
           ["Write five measurable acceptance criteria", "Decide what remains local if SCADA fails", "Build a defect-and-retest workflow"],
           "SCADA fails during an automatic fill", "PLC scan and local I/O remain healthy. High and High-High protection live in the PLC. Remote commands are unavailable and displayed values become stale.",
           "PLC health, local protection, stale SCADA values and lost remote command", ["Define what continues locally", "Specify indication and ownership", "Choose pause/continue/stop behavior from risk", "Test protection and recovery"],
           ["Integration specification", "Interface register", "FAT", "Defect register", "Backup/restore record", "Handover"], "Completes the technical lifecycle expected of a supervised junior contributor."),
]


def module_table(module: Module) -> Table:
    rows = [
        [P("MODULE", "table_head"), P("DATES", "table_head"), P("DURATION", "table_head")],
        [P(f"{module.num:02d} - {ptext(module.title)}", "table_bold"), P(ptext(module.dates), "table"), P(f"{module.weeks} week" + ("s" if module.weeks != 1 else ""), "table")],
    ]
    t = Table(rows, colWidths=[104 * mm, 43 * mm, 27 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def two_col_lists(left_title: str, left_items: list[str], right_title: str, right_items: list[str]) -> Table:
    left = [P(ptext(left_title).upper(), "label")] + checklist(left_items, "small")
    right = [P(ptext(right_title).upper(), "label")] + checklist(right_items, "small")
    t = Table([[left, right]], colWidths=[87 * mm, 87 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def build_syllabus():
    path = OUT / "Emmanual-Januarie-Junior-Automation-Controls-Syllabus.pdf"
    doc = TrainingDoc(path, "Junior Automation and Controls Technician Syllabus", "TECHNICAL SYLLABUS")
    story = cover_story(
        "Junior Automation and Controls Technician Syllabus",
        "A focused technical curriculum with modules, activities, exercises, case studies and competency gates",
        "7 September 2026 - 28 February 2027",
        ["14 technical modules", "25 core weeks", "Approximately 425 guided hours", "PC-first practical work with explicit safety limits"],
        "Technical learning only. Portfolio construction, CV work and applications are intentionally kept outside this syllabus.",
    )
    story += [PageBreak(), P("Purpose and target standard", "h1"),
              P("This syllabus prepares Emmanual Januarie to contribute as a junior or trainee automation and control technician under supervision. It emphasizes electrical controls, PLCs, instrumentation, HMI/SCADA, industrial communications, systematic troubleshooting, testing and technical documentation."),
              info_box("Honest boundary", "This is a personal training syllabus, not a trade qualification, apprenticeship, licence, site authorization, safety certificate or substitute for supervised plant experience.", "gold"),
              P("Role-aligned competency priorities", "h2")]
    role_rows = [[P("Priority", "table_head"), P("What a junior should be able to demonstrate", "table_head")],
                 [P("Core", "table_bold"), P("Read basic control schematics; trace 24 VDC I/O; explain the PLC scan; create and test Ladder Logic; work with modes, permissives, interlocks and sequences.", "table")],
                 [P("Core", "table_bold"), P("Diagnose faults across power, field device, wiring, I/O, logic, output, actuator, process, network and HMI layers without random changes.", "table")],
                 [P("Core", "table_bold"), P("Create usable I/O lists, tag registers, control narratives, cause-and-effect tables, network maps, test records, fault reports and change logs.", "table")],
                 [P("Role-dependent", "table_bold"), P("Scale 4-20 mA signals, interpret measurement faults, understand valves and PID behavior, and support HMI/SCADA, trends and industrial communications.", "table")],
                 [P("Awareness", "table_bold"), P("Know when a task requires formal authorization, qualified electrical work, site procedures, OEM training, cybersecurity controls or escalation.", "table")]]
    rt = Table(role_rows, colWidths=[28 * mm, 146 * mm], repeatRows=1)
    rt.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("GRID", (0,0), (-1,-1), .5, LINE), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6), ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
    story += [rt, Spacer(1, 4 * mm), P("The role scan behind this design consistently emphasizes PLC/HMI/SCADA, drives, instrumentation, industrial networks, drawings, testing, commissioning, fault finding, documentation, safety and supervised learning. The syllabus therefore gives these areas more weight than advanced theory or vendor-specific specialization.", "small"),
              PageBreak(), P("Program map", "h1")]
    map_rows = [[P("No.", "table_head"), P("Dates", "table_head"), P("Technical module", "table_head"), P("Primary output", "table_head")]]
    for m in modules:
        map_rows.append([P(str(m.num), "table_bold"), P(ptext(m.dates), "tiny"), P(ptext(m.title), "tiny"), P(ptext(m.deliverables[0] + "; " + m.deliverables[-1]), "tiny")])
    mt = Table(map_rows, colWidths=[10*mm, 34*mm, 71*mm, 59*mm], repeatRows=1)
    mt.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT]), ("GRID", (0,0), (-1,-1), .4, LINE), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)]))
    story += [mt, Spacer(1, 5 * mm), info_box("Module completion rule", "A module is complete only when the learner can explain the concept, apply it, test normal and fault behavior, and produce readable evidence. Watching material alone is preparation, not completion.")]

    story += [PageBreak(), P("Assessment and evidence standard", "h1"),
              P("Each module uses the same evidence ladder so claims remain defensible."),
              two_col_lists("Evidence labels", ["Studied - explain in your own words", "Simulated - built in training software", "Implemented - configured/programmed yourself", "Tested - expected and actual results recorded", "Documented - usable technical record exists", "Certified - valid formal certificate held"],
                            "Completion gate", ["Closed-book explanation completed", "Exercises corrected and understood", "Normal behavior tested", "At least two fault paths tested", "Root cause supported by evidence", "Files dated, versioned and backed up"]),
              P("Technician troubleshooting method", "h2")]
    trouble_rows = [[P("Stage", "table_head"), P("Required behavior", "table_head")]]
    trouble = [
        ("1. Make safe", "Identify hazards, stored energy, state and authorization limits."),
        ("2. Define", "Write expected behavior, actual behavior, timing and recent changes."),
        ("3. Check basics", "Power, safety state, mode, permissives, device status, links and alarms."),
        ("4. Trace", "Field device -> I/O -> tag -> logic -> output -> actuator -> process -> HMI."),
        ("5. Isolate", "Use evidence and known-good comparison; change one thing at a time."),
        ("6. Test", "Write the expected safe result before performing the test."),
        ("7. Diagnose", "Name the root cause separately from symptoms and contributing conditions."),
        ("8. Correct", "Make one authorized, controlled correction with rollback where relevant."),
        ("9. Verify", "Repeat the failed step, normal test, fault test and recovery test."),
        ("10. Document", "Record cause, action, result, version, remaining risk and handover."),
    ]
    for a,b in trouble:
        trouble_rows.append([P(a, "table_bold"), P(b, "table")])
    tt=Table(trouble_rows,colWidths=[34*mm,140*mm],repeatRows=1)
    tt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),("GRID",(0,0),(-1,-1),.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    story += [tt]

    for m in modules:
        story += [PageBreak(), module_table(m), Spacer(1, 4 * mm), P(ptext(m.objective), "h2"),
                  info_box("Role value", ptext(m.role_value)), Spacer(1, 3 * mm),
                  two_col_lists("Core content", m.topics, "Required activities", m.activities),
                  Spacer(1, 4 * mm), P("Required exercises", "h2")]
        story += checklist(m.exercises, "body")
        story += [P("Module outcome", "h2"),
                  P("By the end of this module, the learner must explain the core content without copied notes, complete the exercises, apply the topic in simulation or a safe training context, diagnose the case study systematically, and produce the listed deliverables."),
                  info_box("Safety and scope check", "State assumptions and authorization limits. Never use mains voltage, defeat protection, force live equipment, or represent simulation as commissioned field work.", "gold"),
                  PageBreak(), P(f"Module {m.num:02d} technician case study", "h1"),
                  P(ptext(m.case_title), "h2"), P(f"<b>Situation:</b> {ptext(m.situation)}"),
                  P(f"<b>Available evidence:</b> {ptext(m.evidence)}"),
                  P("Your tasks", "h2")]
        story += checklist(m.tasks)
        story += [P("Required technical evidence", "h2"), two_col_lists("Deliverables", m.deliverables, "Verification record", ["Expected result written before testing", "Normal condition tested", "At least two relevant faults tested", "Recovery tested", "Actual results recorded", "Untested items marked NOT TESTED", "Files versioned and backed up", "Result explainable without notes"]),
                  Spacer(1, 5 * mm), info_box("Case-study rule", "Do not guess or change multiple things at once. Define expected behavior, isolate the failing layer, choose a safe test, support the root cause with evidence, correct it, verify recovery and record the result."),
                  Spacer(1, 6 * mm), P("[ ] MODULE COMPLETE    Date: ____________________    Revisit needed: YES / NO", "body")]

    story += [PageBreak(), P("Final technical release standard", "h1"),
              P("The target is credible junior contribution under supervision, not unsupported expert status."),
              two_col_lists("Target Level 3/4", ["Electrical calculations and schematic tracing", "PLC scan, I/O and Ladder Logic", "Modes, permissives, sequences and faults", "4-20 mA scaling and loop reasoning", "Systematic troubleshooting and verification"],
                            "Target Level 2/3", ["HMI/SCADA, alarms, trends and quality", "Industrial networks and protocol diagnostics", "Motors, VFDs, valves and PID awareness", "Lifecycle documents, FAT and change control", "Cybersecurity and authorization awareness"]),
              P("Release questions", "h2")]
    story += checklist(["Can every screenshot and diagram be explained without notes?", "Does each test show expected and actual results?", "Are simulations labelled as simulations?", "Are unperformed tests marked NOT TESTED?", "Can one complete signal be traced through field, PLC, network and HMI layers?", "Can a fault be isolated without random code changes?", "Are safety and authorization limits stated clearly?"])
    story += [PageBreak(), P("Role-alignment references", "h1"),
              P("Content was cross-checked against the attached source PDFs and a current role scan on 2 September 2026. Job requirements vary by employer, industry and jurisdiction; each vacancy and local legal framework remains authoritative."),
              P("Current role examples", "h2"),
              P("1. Adsyst Automation - Graduate/Junior Control Systems Technician: PLC, SCADA, HMI, VSDs, instrumentation, specifications, architecture, testing and commissioning."),
              P("https://careers.adsyst.co.uk/job/886184", "small"),
              P("2. Siemens - Field Service Engineer Apprenticeship: electrical safety, drawings, troubleshooting, PLC/HMI operation, networks, FAT/SAT and document control."),
              P("https://jobs.siemens.com/en_US/externaljobs/JobDetail/478759", "small"),
              P("3. Anglo American / De Beers - C&I Technician Plant (South Africa): instrumentation and control maintenance, PLC/SCADA programming and problem-solving methods; formal qualification and experience requirements apply."),
              P("https://jobs.smartrecruiters.com/AngloAmericanDeBeersGroup/744000143313275-c-i-technician-plant", "small"),
              Spacer(1, 8 * mm), info_box("Important", "This study plan improves technical readiness and evidence quality. It does not guarantee employment or replace employer-specific qualifications, trade requirements, site inductions, medicals, licences or supervised experience.", "gold")]
    doc.build(story)
    return path


@dataclass
class Project:
    num: int
    title: str
    window: str
    pitch: str
    competencies: list[str]
    scope: list[str]
    milestones: list[tuple[str,str,str]]
    faults: list[str]
    evidence: list[str]
    demo: list[str]
    golden: list[str]


projects = [
    Project(1, "Smart Conveyor Sorting Cell", "21 September - 1 November 2026",
            "A two-zone conveyor cell that detects, counts and transfers products with clear operating modes, permissives, feedback and fault recovery.",
            ["24 VDC control concepts", "PLC I/O and scan cycle", "Ladder Logic", "Modes and command ownership", "Timers, counters and one-shots", "HMI diagnostics", "FAT and troubleshooting"],
            ["Two conveyors, two photoeyes, two motor commands and running feedback", "Auto, Manual and Local/Remote simulation", "Start permissives, overload trips, jam timing and downstream-ready logic", "Count target, batch-complete state and controlled reset", "HMI overview, faceplates, alarms and sequence-state display"],
            [("21 Sep-4 Oct", "Design", "Process sketch, 12-point I/O list, tag standard and signal trace"), ("5-11 Oct", "Logic library", "Start/stop, timer, counter, one-shot and comparison routines"), ("12-25 Oct", "Integrate", "Modes, sequence, HMI, faults and cause-and-effect"), ("26 Oct-1 Nov", "Prove", "FAT, defect correction, recovery tests and recorded demo")],
            ["Sensor LED on but PLC input off", "Repeated counts from a maintained sensor", "Downstream Ready false", "Motor command true but feedback missing", "Overload trip and reset-before-correction attempt", "Communication loss and stale HMI indication"],
            ["README with architecture and assumptions", "I/O list and tag standard", "Control narrative and sequence chart", "Commented PLC logic", "HMI screenshots", "Cause-and-effect matrix", "FAT with expected/actual results", "Three fault reports", "Two-minute demo"],
            ["Explain the scan and one signal path", "Run Auto cycle", "Switch mode and show ownership", "Inject a jam fault", "Recover only after correction", "Show evidence and limitations"],
            ["First-out fault banner", "State/transition diagram beside live sequence state", "A before/after diagnosis screenshot pair", "A recruiter-readable one-page architecture"]),
    Project(2, "Automated Batch Tank and Dosing Station", "2 November 2026 - 3 January 2027",
            "A simulated fill, mix, dose and drain process combining motor/VFD control, instruments, 4-20 mA scaling, valves, alarms and basic feedback control.",
            ["Motors and VFD interface", "Sensor selection", "4-20 mA scaling", "Analog validation", "Process sequences", "Valves and fail state", "Alarms, trends and PID awareness"],
            ["Inlet valve, outlet valve, mixer motor and dosing pump", "Level and flow transmitters with simulated 4-20 mA signals", "Auto batch sequence with hold, abort and controlled restart", "Manual/Automatic level behavior; PID awareness without claiming tuning expertise", "Alarm priorities, High-High trip, discrepancy alarms and trend diagnostics"],
            [("2-15 Nov", "Actuation", "Motor/VFD map, faceplate, command/feedback tests"), ("16-29 Nov", "Measurement", "Instrument selection, list, ranges and failure states"), ("30 Nov-13 Dec", "Analog", "Loop diagrams, scaling, quality and alarm tests"), ("14 Dec-3 Jan", "Process", "Sequence, valves, alarms, trends, FAT and demo")],
            ["Drive left in LOCAL", "Frozen level value", "Noisy analog signal", "Wrong PLC scaling range", "Outlet valve command/position discrepancy", "High-High trip during filling"],
            ["P&ID and process description", "I/O and instrument lists", "Loop diagrams and scaling worksheet", "PLC logic and HMI screens", "Alarm rationalization table", "Trend screenshots with event explanation", "FAT and fault reports", "Three-minute demo"],
            ["Trace level from process to HMI", "Run one complete batch", "Show scaling at 0/50/100 percent", "Inject valve discrepancy", "Explain trend and protective action", "Show controlled restart"],
            ["Animated but restrained process overview", "Three-point scaling proof", "Alarm cause-response-consequence table", "Trend-based root-cause explanation"]),
    Project(3, "Plantwide SCADA and Industrial Communications Lab", "4 January - 7 February 2027",
            "A small multi-device control network that proves tag mapping, data quality, alarms, trends, commands, timeouts, access control and communications recovery.",
            ["HMI/SCADA usability", "IPv4 and subnet basics", "Modbus TCP mapping", "OPC UA awareness", "Read/write permissions", "Watchdogs and stale data", "Backup, restore and change control"],
            ["PLC, HMI, SCADA/client, switch and simulated VFD/instrument nodes", "IP schedule and protocol map", "At least 20 integrated tags with source, data type, scale, access and quality", "Alarm/event and diagnostic trend views", "Loss-of-comms behavior, local control philosophy and recovery timing"],
            [("4-10 Jan", "HMI design", "Hierarchy, overview, faceplates, alarm and trend views"), ("11-24 Jan", "Network", "Architecture, IP plan, Modbus map and layered tests"), ("25-31 Jan", "SCADA", "Tags, alarms, trends, access and recovery"), ("1-7 Feb", "Fault pack", "Ten network/system faults, change log and retest")],
            ["Wrong subnet", "Wrong Modbus register", "Wrong data type or byte order", "Read-only command tag", "PLC offline", "Stale value without quality indication", "Timeout too long", "Incorrect scale", "Duplicate tag name", "Restore from wrong version"],
            ["Network architecture and IP schedule", "Protocol/tag map", "SCADA screen pack", "Alarm and trend tests", "Command-access test", "Loss/recovery timeline", "Backup/restore checklist", "Ten fault reports", "Three-minute demo"],
            ["Show architecture and tag lifecycle", "Prove a normal data exchange", "Break one mapping", "Diagnose by layer", "Break communications", "Show stale indication and safe local behavior", "Restore and time recovery"],
            ["Layer-status diagnostic page", "Single tag traced across all layers", "Comms-loss event timeline", "Access-control test showing allowed and denied actions"]),
    Project(4, "Integrated Water Treatment Automation System", "8 February - 31 March 2027",
            "The flagship: a simulated raw-water, treatment, filtration and storage process that unifies PLC, instrumentation, HMI/SCADA, networks, testing, troubleshooting and lifecycle documentation.",
            ["Requirements and architecture", "Reusable equipment modules", "Process sequences and interlocks", "Analog instruments and validation", "SCADA and networks", "FAT and defect management", "Troubleshooting and handover"],
            ["Raw-water intake, transfer pumping, treatment tank, filtration and storage", "Pumps, valves, level/flow/pressure/quality signals", "Local protection retained if SCADA fails", "Clear Auto/Manual and Local/Remote ownership", "Alarm priorities, trends, quality indication and recovery", "Controlled scope: simulation only, with explicit exclusions"],
            [("8-14 Feb", "Baseline", "URS-lite, P&ID, architecture, I/O, instruments and acceptance criteria"), ("15-21 Feb", "Integrate", "Equipment modules, sequences, HMI/SCADA and communications"), ("22-28 Feb", "FAT", "Normal, mode, fault, network-loss and recovery tests"), ("1-14 Mar", "Harden", "Fix defects, run regression, audit tags and backups"), ("15-31 Mar", "Present", "Final technical demonstration, evidence index and honest limitations")],
            ["Pump start failure", "Level transmitter open loop", "Valve position discrepancy", "Filter high differential pressure", "PLC-SCADA network loss", "Stale historian value", "Incorrect mode ownership", "Alarm flood after restart", "Wrong tag scale", "Backup/restore mismatch"],
            ["Requirements and scope", "P&ID and system architecture", "I/O, instrument, alarm and tag registers", "Control narrative and cause-and-effect", "PLC/HMI/SCADA evidence", "Network plan", "FAT and defect log", "Fault reports", "Backup/change log", "Five-to-ten-minute demo"],
            ["Open with requirements and safe-state philosophy", "Trace one critical loop end to end", "Run normal automatic operation", "Inject network loss and prove local protection", "Show defect, fix and regression evidence", "Close with limitations and next engineering steps"],
            ["Requirements-to-test traceability matrix", "One-page executive architecture", "Network-failure philosophy", "Defect closure chart", "Short narrated demo with timestamps"]),
]


def build_portfolio():
    path = OUT / "Emmanual-Januarie-Golden-Portfolio-Projects.pdf"
    doc = TrainingDoc(path, "Golden Portfolio Projects", "PORTFOLIO PROJECTS")
    story = cover_story(
        "Four Golden Portfolio Projects",
        "A progressive evidence plan that demonstrates junior automation and controls competence without overstating field experience",
        "September 2026 - March 2027",
        ["4 recruiter-readable projects", "From discrete control to integrated SCADA", "Every claim backed by tests and documents", "Simulation / Training Project labels required"],
        "Each project is broad enough to prove competence, yet scoped tightly enough to finish and explain in an interview.",
    )
    story += [PageBreak(), P("Why these four projects", "h1"),
              P("Together, the projects cover the technical arc found in junior automation and control roles: electrical signal paths, PLC logic, modes and sequences, motors and drives, analog instrumentation, process control, HMI/SCADA, industrial networks, troubleshooting, testing and documentation."),
              info_box("Golden rule", "A smaller finished project with traceable tests is stronger than a large unfinished build. Every screenshot must be explainable, every simulation labelled, and every unperformed test marked NOT TESTED.", "gold"),
              P("Portfolio coverage matrix", "h2")]
    headers = ["Competence", "P1", "P2", "P3", "P4"]
    matrix = [
        ["Discrete I/O and Ladder", "High", "Med", "Low", "High"],
        ["Modes, sequences and faults", "High", "High", "Med", "High"],
        ["Motors and VFDs", "Med", "High", "Med", "High"],
        ["Instrumentation and 4-20 mA", "Low", "High", "Med", "High"],
        ["HMI/SCADA and alarms", "Med", "High", "High", "High"],
        ["Industrial networks", "Low", "Low", "High", "High"],
        ["Troubleshooting and testing", "High", "High", "High", "High"],
        ["Engineering documentation", "High", "High", "High", "High"],
    ]
    rows = [[P(x, "table_head") for x in headers]] + [[P(row[0], "table_bold")] + [P(x, "center") for x in row[1:]] for row in matrix]
    t=Table(rows,colWidths=[94*mm,20*mm,20*mm,20*mm,20*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(1,1),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [t, Spacer(1, 5*mm), P("Universal project release gate", "h2")]
    story += checklist(["Scope, assumptions, exclusions and safety boundaries are written", "Architecture, I/O/tags and acceptance criteria agree", "Normal, stop, fault and recovery behavior is tested", "Expected and actual results are recorded", "At least three evidence-based fault reports exist", "Backups, versions and change log are present", "README can be understood in under two minutes", "Demo can be delivered without hidden setup or unsupported claims"])

    for pr in projects:
        story += [PageBreak(), P(f"Project {pr.num:02d}", "cover_kicker"), P(ptext(pr.title), "h1"),
                  info_box("Recruiter pitch", ptext(pr.pitch), "gold"), Spacer(1, 3*mm),
                  Table([[P("BUILD WINDOW", "table_head"), P("LABEL", "table_head")], [P(ptext(pr.window), "table_bold"), P("Simulation / Training Project", "table_bold")]], colWidths=[87*mm,87*mm], style=[("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),.5,LINE),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]),
                  Spacer(1, 4*mm), two_col_lists("Competencies", pr.competencies, "System scope", pr.scope),
                  P("Acceptance criteria", "h2")]
        criteria = [
            "The system starts only when written permissives are true.",
            "Mode and command ownership are visible and deterministic.",
            "Normal operation, stop, fault and recovery match the control narrative.",
            "Bad signal or communications quality is visible and cannot look normal.",
            "Each critical fault produces a defined safe response and useful diagnostic.",
            "Documents, PLC/HMI tags and test records remain traceable by revision.",
        ]
        story += checklist(criteria, "small")
        story += [PageBreak(), P(f"Project {pr.num:02d} build plan", "h1")]
        rows=[[P("Window", "table_head"),P("Stage", "table_head"),P("Required output", "table_head")]]
        for a,b,c in pr.milestones:
            rows.append([P(ptext(a),"table"),P(ptext(b),"table_bold"),P(ptext(c),"table")])
        t=Table(rows,colWidths=[35*mm,31*mm,108*mm],repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        story += [t, Spacer(1,4*mm), two_col_lists("Required fault injections", pr.faults, "Evidence package", pr.evidence),
                  PageBreak(), P(f"Project {pr.num:02d} demonstration and scoring", "h1"),
                  P("Demonstration script", "h2")]
        story += [P(f"{i+1}. {ptext(x)}", "body") for i,x in enumerate(pr.demo)]
        story += [P("Golden differentiators", "h2")] + checklist(pr.golden)
        score_rows=[[P("Category", "table_head"),P("Weight", "table_head"),P("Release question", "table_head")],
                    [P("Correct function","table_bold"),P("25%","center"),P("Does normal operation match the written narrative?","table")],
                    [P("Fault behavior","table_bold"),P("25%","center"),P("Are faults isolated, protected and recoverable?","table")],
                    [P("Traceability","table_bold"),P("20%","center"),P("Do drawings, tags, logic and tests agree?","table")],
                    [P("Operator clarity","table_bold"),P("15%","center"),P("Are mode, quality, alarms and actions obvious?","table")],
                    [P("Explanation","table_bold"),P("15%","center"),P("Can the work be explained honestly without notes?","table")]]
        st=Table(score_rows,colWidths=[38*mm,22*mm,114*mm],repeatRows=1)
        st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        story += [st, Spacer(1,4*mm), info_box("Release gate", "Target at least 80/100, with no category below 60 percent. A safety, ownership or data-quality defect blocks release even if the total score passes.", "gold")]

    story += [PageBreak(), P("Portfolio file structure and evidence index", "h1"),
              P("Use the same predictable structure for all four projects."),
              info_box("Recommended folder pattern", "00_README | 01_Requirements | 02_Design | 03_PLC | 04_HMI_SCADA | 05_Network | 06_Testing | 07_Faults | 08_Demo | 09_Backups"),
              P("Evidence index fields", "h2")]
    story += checklist(["Evidence ID", "Project and document title", "Revision and date", "Studied / Simulated / Implemented / Tested / Documented", "What the artifact proves", "Tool or platform used", "Linked requirement or test", "Known limitation", "File path"])
    story += [P("README opening statement", "h2"), P("This is a personal Simulation / Training Project created to demonstrate junior automation and control-system skills. It was not commissioned on a live plant. Safety functions, field wiring and site behavior are represented only to the extent stated in the scope and limitations."),
              Spacer(1,5*mm), info_box("Final presentation standard", "Lead with the process problem, show the architecture, prove one normal cycle, inject one fault, explain the diagnosis, show recovery and close with documented limitations. Keep evidence stronger than adjectives.", "gold")]
    doc.build(story)
    return path


week_data = [
    (1,"M01","Electrical fundamentals","Quantities and safety","PLC purpose preview","Signal-chain preview","PV/SP preview","HMI purpose and screen hierarchy","Build low-voltage circuit evidence","Panel-indicator fault and filing","Foundation evidence pack","None - foundation"),
    (2,"M02","Control circuits","Relays, contactors and protection","Map relay logic to PLC","Switch states and feedback","Permissive chain","Ethernet and device addressing","Simulate DOL start/stop circuit","Seal-in fault report","Motor-control simulation","None - foundation"),
    (3,"M03","PLC hardware and I/O","24 VDC I/O paths","CPU, modules and scan","Digital input/output devices","Command and feedback path","I/O list and tag convention","Design conveyor I/O and architecture","Missing-input diagnosis","P1 design pack","Project 1 - Design"),
    (4,"M03","PLC addressing and diagnostics","PNP/NPN awareness","Tags, monitor and backups","Analog I/O overview","Timing and short pulses","Integration review","Complete signal tracing","Missing-output diagnosis","P1 signal trace","Project 1 - Design"),
    (5,"M04","Ladder Logic patterns","Control-circuit comparison","Seal-in, timers and counters","Sensor edge behavior","Timing and state behavior","Conveyor HMI controls","Build logic library","Counter case and retest","P1 logic library","Project 1 - Logic"),
    (6,"M05","Modes and permissives","Motor-control review","Permissives and interlocks","Object detection","Modes and ownership","PLC/HMI communications path","Add modes and start conditions","Will-not-start fault","P1 modes","Project 1 - Integrate"),
    (7,"M05","Sequences and feedback","Overload protection","Sequence and counting","Sensor plausibility","Command-feedback timers","Conveyor narrative and test plan","Add sequence, faults and HMI","Sequence-stall case","P1 integrated build","Project 1 - Integrate"),
    (8,"M05","Recovery and FAT","Isolation review","Refactor and comments","Signal plausibility","Safe recovery","Conveyor integration review","Execute conveyor FAT","Retest and close defects","P1 final release","Project 1 - Prove"),
    (9,"M06","Motors and starters","Motors and DOL starters","Motor interface logic","Running feedback","Command-feedback discrepancy","Motor/VFD faceplate","Build starter simulation","Overload diagnosis","P2 actuation pack","Project 2 - Actuation"),
    (10,"M06","VFD fundamentals","Nameplate and protection","Speed and reset logic","Analog speed reference","Drive status and trips","Drive communications awareness","Complete VFD interface","LOCAL/Ready case","P2 VFD interface","Project 2 - Actuation"),
    (11,"M07","Temperature and pressure","Sensor power and wiring","Input diagnostics","Temperature/pressure selection","Measurement quality","Instrument list and signal chains","Select and document instruments","Frozen-signal drill","P2 instrument list","Project 2 - Measurement"),
    (12,"M07","Level, flow and process effects","Shielding awareness","Alarm from measurement","Level/flow technologies","Installation and process effects","Motor/sensor integration review","Complete measurement chain","Ultrasonic-level case","P2 selection matrix","Project 2 - Measurement"),
    (13,"M08","4-20 mA and scaling","Analog wiring concepts","Raw values and scaling","Loop calculation","PV quality","Analog faceplate, alarms and trends","Build first analog loop","Open-loop diagnosis","P2 scaling proof","Project 2 - Analog"),
    (14,"M08","Analog faults and records","Noise and shielding","Plausibility alarms","Calibration/HART awareness","Filtering and validation","Serial and HART fundamentals","Test second loop","Wrong-scaling case","P2 analog verification","Project 2 - Analog"),
    (15,"M09","Valves and feedback loops","Actuator interfaces","Tank sequence and modes","Valves and position feedback","PV/SP/MV and feedback","Tank P&ID and alarm list","Build tank process","Valve-will-not-open","P2 process build","Project 2 - Process"),
    (16,"M09","Alarms, trips and PID behavior","Protection review","Alarm/trip logic","Instrument faults","PID trends","Light catch-up and integration","Add alarms and control","High-High case","P2 alarm/FAT prep","Project 2 - Process"),
    (17,"M09","Process recovery and release","Schematic review","Refactor and comments","Range/plausibility audit","Manual/Auto recovery","Light HMI review","Execute batch FAT","Close documents and release","P2 final release","Project 2 - Prove"),
    (18,"M10","HMI and SCADA usability","Panel/HMI power","HMI tag interface","PV quality display","Operator controls","IP plan and PLC/HMI path","Build screen hierarchy","Stale-data case","P3 HMI pack","Project 3 - HMI"),
    (19,"M11","Ethernet and addressing","Cables and topology","PLC Ethernet settings","Smart-instrument path","Data quality","Network and protocol map","Build IP plan and links","Link/IP fault","P3 network baseline","Project 3 - Network"),
    (20,"M11","Protocols and mapping","Shielding/termination awareness","Modbus and OPC mapping","Serial/HART review","Timeout and fallback","Communications recovery tests","Execute protocol tests","Wrong-register case","P3 protocol proof","Project 3 - Network"),
    (21,"M12","End-to-end SCADA integration","Control-panel review","PLC tag cleanup","Instrument quality","Integrated process path","SCADA overview and diagnostics","Integrate 20 tags and FAT","Read-only command case","P3 SCADA release","Project 3 - SCADA"),
    (22,"M13","Troubleshooting and change control","Electrical test sequence","I/O and logic tracing","Loop isolation","Process symptoms","Layered network fault finding","Run ten-fault pack","Pump selector case","P3 fault pack","Project 3 - Prove"),
    (23,"M14","Requirements and interfaces","Motor/valve interfaces","Equipment modules","Instrument definitions","Control narrative","Flagship baseline documents","Design first subsystem","Design review","P4 baseline","Project 4 - Baseline"),
    (24,"M14","Integration and failure behavior","Protection audit","Sequences and modes","PV validation","Alarms and PID","Subsystem integration","Integrate PLC/HMI/SCADA","Network-failure case","P4 integrated build","Project 4 - Integrate"),
    (25,"M14","Commissioning and handover","Schematic final","Logic cleanup and backup","Tag audit","Recovery behavior","Final HMI and trends","Execute FAT and close defects","Technical sign-off","P4 FAT release","Project 4 - FAT"),
    (26,"Review","Electrical and PLC consolidation","Timed schematic trace","Timed logic-from-spec","Scaling drill","Cause-and-effect drill","Network troubleshooting explanation","Fix highest-risk P4 defects","Regression tests","P4 hardened build","Project 4 - Harden"),
    (27,"Review","Instrumentation and SCADA consolidation","Control-path recall","PLC refactor","Instrument fault drill","Trend diagnosis","Evidence and document audit","Requirements-to-test audit","Fault-report rewrite","Traceability pack","Project 4 - Harden"),
    (28,"Review","Integrated troubleshooting","Electrical fault drill","PLC fault drill","Analog fault drill","Process fault drill","Mock technical demonstration","Run integrated fault set","Correct weak explanations","Demo rehearsal 1","Project 4 - Present"),
    (29,"Review","Targeted retest and release","Weak electrical topic","Weak PLC topic","Weak instrument topic","Weak process topic","Final SCADA usability review","Full regression and backup","Final evidence audit","Demo rehearsal 2","Project 4 - Present"),
    (30,"Close","Final three-day close-out","Final electrical recall","Final PLC and project demo","Final instrumentation recall","Not scheduled","Not scheduled","Not scheduled","Archive, next-study plan","Final release pack","Project 4 - Release"),
]


def friday_label(idx: int, friday: date) -> str:
    cycle = ["A - HMI/SCADA", "B - Networking", "C - Documentation", "D - Integration/review"][(idx-1)%4]
    if friday == date(2026,12,25):
        return "D - Light catch-up / rest"
    if friday == date(2027,1,1):
        return "A - Light HMI review / rest"
    return cycle


def build_weekly():
    path = OUT / "Emmanual-Januarie-Weekly-Study-Guide.pdf"
    doc = TrainingDoc(path, "Weekly Study Guide", "WEEKLY STUDY GUIDE")
    story = cover_story(
        "Weekly Study Guide",
        "A day-by-day plan synchronized with the technical syllabus and the four-project portfolio",
        "7 September 2026 - 31 March 2027",
        ["17 hours per full week", "Monday to Sunday", "25 core weeks plus March consolidation", "Exact technical and project outputs"],
        "Every week names the syllabus module, the active project milestone, the required daily work and the evidence to save.",
    )
    story += [PageBreak(), P("How the three PDFs work together", "h1"),
              P("Use this guide as the calendar. Read the named module in the Technical Syllabus, then build the named milestone in Four Golden Portfolio Projects. Do not replace technical study with portfolio polishing."),
              Table([[P("DOCUMENT", "table_head"),P("QUESTION IT ANSWERS", "table_head")],
                     [P("Technical Syllabus","table_bold"),P("What must I understand, practise and troubleshoot?","table")],
                     [P("Weekly Study Guide","table_bold"),P("What do I do today, for how long, and what do I save?","table")],
                     [P("Portfolio Projects","table_bold"),P("How do I combine the skills into four strong, explainable builds?","table")]], colWidths=[48*mm,126*mm], style=[("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]),
              P("Fixed weekly rhythm", "h2")]
    rhythm = [["Monday","2 h","20 recall | 60 learn | 40 calculate/draw"], ["Tuesday","2 h","20 recall | 50 learn | 50 program/test"], ["Wednesday","2 h","20 recall | 60 learn | 40 apply"], ["Thursday","2 h","20 recall | 60 learn | 40 process case"], ["Friday","2 h","20 review | 50 rotate | 40 practical | 10 file"], ["Saturday","4 h","60 plan | 120 build | 60 test/document"], ["Sunday","3 h","60 closed-book recall | 60 fault | 60 evidence review"]]
    rows=[[P("Day","table_head"),P("Time","table_head"),P("Structure","table_head")]]+[[P(a,"table_bold"),P(b,"center"),P(c,"table")] for a,b,c in rhythm]
    t=Table(rows,colWidths=[30*mm,20*mm,124*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    story += [t, Spacer(1,5*mm), info_box("Minimum viable week", "If life interrupts, protect Tuesday PLC practice, Saturday build/test work and Sunday recall/fault review. Reschedule foundations; do not quietly skip them.", "gold"),
              PageBreak(), P("Daily completion standard", "h1")]
    daily = [
        ("Monday - Electrical", "Recall last mistakes; learn one tight topic; solve at least five calculations or trace one circuit; record units and safe test steps."),
        ("Tuesday - PLC", "Explain the last routine from memory; write or modify logic; test start, stop, fault and restart; save commented evidence."),
        ("Wednesday - Instrumentation", "Trace sensor to HMI; calculate, draw or compare; state likely faults and safe checks."),
        ("Thursday - Process control", "Link the concept to a conveyor, tank or water process; write one operator action and one automatic response."),
        ("Friday - Rotation", "Complete only the dated A/B/C/D topic; save one artifact for Saturday integration."),
        ("Saturday - Project", "Write acceptance criteria; build; integrate; test expected versus actual; record next smallest action."),
        ("Sunday - Review", "Closed-book recall; one systematic fault; update wrong-answer log, test record and evidence index."),
    ]
    for a,b in daily:
        story += [P(a,"h2"),P(b)]
    story += [info_box("Evidence labels", "Studied | Simulated | Implemented | Tested | Documented | Certified. Use a label only when its evidence standard is actually met."),
              P("Friday rotation", "h2"),
              P("A = HMI/SCADA; B = Industrial networking; C = Technical documentation; D = Integration and review. The cycle begins Friday, 11 September 2026 and repeats continuously. 25 December and 1 January are deliberately light.")]

    start = date(2026,9,7)
    for entry in week_data:
        idx, mod, theme, mon, tue, wed, thu, fri_topic, sat, sun, output, project = entry
        monday = start + timedelta(days=7*(idx-1))
        if idx < 30:
            sunday = monday + timedelta(days=6)
        else:
            sunday = date(2027,3,31)
        friday = monday + timedelta(days=4)
        story += [PageBreak(), P(f"Week {idx:02d} | {monday.strftime('%d %b')} - {sunday.strftime('%d %b %Y')}", "cover_kicker"),
                  P(ptext(theme), "h1")]
        meta = Table([[P("SYLLABUS","table_head"),P("PROJECT TRACK","table_head"),P("WEEKLY OUTPUT","table_head")],
                      [P(ptext(mod),"table_bold"),P(ptext(project),"table_bold"),P(ptext(output),"table_bold")]], colWidths=[30*mm,58*mm,86*mm])
        meta.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        story += [meta, Spacer(1,4*mm)]
        day_rows=[[P("Day / time","table_head"),P("Technical focus","table_head"),P("Required result","table_head")]]
        days = [
            (monday,"Mon - 2 h",mon,"Recall, learn, then calculate, draw or trace. Save one corrected artifact."),
            (monday+timedelta(days=1),"Tue - 2 h",tue,"Write or inspect PLC logic line by line; test normal, stop, fault and restart."),
            (monday+timedelta(days=2),"Wed - 2 h",wed,"Apply through a loop sketch, range calculation, signal trace or fault symptom."),
            (monday+timedelta(days=3),"Thu - 2 h",thu,"Apply to the active process; state expected automatic and operator responses."),
            (friday,"Fri - 2 h",f"{friday_label(idx,friday)}: {fri_topic}","Create one rotation artifact and link it to the active build."),
            (monday+timedelta(days=5),"Sat - 4 h",sat,"Plan 60; build/integrate 120; test and document 60. Record expected vs actual."),
            (monday+timedelta(days=6),"Sun - 3 h",sun,"Recall 60; troubleshoot 60; file evidence and plan 60."),
        ]
        if idx == 30:
            days = days[:3]
        for d,label,focus,result in days:
            day_rows.append([P(f"{label}<br/>{d.strftime('%d %b')}","table_bold"),P(ptext(focus),"table"),P(ptext(result),"table")])
        dt=Table(day_rows,colWidths=[28*mm,61*mm,85*mm],repeatRows=1)
        dt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LIGHT]),("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        story += [dt, Spacer(1,4*mm), two_col_lists("Evidence to file", [output, "One PLC or diagnostic artifact", "One calculation/diagram/signal analysis", "One fault or case-study record"], "Weekly sign-off", ["Hours planned/completed recorded", "Correct module studied", "Correct project milestone advanced", "Normal and fault behavior tested", "Wrong-answer log updated", "Next smallest action written"])]

    story += [PageBreak(), P("Weekly record - print or duplicate", "h1")]
    fields=["Week number / dates","Syllabus module","Active project milestone","Hours planned / completed","Main concept learned","Practical output","Fault investigated","Evidence saved","Weak point to review","Next action"]
    rows=[[P(x,"table_bold"),P("______________________________________________________________","table")] for x in fields]
    ft=Table(rows,colWidths=[48*mm,126*mm])
    ft.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.5,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story += [ft, Spacer(1,5*mm), two_col_lists("Daily sign-off", ["Monday complete", "Tuesday complete", "Wednesday complete", "Thursday complete", "Friday rotation complete", "Saturday project complete", "Sunday review complete"], "Quality sign-off", ["Expected/actual recorded", "Fault evidence saved", "Simulation labelled", "NOT TESTED used honestly", "Files versioned/backed up", "Next week planned"]),
              Spacer(1,5*mm), info_box("Recovery rule", "If a week is missed, resume the next unfinished technical milestone. Do not skip prerequisite modules or double the next week's load. Reduce project scope before reducing safety, testing or documentation.", "gold")]
    doc.build(story)
    return path


if __name__ == "__main__":
    outputs = [build_portfolio(), build_syllabus(), build_weekly()]
    for output in outputs:
        print(output)
