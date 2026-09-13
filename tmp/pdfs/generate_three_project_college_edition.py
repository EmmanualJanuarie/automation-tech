from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

SYLLABUS_PATH = OUT / "01_Junior_Automation_Controls_Syllabus_COLLEGE_EDITION.pdf"
PORTFOLIO_PATH = OUT / "02_Junior_Automation_Controls_Portfolio_Projects_COLLEGE_EDITION.pdf"
GUIDE_PATH = OUT / "03_Study_Guide_7Sep2026_to_28Feb2027_COLLEGE_EDITION.pdf"

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

base = getSampleStyleSheet()
STYLES = {
    "cover_title": ParagraphStyle("cover_title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=10),
    "cover_sub": ParagraphStyle("cover_sub", parent=base["BodyText"], fontName="Helvetica", fontSize=12.5, leading=16, textColor=MUTED, alignment=TA_CENTER, spaceAfter=10),
    "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=NAVY, spaceAfter=8),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=14.5, leading=17, textColor=BLUE, spaceBefore=6, spaceAfter=4),
    "h3": ParagraphStyle("h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=BLUE, spaceBefore=4, spaceAfter=3),
    "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Helvetica", fontSize=9, leading=12, textColor=TEXT, spaceAfter=4),
    "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.6, leading=9.5, textColor=TEXT, spaceAfter=2),
    "tiny": ParagraphStyle("tiny", parent=base["BodyText"], fontName="Helvetica", fontSize=6.7, leading=8.1, textColor=TEXT),
    "tiny_bold": ParagraphStyle("tiny_bold", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=6.8, leading=8.2, textColor=NAVY),
    "label": ParagraphStyle("label", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=BLUE, spaceAfter=3),
    "center": ParagraphStyle("center", parent=base["BodyText"], fontName="Helvetica", fontSize=7.2, leading=8.5, textColor=TEXT, alignment=TA_CENTER),
}


def P(text: str, style: str = "body") -> Paragraph:
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), STYLES[style])


def PRich(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def checklist(items, style="body"):
    return [P(f"[ ] {item}", style) for item in items]


def box(title: str, body: str, amber=False, width=176 * mm):
    edge = AMBER if amber else BLUE
    bg = PALE_AMBER if amber else PALE_BLUE
    t = Table([[[P(title.upper(), "label"), P(body, "body")]]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.6, edge),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def table(headers, rows, widths, font=7.1, leading=8.7, repeat=1):
    hs = ParagraphStyle("th", parent=STYLES["tiny_bold"], fontSize=font, leading=leading, textColor=WHITE)
    bs = ParagraphStyle(f"tb{font}{leading}", parent=STYLES["tiny"], fontSize=font, leading=leading)
    data = [[Paragraph(escape(str(x)), hs) for x in headers]]
    data += [[Paragraph(escape(str(x)).replace("\n", "<br/>"), bs) for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=repeat, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        cmds.append(("BACKGROUND", (0, i), (-1, i), WHITE if i % 2 else PALE_ALT))
    t.setStyle(TableStyle(cmds))
    return t


def two_col(left_title, left_items, right_title, right_items):
    left = [P(left_title.upper(), "label")] + checklist(left_items, "small")
    right = [P(right_title.upper(), "label")] + checklist(right_items, "small")
    t = Table([[left, right]], colWidths=[88 * mm, 88 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_ALT),
        ("BOX", (0, 0), (-1, -1), 0.5, GRID),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


class CollegeDoc(BaseDocTemplate):
    def __init__(self, path: Path, title: str, code: str):
        self.header_code = code
        super().__init__(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=22 * mm, bottomMargin=21 * mm, title=title,
                         author="Emmanual Januarie", subject="Junior Automation and Controls Technician Development Programme")
        self.addPageTemplates(PageTemplate(id="all", frames=Frame(self.leftMargin, self.bottomMargin, self.width, self.height), onPage=self.decorate))

    def decorate(self, canvas, doc):
        page = canvas.getPageNumber()
        w, h = A4
        canvas.saveState()
        if page > 1:
            canvas.setStrokeColor(GRID)
            canvas.setLineWidth(0.6)
            canvas.line(18 * mm, h - 15.5 * mm, w - 18 * mm, h - 15.5 * mm)
            canvas.setFont("Helvetica-Bold", 7.5)
            canvas.setFillColor(NAVY)
            canvas.drawString(18 * mm, h - 11.5 * mm, self.header_code)
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawRightString(w - 18 * mm, h - 11.5 * mm, "JUNIOR AUTOMATION & CONTROLS TECHNICIAN")
        canvas.setStrokeColor(GRID)
        canvas.line(18 * mm, 16.5 * mm, w - 18 * mm, 16.5 * mm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 11.5 * mm, "Emmanual Januarie - Development Programme")
        canvas.drawRightString(w - 18 * mm, 11.5 * mm, f"Page {page}")
        canvas.restoreState()


def cover(title, subtitle, facts, promise):
    rows = [(a, b) for a, b in facts]
    return [
        Spacer(1, 30 * mm),
        P(title, "cover_title"),
        P(subtitle, "cover_sub"),
        Spacer(1, 10 * mm),
        table(["PROGRAMME INFORMATION", ""], rows, [52 * mm, 124 * mm], 7.7, 9.5),
        Spacer(1, 14 * mm),
        box("Purpose", promise),
        Spacer(1, 9 * mm),
        P("Prepared for Emmanual Januarie", "h2"),
        P("College-style personal learning programme - not an accredited qualification", "body"),
    ]


@dataclass
class Week:
    num: int
    module: str
    module_week: int
    theme: str
    scope: str
    topics: list[str]
    applications: list[str]
    outcomes: list[str]
    saturday: str
    project: str | None = None


WEEKS = [
    Week(1,"M1",1,"Electrical I","Voltage, current, resistance, Ohm's Law, power and DC circuits",
         ["Voltage","Current","Resistance","Ohm's Law","Electrical power and DC circuits"],
         ["A battery measures 9 V. State the potential difference and identify positive and negative reference points.","A branch carries 0.025 A. Convert to mA and show where an ammeter belongs.","Compare 220 ohm and 1 kohm loads on the same source; predict which draws less current.","Calculate voltage for 15 mA through 330 ohms, then calculate current at 9 V.","Calculate power for 9 V at 20 mA and select a supply with reasonable margin."],
         ["Explain electrical quantities and units","Rearrange V=IR","Calculate P=VI"],
         "Build a battery-resistor-LED circuit on the breadboard. Predict current, verify polarity, observe normal/open-circuit behavior and record expected versus actual results. Do not short the battery."),
    Week(2,"M1",2,"Electrical II","AC/DC, series and parallel circuits, measurement and multimeter fundamentals",
         ["AC and DC fundamentals","Series circuits","Parallel circuits","Voltage measurement","Current, resistance and continuity measurement"],
         ["Compare battery DC with mains AC and state why the home trainer remains low voltage.","Calculate total resistance and current for two series resistors on 9 V.","Calculate branch and total current for two parallel resistors.","Create a safe voltage-measurement plan with reference point and expected range.","Choose the correct meter connection for voltage, current, resistance and continuity; identify unsafe energized resistance testing."],
         ["Distinguish AC from DC","Solve series/parallel networks","Select safe meter methods"],
         "Build one series and one parallel LED/resistor circuit. Predict node voltages and branch behavior, compare brightness qualitatively, and document one open-branch fault. Use only battery-level voltage."),
    Week(3,"M1",3,"Electrical III","Relays, contactors, circuit protection and industrial control circuits",
         ["Relays and NO/NC contacts","Contactors and auxiliary contacts","Fuses, breakers and overload concepts","Start/Stop and seal-in circuits","Electrical control schematics"],
         ["Draw coil de-energized and energized contact states.","Trace a contactor coil, main contacts and auxiliary feedback without using mains voltage.","Match fuse, breaker and overload functions to faults they address.","Create a Start/Stop truth table with NC Stop and holding contact.","Trace supply-to-load and supply-to-coil paths on a motor-control schematic."],
         ["Recognize control components","Trace a holding circuit","Explain protection boundaries"],
         "Create a breadboard relay/contactor simulation using LEDs as coil, motor and feedback indications. Use jumpers or buttons for Start, Stop and overload; prove seal-in logic with a software or manual state table."),
    Week(4,"M1",4,"Electrical IV","Motors, three-phase and VFD fundamentals plus basic troubleshooting",
         ["DC motor fundamentals","Three-phase motor fundamentals","Motor protection and overloads","VFD fundamentals","Basic electrical troubleshooting"],
         ["Explain electrical-to-mechanical energy conversion in a small DC motor.","Interpret a sample three-phase nameplate at awareness level; do not wire mains equipment.","Separate short-circuit protection from overload protection.","Map VFD ready, run, speed reference, running and fault signals.","Create a source-to-load troubleshooting sequence for a motor-will-not-run symptom."],
         ["Explain motor-control layers","Describe VFD interfaces","Troubleshoot systematically"],
         "Simulate a motor/VFD interface using LEDs for Ready, Run and Fault, a jumper for Run command and a state table for speed reference. Inject missing-ready and overload-open faults; record diagnosis and recovery."),

    Week(5,"M2",1,"PLC I","PLC architecture, scan cycle, digital I/O, tags and Ladder basics",
         ["PLC architecture","PLC scan cycle","Digital inputs","Digital outputs","Tags and Ladder Logic fundamentals"],
         ["Draw power supply, CPU, DI, DO, communications and field devices.","Explain when an input change becomes visible to cyclic logic and the output update.","Trace a hobby button or jumper from field state to a PLC-style input tag.","Trace an output command through interface device to LED or motor representation.","Write and test a basic Start/Stop rung with named tags."],
         ["Draw PLC architecture","Explain the scan","Write basic rungs"],"Focus on Project 1 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 1"),
    Week(6,"M2",2,"PLC II","Core Ladder instructions, latching, timers, counters and one-shots",
         ["Contacts and coils","Seal-in and Set/Reset","On-delay and off-delay timers","Counters and comparisons","One-shots and edge detection"],
         ["Predict rung truth for series and parallel contacts.","Compare seal-in with Set/Reset and define safe reset behavior.","Create a delayed-start timing chart.","Build a count-to-five state table with reset.","Explain why a maintained sensor needs one-shot logic for one count per object."],
         ["Read rungs left to right","Use timers/counters","Control repeated events"],"Focus on Project 1 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 1"),
    Week(7,"M2",3,"PLC III","Modes, command ownership, permissives and interlocks",
         ["Permissives","Interlocks","Auto/Manual control","Local/Remote ownership","Command versus feedback"],
         ["Write the Boolean conditions required before a motor may start.","Explain how an interlock removes or prevents an unsafe command.","Define what the operator may command in Manual versus Auto.","Create an ownership table for Local and Remote modes.","Design a timer that alarms when RunCmd is true but RunFb remains false."],
         ["Separate permissive/interlock roles","Define mode ownership","Detect command-feedback mismatch"],"Focus on Project 1 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 1"),
    Week(8,"M2",4,"PLC IV","Sequencing, transitions, controlled restart and recovery",
         ["Sequence requirements","Steps and transitions","State-machine fundamentals","Pause, abort and reset","Power-loss and restart behavior"],
         ["Convert a conveyor description into numbered steps.","Define measurable transition conditions between three steps.","Draw a state diagram including Idle, Running, Complete and Faulted.","Specify pause, abort and reset behavior without skipping prerequisites.","Decide what state must occur after power restoration and justify it."],
         ["Design ordered sequences","Define transitions","Control recovery"],"Focus on Project 1 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 1"),
    Week(9,"M2",5,"PLC V","Fault handling, alarms, trips, acknowledgement and diagnostics",
         ["Fault detection","Alarm versus trip","Acknowledgement versus reset","First-out and fault memory","PLC troubleshooting workflow"],
         ["Define five detectable conveyor faults and their evidence.","Classify warning, alarm and trip responses.","Create an acknowledgement/reset state table.","Preserve the first cause when several conditions follow a trip.","Trace field device, wiring, I/O, logic, HMI and process layers before editing code."],
         ["Design useful diagnostics","Handle faults predictably","Troubleshoot by layer"],"Focus on Project 1 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 1"),
    Week(10,"M2",6,"PLC VI","Siemens fundamentals, online diagnostics and Rockwell awareness",
         ["TIA Portal project structure","S7-1200/S7-1500 fundamentals","Monitoring and diagnostic buffers","Backup and change control","Allen-Bradley/Rockwell awareness"],
         ["Identify hardware configuration, tags, blocks and watch tables in a TIA project.","Compare compact and modular PLC concepts without claiming hardware experience.","Interpret a simulated diagnostic event before changing logic.","Create a versioned backup and change note.","Translate Siemens tag/block terminology into introductory Logix concepts."],
         ["Navigate a vendor project","Use diagnostics first","Translate basic vendor concepts"],"Focus on Project 1 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 1"),

    Week(11,"M3",1,"Instrumentation I","Sensors, transmitters, digital/analog signals and 4-20 mA",
         ["Sensors and transducers","Transmitters","Digital instrument signals","Analog instrument signals","4-20 mA and live zero"],
         ["Trace a physical variable from sensor to displayed tag.","Explain why a transmitter standardizes the sensor response.","Create a fail-safe level-switch truth table.","Compare 0-10 V and 4-20 mA for noise and fault detection.","Calculate percent span at 4, 8, 12, 16 and 20 mA."],
         ["Trace the measurement chain","Distinguish signal types","Explain live zero"],"Focus on Project 2 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 2"),
    Week(12,"M3",2,"Instrumentation II","Temperature measurement, selection, scaling and faults",
         ["Temperature and units","RTD fundamentals","Thermocouple fundamentals","Temperature transmitters and scaling","Temperature faults and calibration checks"],
         ["Convert between degrees C and K and define the measured range.","Explain RTD resistance change and 2/3/4-wire lead effects.","Explain thermocouple millivolts and cold-junction awareness.","Scale 4-20 mA to 0-100 degrees C.","Distinguish open sensor, wrong type, wiring error and actual process change."],
         ["Compare temperature technologies","Scale a signal","Diagnose measurement faults"],"Focus on Project 2 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 2"),
    Week(13,"M3",3,"Instrumentation III","Pressure and level measurement",
         ["Pressure fundamentals","Pressure transmitter selection","Level measurement technologies","Level scaling and independent switches","Pressure/level troubleshooting"],
         ["Differentiate gauge, absolute and differential pressure.","Select a range and wetted-material assumptions for a small water system.","Compare float, ultrasonic, hydrostatic and simulated level measurement.","Scale a level input and define low-low/high-high switches.","Separate process, installation, wiring, configuration and device causes."],
         ["Explain pressure reference","Select level methods","Troubleshoot by cause category"],"Focus on Project 2 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 2"),
    Week(14,"M3",4,"Instrumentation IV","Flow, calibration, valves, actuators and HART awareness",
         ["Flow measurement fundamentals","Flow sensor signals and scaling","Calibration fundamentals","Control valves and actuators","HART fundamentals"],
         ["Compare pulse, switch and analog flow signals.","Convert pulse frequency or 4-20 mA into engineering units.","Prepare three-point as-found/as-left records using simulation.","Define valve command, position feedback, fail position and travel fault.","Explain how HART information coexists with a 4-20 mA signal at awareness level."],
         ["Scale flow signals","Record calibration evidence","Explain final elements and HART"],"Focus on Project 2 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 2"),

    Week(15,"M4",1,"Process Control I","Process variables, PV/SP/MV, feedback and Manual/Automatic control",
         ["Process variables","PV and SP","Manipulated variable and disturbances","Feedback control loops","Manual and Automatic control"],
         ["Identify controlled, measured and manipulated variables for a tank.","Calculate SP-PV error and state the assumed control direction.","Separate controller output from process response and disturbances.","Draw process-sensor-controller-actuator feedback.","Design a bumpless Manual-to-Auto transfer check at fundamentals level."],
         ["Label loop variables","Explain feedback","Compare Manual/Auto"],"Focus on Project 2 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 2"),
    Week(16,"M4",2,"Process Control II","PID fundamentals, alarms, permissives, interlocks and ESD concepts",
         ["Proportional action","Integral and derivative awareness","Process response and PID trends","Alarm design and deadband","Interlocks, permissives, trips and ESD concepts"],
         ["Predict the directional effect of increasing proportional action.","Explain integral removal of offset and why derivative reacts to rate of change.","Classify stable, slow, overshooting, oscillating and saturated trends.","Create alarm priority, deadband and operator-response entries.","Build a cause/effect row for high-high level trip and safe recovery."],
         ["Explain PID terms","Interpret trends","Design protective responses"],"Focus on Project 2 only for 4 hours. Choose the next incomplete project section from your own design/build plan; no separate Saturday laboratory.","Project 2"),

    Week(17,"M5",1,"SCADA/HMI I","HMI/SCADA fundamentals, visualization, hierarchy and PLC communications",
         ["HMI versus SCADA","Process visualization principles","Screen hierarchy and navigation","Equipment faceplates","PLC communications and command ownership"],
         ["Compare local HMI and supervisory SCADA roles.","Redesign a cluttered screen using neutral normal states.","Create overview, area, equipment, alarm and trend navigation.","Design a pump faceplate showing command, mode, feedback, permissives and fault.","Trace an HMI command through communications and PLC ownership logic."],
         ["Create screen hierarchy","Show state and ownership","Trace communications"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),
    Week(18,"M5",2,"SCADA/HMI II","Alarm management, trends, history, historian concepts and Ignition",
         ["Alarm philosophy","Alarm priorities and acknowledgement","Trends","Historical data and historian concepts","Ignition fundamentals"],
         ["Separate alarm condition, priority, message, response and shelving awareness.","Explain acknowledge versus return-to-normal and avoid nuisance alarms.","Select pens, scales and time windows for a tank diagnostic trend.","Distinguish live, historical, stale and bad-quality data.","Build or plan an Ignition tag, alarm, trend and Perspective view workflow."],
         ["Design useful alarms","Interpret trends/history","Navigate Ignition fundamentals"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),

    Week(19,"M6",1,"Networking I","Ethernet, topology, IP addressing, subnetting and TCP/IP",
         ["Ethernet fundamentals","Industrial network topology","IPv4 addressing","Subnet masks and gateways","TCP/IP, ports and ping"],
         ["Draw PLC, HMI, SCADA and device Ethernet links.","Compare a star topology with a small redundant concept at awareness level.","Assign unique addresses and create an IP schedule.","Determine whether two /24 addresses are local peers.","Explain why ping success does not prove an application service is healthy."],
         ["Draw network topology","Create an IP plan","Troubleshoot by layer"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),
    Week(20,"M6",2,"Networking II","Modbus, OPC UA, serial communications, Profinet and troubleshooting",
         ["Modbus TCP fundamentals","Modbus RTU and serial settings","OPC UA fundamentals","Profinet awareness","Industrial network troubleshooting"],
         ["Map device ID, function, register, datatype and byte order.","Match baud, parity, stop bits, node address and termination.","Explain OPC UA client/server, tags and quality at fundamentals level.","Compare Profinet device naming and IP awareness with ordinary Ethernet.","Diagnose link, address, transport, protocol, mapping and application layers in order."],
         ["Explain common protocols","Record serial settings","Diagnose network faults"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),

    Week(21,"M7",1,"Documentation I","P&IDs, schematics, wiring/loop diagrams and registers",
         ["P&IDs","Electrical schematics","Wiring diagrams","Instrument loop diagrams","I/O and instrument lists"],
         ["Trace equipment, piping, valves and an instrument loop on a tank P&ID.","Trace protection, command, coil and feedback on a motor schematic.","Create terminal-to-terminal wiring for a simulated transmitter.","Draw process-to-HMI loop boundaries and safe verification points.","Coordinate tags, ranges, addresses, normal/fail states and descriptions."],
         ["Trace drawings","Coordinate tags","Build usable registers"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),
    Week(22,"M7",2,"Documentation II","Narratives, matrices, alarm/network documents and technician reports",
         ["Control narratives","Sequence descriptions","Cause/effect and trip/interlock matrices","Alarm lists and network diagrams","Test procedures and troubleshooting reports"],
         ["Write purpose, modes, sequence, protections and recovery in a control narrative.","Define steps and transitions without ambiguous words.","Create traceable cause/effect and trip/interlock rows.","Coordinate alarm tags with a labelled network drawing.","Write expected result, actual result, evidence, defect and retest fields."],
         ["Write maintainable documents","Create traceable matrices","Report troubleshooting clearly"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),

    Week(23,"M8",1,"Safety Awareness","LOTO, permits, electrical hazards, emergency stops and ESD concepts",
         ["Industrial hazard identification","Lockout/Tagout awareness","Permit-to-work awareness","Electrical safety and test-before-touch","Emergency-stop, ESD and hazardous-area awareness"],
         ["Identify electrical, stored-energy, rotating, pressure and water/electronics hazards.","Explain isolation, lock, tag, verification and authorization boundaries.","List permit purpose, limits, responsible people and close-out.","Create a safe test plan for a low-voltage trainer and state stop-work triggers.","Differentiate a training E-stop input from a certified safety function."],
         ["Identify hazards","Respect authorization limits","Classify protective functions"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),
    Week(24,"M8",2,"Commissioning","Pre-commissioning, I/O checks, loop checks, FAT/SAT and punch lists",
         ["Commissioning planning","Visual and cold checks","I/O and loop checks","FAT/SAT-style testing","Defects, punch lists and controlled restoration"],
         ["Define scope, roles, prerequisites, hold points and safe boundaries.","Inspect labels, polarity, protection, termination and document revision before power.","Prove input stimulus, PLC state, output command, feedback and HMI indication.","Separate factory-style and site-style acceptance evidence for a home simulation.","Classify, correct, retest and close defects with traceability."],
         ["Plan commissioning","Execute traceable checks","Control defects and restoration"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),
    Week(25,"M8",3,"Integrated Troubleshooting and Handover","Structured fault-finding, regression, demonstration and release",
         ["Symptom-to-root-cause method","Electrical and I/O fault isolation","Instrument/process fault isolation","HMI/network fault isolation","Regression, handover and technical demonstration"],
         ["Use symptom, checks, evidence, isolation, diagnosis, correction and verification in order.","Trace source, protection, field input, I/O, logic, interface and output.","Separate bad measurement from real process change.","Diagnose quality, connectivity, address, protocol, tag mapping and ownership.","Run regression, back up files and explain the flagship project in 5-10 minutes."],
         ["Troubleshoot systematically","Verify correction","Deliver an honest evidence pack"],"Focus on Project 3 only for 4 hours. Choose the next incomplete flagship-project section from your own design/build plan; no separate Saturday laboratory.","Project 3"),
]


@dataclass
class Module:
    code: str
    title: str
    level: str
    weeks: list[int]
    purpose: str
    activities: list[str]
    case_title: str
    situation: str
    evidence: list[str]
    tasks: list[str]


MODULES = [
    Module("M1","Electrical Fundamentals","Fundamentals",[1,2,3,4],"Develop safe low-voltage circuit reasoning, measurement habits, component recognition, schematic tracing and motor/VFD awareness before PLC work.",["Calculate and annotate DC circuits","Build breadboard LED/resistor circuits","Trace relay/contactor control paths","Simulate motor/VFD interfaces and faults"],"Conveyor motor indication will not start","The low-voltage trainer has a Start request, but the motor indicator remains off. Supply polarity, Stop state, overload representation, holding path and output interface must be checked without guessing.",["Schematic","Expected voltages/states","Measurement or simulation observations","Corrected fault record"],["Trace source to load","Identify the first abnormal boundary","State the safest confirming check","Verify normal, fault and recovery behavior"]),
    Module("M2","PLC & Automation","Developing",[5,6,7,8,9,10],"Build PLC architecture, Ladder Logic, sequencing, mode control, protection, diagnostics and introductory Siemens/Rockwell awareness around Project 1.",["Create I/O and tag lists","Write and comment Ladder patterns","Build modes, permissives and interlocks","Run fault and recovery checks"],"Conveyor stops during transfer","The sequence is active, safety and overload conditions are healthy, but downstream-ready is false. The learner must distinguish field input, wiring, I/O, tag, logic and sequence causes.",["I/O state table","Logic screenshot","Sequence state","Fault timeline"],["Confirm the active step","Trace downstream-ready end to end","Explain why code edits are not first","Retest after correction"]),
    Module("M3","Instrumentation","Developing",[11,12,13,14],"Understand measurement chains, common process measurements, signal types, 4-20 mA, scaling, calibration records, valves and HART fundamentals.",["Build signal-chain drawings","Calculate percent/current/engineering units","Compare sensor technologies","Prepare calibration and loop-check sheets"],"Level indication is wrong after replacement","A replacement level device is healthy but the displayed value is consistently incorrect. The configured range does not match the documented device range.",["Device/simulated range","Raw signal","PLC scaling","Displayed value and quality"],["Calculate the expected value","Identify configuration versus calibration","Correct the documented parameter","Verify low, midpoint and high points"]),
    Module("M4","Process Control","Fundamentals",[15,16],"Connect measurement, control logic and final elements through PV, SP, MV, feedback, Manual/Auto, PID, alarms and protective concepts.",["Draw feedback loops","Interpret response trends","Write alarm responses","Create cause/effect rows"],"Tank approaches high-high level","The level PV rises while the normal control output is saturated. High-high protection must act independently of routine control and recovery must require a healthy condition.",["PV/SP/MV trend","Alarm/trip state","Permissive/interlock state","Actuator command and feedback"],["Separate control failure from protection","Define safe cause/effect","State operator information","Prove recovery cannot bypass the trip"]),
    Module("M5","SCADA / HMI","Developing",[17,18],"Create operator displays that communicate state, ownership, alarm, quality, history and process response without hiding PLC authority.",["Design hierarchy and faceplates","Configure or simulate tags","Build alarms and trends","Test stale/bad-quality behavior"],"A normal-looking level remains after communications fail","The screen continues showing the last plausible value even though the controller connection has failed. The operator cannot distinguish live from stale data.",["Tag quality","Timestamp","Communication state","Alarm and display behavior"],["Identify the misleading presentation","Design bad-quality behavior","Prevent unsafe command assumptions","Verify loss and recovery"]),
    Module("M6","Industrial Networking","Working knowledge",[19,20],"Develop Ethernet, addressing, protocol and layered troubleshooting skills for PLC/HMI/SCADA communications.",["Create topology and IP schedules","Document serial settings","Map Modbus/OPC data","Inject safe communication faults"],"HMI stopped communicating after maintenance","The physical link is present, but the HMI cannot read the controller after an address change. The learner must test physical, addressing, transport, protocol and application layers.",["Link state","IP/subnet results","Port/service state","Driver and tag diagnostics"],["Start at the physical layer","Confirm unique compatible addresses","Check service/protocol mapping","Document correction and reconnection"]),
    Module("M7","Engineering Documentation","Developing",[21,22],"Produce coordinated drawings, registers, narratives, matrices, test procedures and fault reports that another technician can follow.",["Create a P&ID and schematics","Coordinate I/O/instrument lists","Write narratives and matrices","Cross-check documents against logic"],"Pump-skid modification has conflicting documents","The P&ID, I/O list, PLC tag and HMI label use different identifiers for the same device after a change.",["Document revisions","Tag cross-reference","PLC/HMI evidence","Approved change note"],["Identify the controlling baseline","Resolve every mismatch","Update affected documents","Record verification and limitations"]),
    Module("M8","Safety Awareness, Commissioning & Troubleshooting","Fundamentals with integration",[23,24,25],"Apply safety boundaries, commissioning discipline, FAT/SAT-style checks and structured fault-finding to the Project 3 flagship simulator.",["Prepare hazard and boundary notes","Execute I/O/loop checks","Manage punch items","Run integrated faults and regression"],"Instrument fault during simulated operation","A process value suddenly becomes implausible while the pump is commanded. The learner must protect the simulated process, distinguish real change from measurement failure and restore only after verification.",["Alarm/trip chronology","Raw and engineering values","I/O/loop checks","Correction and regression results"],["State the safe immediate response","Trace sensor to HMI","Diagnose without bypassing protection","Verify restoration and document the lesson"]),
]


def week_dates(num):
    monday = date(2026, 9, 7) + timedelta(days=7 * (num - 1))
    return monday, monday + timedelta(days=6)


def module_dates(module):
    a, _ = week_dates(module.weeks[0])
    _, b = week_dates(module.weeks[-1])
    return f"{a.strftime('%d %b %Y')} - {b.strftime('%d %b %Y')}"


def build_syllabus():
    doc = CollegeDoc(SYLLABUS_PATH, "Junior Automation & Controls Technician Syllabus - College Edition", "COLLEGE EDITION SYLLABUS")
    story = cover("Junior Automation & Controls Technician", "College Edition Competency Syllabus - Eight Integrated Modules",
                  [("PROGRAMME WINDOW","7 September 2026 - 28 February 2027"),("CORE LOAD","25 weeks | 19 hours/week | approximately 475 hours"),("WEEKLY RHYTHM","Monday-Friday study | Saturday laboratory or active project"),("PORTFOLIO","Exactly three progressive low-voltage projects")],
                  "A structured path from electrical fundamentals through PLCs, instrumentation, process control, SCADA, networking, troubleshooting, commissioning and engineering documentation.")
    story += [PageBreak(), P("Course overview", "h1"), P("This personal programme supports entry-level Junior Automation Technician, Junior Controls Technician, PLC Technician, Instrumentation & Controls Technician and E&I Technician roles. It combines theory, worked applications, simulation, safe hobby-scale physical work and three substantial portfolio projects."),
              box("Learning principle", "Study for usable understanding, not for a Sunday score. Weekday retrieval and application strengthen memory in context; Saturday proves the week's learning through an accurate laboratory or advances the active portfolio project. Sunday is optional light consolidation or rest."),
              P("Fixed learning rhythm", "h2"),
              table(["Day","Duration","Purpose"],[("Monday-Friday","3 h/day","One topic per day: retrieval, focused learning, worked examples, application, error log and next action."),("Saturday","4 h","Weeks 1-4: topic-matched laboratory. Weeks 5-25: active project only; no separate laboratory."),("Sunday","Optional 30-60 min","Light review, filing or preview only. No test, score, submission deadline or new topic.")],[38*mm,34*mm,104*mm],7.7,9.5),
              P("Programme outcomes", "h2")]
    story += checklist(["Trace an electrical or instrument signal from process/field device through wiring, I/O, PLC logic, HMI and actuator.","Create and troubleshoot maintainable Ladder Logic with modes, sequences, permissives, interlocks and recoverable faults.","Explain and simulate analog instrumentation, 4-20 mA, scaling, calibration, PV/SP/feedback and PID fundamentals.","Create HMI/SCADA screens, alarm/trend evidence and basic Ethernet/Modbus/OPC UA diagnostics.","Produce coordinated P&IDs, schematics, loop drawings, registers, narratives, matrices, test sheets and reports.","Work honestly within low-voltage DIY/simulation boundaries and distinguish training evidence from industrial authorization."])
    story += [PageBreak(), P("Curriculum map and workload", "h1")]
    rows=[]
    for m in MODULES:
        rows.append((m.code,m.title,module_dates(m),m.level,f"{len(m.weeks)*19} h"))
    story += [table(["Module","Title","Dates","Target","Core hours"],rows,[15*mm,62*mm,43*mm,37*mm,19*mm],6.9,8.5),Spacer(1,6),
              box("Portfolio windows", "Project 1: 5 Oct-15 Nov 2026. Project 2: 16 Nov-27 Dec 2026. Project 3 flagship: 28 Dec 2026-28 Feb 2027. During these windows, Saturday is reserved entirely for the active project."),
              P("Skill coverage", "h2"),
              two_col("Technical",["Electrical and motor control","PLC architecture and programming","Instrumentation and 4-20 mA","Process control and PID","HMI/SCADA and historian","Ethernet and industrial protocols"],"Technician practice",["Schematics and P&IDs","I/O and loop checks","Fault isolation","FAT/SAT-style testing","Change and evidence control","Safe-work awareness"]),
              PageBreak(), P("Learning, submission and evidence policies", "h1"),
              two_col("Evidence labels",["Studied - explain in own words","Simulated - software/hobby model","Implemented - built/configured","Tested - expected versus actual","Documented - revision controlled","Industrial claim - never implied"],"File discipline",["Project-document-revision names","One evidence index per project","Keep source and exported PDF","Record software/version used","Mark unperformed work NOT TESTED","Back up before major changes"]),
              P("Daily comprehension approach", "h2"), P("Retrieval is brief and low-stakes: explain yesterday's idea, then use the answer immediately. Worked examples, application problems and error correction are learning activities, not examinations."),
              P("Saturday rule", "h2"), P("Weeks 1-4 use only the laboratory printed for that week. From Week 5 onward, do not add a separate laboratory: focus on the active project for the full four hours and choose the next incomplete section from your own design and build plan."),
              P("Sunday boundary", "h2"), P("Sunday may be rest or 30-60 minutes of light review, file organization, error-log review and preview. There is no Sunday test, formal assessment, homework submission or new topic."),
              box("Safety and honesty", "Keep physical work at safe low voltage. Hobby components and DIY structures may represent industrial functions, but do not DIY mains, safety-critical, pressure-rated or hazardous-area equipment. State what is real, DIY-built, simulated or software-based.", True)]

    for m in MODULES:
        story += [PageBreak(), P(f"{m.code} - {m.title}", "h1"),
                  table(["TARGET LEVEL","DATES","PLANNED CORE LOAD"],[(m.level,module_dates(m),f"{len(m.weeks)*19} hours")],[52*mm,70*mm,54*mm],7.6,9.2),
                  box("Module purpose", m.purpose), P("Module competencies", "h2")]
        all_out=[]
        for n in m.weeks:
            all_out.extend(next(w.outcomes for w in WEEKS if w.num==n))
        story += checklist(all_out[:8])
        story += [P("Module activities", "h2")]+checklist(m.activities)
        week_rows=[]
        for n in m.weeks:
            w=next(x for x in WEEKS if x.num==n); a,b=week_dates(n)
            week_rows.append((f"Week {n}",f"{a.strftime('%d %b')} - {b.strftime('%d %b')}",w.theme,w.scope))
        story += [P("Weekly sequence", "h2"), table(["Programme week","Dates","Theme","Primary scope"],week_rows,[27*mm,32*mm,38*mm,79*mm],6.9,8.4)]

        for n in m.weeks:
            w=next(x for x in WEEKS if x.num==n); monday,sunday=week_dates(n)
            portfolio = f"{w.project} active - Saturday is project focus only" if w.project else "Not active - Saturday uses the week's laboratory"
            story += [PageBreak(), P(f"{m.code} Module Week {w.module_week} - Programme Week {w.num}", "h1"),
                      table(["WEEKLY FOCUS",""],[("Dates",f"{monday.strftime('%d %b')} - {sunday.strftime('%d %b %Y')}"),("Theme",w.theme),("Primary scope",w.scope),("Portfolio window",portfolio)],[40*mm,136*mm],7.2,8.8),
                      P("Weekly learning outcomes", "h2")]
            story += checklist(w.outcomes,"small")
            rows=[]
            for i,(topic,app) in enumerate(zip(w.topics,w.applications)):
                d=monday+timedelta(days=i)
                rows.append((d.strftime("%a\n%d %b"),"3 h",topic,f"Study focus: {topic}. Application: {app}"))
            if w.project:
                sat_mode=f"{w.project} focus"
            else:
                sat_mode="Weekly laboratory"
            rows.append(((monday+timedelta(days=5)).strftime("%a\n%d %b"),"4 h",sat_mode,w.saturday))
            rows.append((sunday.strftime("%a\n%d %b"),"Optional\n30-60 min","Light consolidation or rest","No test and no new topic. If useful, review the error log, organize evidence and preview Monday; otherwise rest."))
            story += [P("Monday-Sunday execution plan", "h2"), table(["Day","Time","Mode","Required study and application"],rows,[18*mm,18*mm,35*mm,105*mm],6.7,8.2),Spacer(1,5),
                      box("Session structure", "Monday-Friday: 15 min retrieval, 65 min focused learning, 10 min break, 45 min worked examples, 10 min break, 25 min application, 10 min error log and next action. Saturday: 4 hours using the laboratory or active-project rule shown above.")]

        story += [PageBreak(), P(f"{m.code} applied technician case study", "h1"), P(m.case_title, "h2"), box("Situation", m.situation, True),
                  P("Available evidence", "h2")]+checklist(m.evidence)
        story += [P("Technician reasoning tasks", "h2")]+checklist(m.tasks)
        story += [P("Required case-study record", "h2"), table(["Record section","What to capture"],[("Symptom","Observable behavior without premature diagnosis"),("Initial checks","Safe, non-invasive checks in logical order"),("Evidence","Readings, states, screenshots or traces"),("Isolation","Boundary where expected and actual first differ"),("Root cause","Verified cause, not a guess"),("Correction and verification","Controlled change, normal/fault/recovery retest and limitation")],[43*mm,133*mm],7.4,9.2),Spacer(1,7),box("Learning use", "This case study is an applied comprehension activity, not an examination. Use references, correct misconceptions and preserve the reasoning trail.")]

    story += [PageBreak(), P("Programme completion standard", "h1"), P("Treat the syllabus as complete when the following can be demonstrated honestly through simulation, safe hobby-scale hardware and documented project evidence."),
              two_col("Technical capability",["Trace electrical and control paths","Write/test Ladder Logic","Scale and diagnose analog signals","Explain PV/SP/PID fundamentals","Build HMI alarms and trends","Diagnose basic network faults"],"Professional evidence",["Exactly three integrated projects","Coordinated engineering documents","Normal/fault/recovery results","Structured troubleshooting reports","FAT/SAT-style records","Clear real/simulated/DIY labels"]),
              Spacer(1,7), box("Final standard", "Competence is shown by reasoning, working behavior, traceability and honest limitations. The programme contains no Sunday examinations; readiness grows through repeated application, project work and corrected evidence.", True)]
    doc.build(story)
    return SYLLABUS_PATH


def build_guide():
    doc=CollegeDoc(GUIDE_PATH,"Junior Automation & Controls Technician Study Guide - College Edition","COLLEGE EDITION STUDY GUIDE")
    story=cover("Junior Automation & Controls Technician","Daily Study Guide - 7 September 2026 to 28 February 2027",
                [("PROGRAMME WINDOW","7 September 2026 - 28 February 2027"),("WEEKDAY SESSION","3 hours | one topic per day"),("SATURDAY SESSION","4 hours | weekly laboratory or active project"),("SUNDAY","Optional 30-60 minute light review or rest")],
                "The guide and syllabus use the same 25 weeks, topics and project windows. There are no Sunday tests or examination-driven study sessions.")
    story += [PageBreak(),P("How to use this guide","h1"),P("Open the matching syllabus week. Study only the named topic for that weekday. Complete the specific application, record errors as useful feedback and write the next action before stopping."),
              box("One-topic rule","If a topic is unfinished after three focused hours, record the stopping point and continue it in the next available study block. Do not compress several unfinished topics into one session."),
              P("Three-hour weekday structure","h2"),
              table(["Block","Time","Purpose"],[("Retrieval","15 min","Explain the last relevant idea without scoring yourself."),("Focused learning","65 min","Read/watch, define terms and work through the core concept."),("Break","10 min","Leave the workspace."),("Worked examples","45 min","Calculate, trace, program or interpret with references."),("Break","10 min","Reset attention."),("Application","25 min","Complete the syllabus problem independently, then correct it."),("Error log + next action","10 min","Record misconception, correction, evidence file and next step.")],[38*mm,25*mm,113*mm],7.6,9.4),
              P("Saturday structures","h2"),
              table(["Week type","Four-hour allocation"],[("Weeks 1-4 laboratory","15 min recall/safety | 75 min prepare/build | 15 min break | 90 min measure/test | 15 min break | 20 min evidence | 10 min error log/next action"),("Weeks 5-25 active project","20 min choose scope/acceptance criteria | 100 min build | 15 min break | 70 min test/debug | 15 min break | 20 min evidence and next action")],[48*mm,128*mm],7.5,9.3),
              PageBreak(),P("Learning, reflection and evidence cycle","h1"),
              two_col("During the week",["One topic per weekday","Brief retrieval without scoring","Worked examples with references","Independent application","Correct errors immediately","Save one useful artifact"],"Sunday option",["Rest is acceptable","Review error log if helpful","Organize files/evidence","Preview Monday briefly","No test or score","No new topic or submission"]),
              P("Portfolio coordination","h2"),
              table(["Weeks","Saturday mode","Active work"],[("1-4","Weekly laboratory","Only the laboratory matched to that week's electrical topics"),("5-10","Project focus","Project 1 - Industrial Motor & Conveyor Control System"),("11-16","Project focus","Project 2 - Automated Process & Instrumentation System"),("17-25","Project focus","Project 3 - Integrated Remote/Offshore Process Control Simulator")],[30*mm,43*mm,103*mm],7.6,9.3),
              box("No extra Saturday laboratory", "When a project window is active, the project itself is the practical work. Do not add a separate generic laboratory. Choose the next incomplete section from your own project plan and use the full four hours on it.",True)]

    for w in WEEKS:
        monday,sunday=week_dates(w.num)
        portfolio=f"{w.project} active - project focus only" if w.project else "Not active - use the topic-matched laboratory"
        story += [PageBreak(),P(f"Week {w.num}: {monday.strftime('%d %b')} - {sunday.strftime('%d %b %Y')}","h1"),
                  table(["WEEKLY FOCUS",""],[("Theme",w.theme),("Primary scope",w.scope),("Linked syllabus",w.module),("Saturday",portfolio)],[38*mm,138*mm],7.3,9.0),
                  P("Weekly learning outcomes","h2")]+checklist(w.outcomes,"small")
        rows=[]
        for i,(topic,app) in enumerate(zip(w.topics,w.applications)):
            d=monday+timedelta(days=i)
            rows.append((d.strftime("%a\n%d %b"),"3 h",topic,f"Use the standard 3-hour structure. Complete this application: {app}"))
        rows.append(((monday+timedelta(days=5)).strftime("Sat\n%d %b"),"4 h",f"{w.project} focus" if w.project else "Weekly laboratory",w.saturday))
        rows.append((sunday.strftime("Sun\n%d %b"),"Optional\n30-60 min","Light review or rest","No test, score, homework submission or new topic. Optionally review the error log, organize evidence and preview Monday."))
        story += [table(["Date","Time","Focus","Specific assignment"],rows,[18*mm,18*mm,40*mm,100*mm],6.7,8.25),Spacer(1,5),
                  two_col("Evidence to keep",["Five weekday applications","Corrections/error log","Saturday lab or project evidence","Expected versus actual results"],"End-of-week reflection",["What became clearer?","What remains uncertain?","What evidence is strongest?","What is the next action?"])]

    story += [PageBreak(),P("Three-project Saturday roadmap","h1"),P("This table coordinates the study guide with the revised portfolio. It does not prescribe your design; it protects the full Saturday block for your own project decisions."),
              table(["Project","Dates","Programme weeks","Saturday instruction"],[("Project 1 - Motor & Conveyor","5 Oct-15 Nov 2026","5-10","Focus on Project 1 only for four hours; no separate laboratory."),("Project 2 - Process & Instrumentation","16 Nov-27 Dec 2026","11-16","Focus on Project 2 only for four hours; no separate laboratory."),("Project 3 - Integrated Flagship","28 Dec 2026-28 Feb 2027","17-25","Focus on Project 3 only for four hours; no separate laboratory.")],[43*mm,39*mm,28*mm,66*mm],7.3,9.1),
              P("Project-session record","h2"),
              table(["Field","Record"],[("Chosen scope","____________________________________________________________"),("Acceptance criteria","____________________________________________________________"),("Work completed","____________________________________________________________"),("Expected/actual","____________________________________________________________"),("Faults/corrections","____________________________________________________________"),("Evidence saved","____________________________________________________________"),("Next action","____________________________________________________________")],[45*mm,131*mm],7.4,10),
              PageBreak(),P("Weekly record - print or duplicate","h1")]
    fields=["Week and dates","Syllabus module","Five topics completed","Hours planned/completed","Main concept learned","Application evidence","Saturday lab/project result","Error corrected","Evidence location","Next action"]
    story += [table(["Record field","Entry"],[(x,"____________________________________________________________") for x in fields],[48*mm,128*mm],7.5,10),Spacer(1,7),box("Recovery rule","Resume the next unfinished prerequisite. Do not double the following week or convert Sunday into a compulsory catch-up day. Reduce project scope before reducing safety, testing or documentation.",True),
              PageBreak(),P("Final readiness checklist","h1"),
              two_col("Knowledge and practice",["Electrical quantities and schematics","Motor/control circuits","PLC scan, I/O and Ladder","Modes/sequences/faults","Instrumentation and scaling","Process control and PID","HMI/SCADA and networking","Commissioning/troubleshooting"],"Evidence and conduct",["Exactly three project folders","DIY/simulation labels accurate","Normal/fault/recovery evidence","Drawings/tags/logic agree","Test procedures completed","Fault reports explain reasoning","Backups and revisions controlled","5-10 minute flagship demo"]),
              Spacer(1,7),box("Readiness principle","You are ready to apply when you can explain and demonstrate the work honestly, follow a signal end to end, diagnose faults methodically and show traceable evidence. No Sunday examination is required.")]
    doc.build(story)
    return GUIDE_PATH


def project_cover(title, window, subtitle):
    return [P(title,"h1"),table(["BUILD WINDOW","PROJECT LABEL"],[(window,"Low-voltage DIY / Simulation Training Project")],[88*mm,88*mm],7.6,9.3),Spacer(1,6),box("Project brief",subtitle)]


def build_portfolio():
    doc=CollegeDoc(PORTFOLIO_PATH,"Junior Automation & Controls Technician Portfolio Projects - College Edition","COLLEGE EDITION PORTFOLIO")
    story=cover("Junior Automation & Controls Technician","Three-Project Portfolio Roadmap - DIY Low-Voltage College Edition",
                [("PROGRAMME WINDOW","7 September 2026 - 28 February 2027"),("PORTFOLIO","Exactly three substantial progressive projects"),("BUILD MODEL","One evolving low-voltage DIY training rig"),("TARGET ROLES","Junior automation, controls, PLC, instrumentation and E&I technician")],
                "Prove competence through requirements, design, safe construction, logic, testing, troubleshooting, commissioning evidence and honest technical explanation.")
    story += [PageBreak(),P("Role alignment and project progression","h1"),P("The portfolio is designed for Junior Automation Technician, Junior Controls Technician, Automation & Controls Technician, Instrumentation & Controls Technician, PLC Technician, E&I Technician and related entry-level roles."),
              table(["Project","Technical progression","Build window"],[("1 - Industrial Motor & Conveyor","Electrical fundamentals -> field inputs -> PLC logic -> motor/output control","5 Oct-15 Nov 2026"),("2 - Automated Process & Instrumentation","PLC -> instruments/signals -> sequencing -> process control -> actuators","16 Nov-27 Dec 2026"),("3 - Integrated Remote/Offshore Simulator","Integrated PLC -> HMI/SCADA -> networking -> faults -> commissioning","28 Dec 2026-28 Feb 2027")],[50*mm,87*mm,39*mm],7.4,9.1),
              Spacer(1,7),box("Only three projects","Do not split SCADA, networking, instrumentation, water treatment, troubleshooting or commissioning into extra standalone projects. They are integrated into Projects 2 and 3."),
              P("Single evolving rig","h2"),P("Project 1 establishes a reusable control station and conveyor representation. Project 2 reuses the control station and expands it with a DIY process/tank representation. Project 3 integrates and extends the same hardware and software into the flagship remote-process simulator."),
              PageBreak(),P("Implementation boundary and honest claims","h1"),
              two_col("Acceptable evidence",["Battery/USB low-voltage circuits","Breadboard and hobby components","DIY frames, tanks and brackets","PLC software simulation","Microcontroller physical emulator","Software-generated analog signals","Laptop HMI/SCADA","Safe open-circuit fault injection"],"Do not DIY",["Mains or three-phase wiring","VFD power circuits","Safety-rated E-stop/ESD systems","Pressure-rated vessels","Hazardous-area equipment","Protection relied on for people","Unenclosed mains power supplies","Claims of industrial/offshore experience"]),
              box("Required wording","Each project must state: This low-voltage DIY and software simulation represents industrial control behavior for training. It is not certified industrial, safety, hazardous-area or offshore equipment, and it does not represent site authorization.",True),
              P("Evidence labels","h2"),table(["Label","Meaning"],[("REAL HARDWARE","A physical low-voltage device actually used"),("DIY-BUILT","A learner-made structure, panel, bracket, tank or trainer"),("HOBBY COMPONENT","A low-cost device representing an industrial function"),("SIMULATED","Behavior produced in PLC/process/network software"),("NOT TESTED","Claim or condition not performed"),("CONCEPT ONLY","Awareness without implementation")],[40*mm,136*mm],7.5,9.2),
              PageBreak(),P("DIY-first evolving training rig","h1"),
              box("Starting inventory","Available now: breadboard, lamps/LEDs, resistors, wires and an alkaline battery. Confirm whether each lamp is an LED or bulb and its voltage/current before connection. Never connect an LED without a resistor or deliberately short the battery."),
              P("Buy only when the project requires it","h2"),
              table(["Priority","Low-cost item","Purpose and reuse"],[("1","One ESP32 or Arduino-compatible development board + USB cable","Optional physical I/O controller/emulator for all projects; do not call it an industrial PLC."),("2","4 pushbuttons or DIP switches; 2 x 10 kohm potentiometers","Start/Stop/sensors/modes plus simulated level, pressure, flow or speed."),("3","Logic-level MOSFET module + flyback diode","Interface a small DC motor or pump; never drive it directly from a controller pin."),("4","Small 3-6 V DC hobby motor","Optional moving conveyor evidence."),("5","Small low-voltage pump, tubing and temperature sensor","Optional Project 2 realism; LEDs/potentiometers remain acceptable substitutes."),("6","Digital multimeter","Safe low-voltage measurement learning; do not DIY the measuring instrument.")],[17*mm,63*mm,96*mm],7.1,8.8),
              P("Software path","h2"),P("Create industrial-style PLC logic in TIA Portal/PLCSIM if accessible, or another clearly identified IEC learning environment. A hobby controller may run the physical model separately. Project evidence must distinguish PLC simulation from microcontroller code. Use Ignition Maker or another personal learning HMI/SCADA platform when available."),
              PageBreak(),P("Portfolio governance and release rules","h1"),
              two_col("Every project begins with",["Problem statement and scope","Real/DIY/hobby/simulated boundary","Requirements and exclusions","Architecture and interfaces","Safety limits","Acceptance criteria","Versioned baseline"],"Every project ends with",["Normal/fault/recovery results","Defect closure and regression","As-built/source files","Evidence index and README","Technical demonstration","Limitations and next steps","Backed-up release"]),
              P("Common scoring rubric","h2"),table(["Category","Weight","Release question"],[("Requirements and design","15%","Is intended behavior explicit and traceable?"),("Technical implementation","25%","Does the safe model behave correctly and remain understandable?"),("Fault handling and safety","20%","Are abnormal states protected and recoverable within the training boundary?"),("Testing and evidence","20%","Do expected and actual results prove the claims?"),("Documentation","10%","Can another technician follow and maintain the work?"),("Demonstration","10%","Can decisions, faults and limitations be explained honestly?")],[55*mm,20*mm,101*mm],7.3,9),
              box("Release threshold","Target at least 75/100 with no category below 60%. Any uncorrected safety, ownership, stale-data or protective-response defect blocks release.",True)]

    # Project 1
    story += [PageBreak()]+project_cover("Project 1 - Industrial Motor & Conveyor Control System","5 October-15 November 2026","Build a small-scale, low-voltage industrial-style conveyor and motor-control system. The conveyor may be DIY-built from inexpensive materials; lamps/LEDs may represent actuators until a small motor is affordable.")
    story += [P("Required competence","h2")]+checklist(["Electrical fundamentals: voltage, current, resistance, Ohm's Law and power","DC circuits, relays/basic control paths and circuit-protection concepts","Motor control, digital inputs/outputs and sensor states","PLC architecture, Ladder Logic, latching, timers and counters","Auto/Manual, interlocks, permissives and controlled restart","Fault handling, emergency-stop concept and PLC/electrical troubleshooting"])
    story += [P("Foundation chain","h2"),box("Signal path","Electrical components -> wiring -> field inputs -> PLC -> Ladder Logic -> interface/output -> motor or process representation."),
              PageBreak(),P("Project 1 - DIY implementation and requirements","h1"),
              table(["Function","Low-cost implementation","Industrial meaning"],[("Conveyor structure","Cardboard/wood/plastic frame, bottle-cap rollers or static diagram","Material transport mechanism"),("Motor","LED first; optional small DC hobby motor through MOSFET/driver","Motor/contactor/VFD-controlled load"),("Object sensors","Jumpers/buttons; optional light or proximity hobby sensor","Photoelectric/proximity field inputs"),("Start/Stop/Reset","Jumpers or low-cost pushbuttons","Operator control station"),("Modes","DIP switches or jumpers","Auto/Manual and Local/Remote ownership"),("E-stop concept","Normally closed simulated input only","Training representation, never safety-rated"),("PLC","TIA/PLCSIM or declared IEC software; optional hobby controller for physical I/O","Industrial controller behavior")],[39*mm,68*mm,69*mm],7.0,8.6),
              P("Functional requirements","h2")]+checklist(["Start/Stop with seal-in and safe stopped default","Auto/Manual and Local/Remote ownership","Entry/exit object detection and count target","Run command, running feedback simulation and start-failure timer","Jam/missing-object fault, overload representation and reset after correction","Power-cycle/restart behavior that does not cause uncontrolled motion"])
    story += [PageBreak(),P("Project 1 - documentation, tests and evidence","h1"),
              two_col("Documentation",["Electrical/control schematic","Wiring diagram","PLC I/O and tag lists","Control narrative","Sequence description","Test procedure/results","Fault reports","Photos/video and code screenshots"],"Minimum faults",["Stop circuit open","Missing start permissive","Sensor stuck on/off","Run command without feedback","Overload/E-stop condition","Timer/counter defect","Incorrect I/O mapping","Power-cycle recovery"]),
              P("Acceptance demonstrations","h2")]+checklist(["Explain voltage/current path and calculate one real breadboard load","Trace Start from physical/simulated input through PLC logic to output","Run one complete manual and automatic cycle","Show permissive and interlock preventing startup","Inject a fault, diagnose by layer, correct it and verify recovery","Present the difference between hobby hardware and the industrial target design"])
    story += [box("Project 1 release","Release when electrical drawings, I/O, logic, actual behavior and fault evidence agree. The project establishes the reusable control foundation for Projects 2 and 3.",True)]

    # Project 2
    story += [PageBreak()]+project_cover("Project 2 - Automated Process & Instrumentation System","16 November-27 December 2026","Expand the Project 1 control foundation into a small low-voltage process: feed reservoir -> pump -> process tank -> controlled outlet/valve -> storage/output. DIY containers, tubing and supports are encouraged.")
    story += [P("Required competence","h2")]+checklist(["PLC automation with digital and analog I/O","Level and temperature measurement; flow where practical","Pressure concepts using simulation when necessary","Sensors, transmitters, 4-20 mA concepts, scaling and calibration fundamentals","Pump and valve/actuator control with sequencing","PV/SP/feedback and PID fundamentals","Manual/Automatic, alarms, interlocks, permissives and fault handling","Instrument troubleshooting and loop-check evidence"])
    story += [box("Measurement honesty","Industrial transmitters are not required. Potentiometers, inexpensive sensors, signal simulators and software values may represent 4-20 mA and process variables. Clearly label each measurement REAL HARDWARE, HOBBY COMPONENT or SIMULATED.")]
    story += [PageBreak(),P("Project 2 - DIY process and control implementation","h1"),
              table(["Process element","DIY / low-cost option","Required behavior"],[("Feed/process/storage tanks","Reused plastic bottles or containers in a leak tray","Visible process stages and safe containment"),("Pump","LED representation; optional small USB/low-voltage pump via driver","Command, feedback simulation, duty/fault response"),("Outlet valve","LED/servo representation or manual tubing clamp","Open/close command, position/failure concept"),("Level","Potentiometer plus independent jumper high/low switches","Continuous PV plus protective discrete limits"),("Temperature","Potentiometer first; optional low-cost sensor","Scaling, trend and alarm"),("Flow","Timed volume calculation, pulses from button or simulated value","Engineering-unit conversion and no-flow fault"),("Pressure","Software/potentiometer simulation","Range, scaling, abnormal-value and transmitter concepts")],[39*mm,67*mm,70*mm],6.9,8.5),
              P("Control requirements","h2")]+checklist(["Fill/transfer/drain sequence with explicit transitions","Manual/Automatic and safe command ownership","Low-low and high-high protection independent of routine control","Pump command/feedback discrepancy and no-flow detection","PV/SP display and basic closed-loop/PID simulation","Alarm deadband, acknowledgement, reset and recovery rules"])
    story += [PageBreak(),P("Project 2 - engineering documentation package","h1"),
              two_col("Design documents",["P&ID","Electrical/control schematic","Instrument and I/O lists","Instrument tags","Wiring/loop diagrams","Control narrative","Alarm list","Cause/effect matrix"],"Test evidence",["Calibration sheet","As-found/as-left values","Loop/I/O check sheets","Test procedure/results","Fault reports","Photos/videos","PLC/HMI evidence","Real/simulated register"]),
              P("Minimum instrument faults","h2")]+checklist(["Disconnected or forced-low signal","Abnormal analog value","Incorrect scaling range","Frozen/noisy value","Pump fails to start","Valve fails to move","Missing permissive","High-high trip and verified recovery"])
    story += [box("Project 2 release","Demonstrate the chain: process -> instrument -> signal -> PLC -> control logic -> actuator -> process response. Reuse the control foundation and prepare the process rig for Project 3.",True)]

    # Project 3
    story += [PageBreak()]+project_cover("Project 3 - Integrated Remote/Offshore Process Control Simulator","28 December 2026-28 February 2027","Flagship project: integrate and expand Projects 1 and 2 into a low-voltage training simulator inspired by remote/offshore process equipment. It is not an oil rig and must not imply certified offshore, hazardous-area or industrial authorization.")
    story += [P("Integrated process concept","h2"),box("Process chain","Feed -> pump -> process vessel -> instrumentation -> PLC/control -> separator/filter representation -> storage/output."),
              P("Flagship scope","h2")]+checklist(["PLC digital/analog I/O, sensors and simulated transmitters","4-20 mA concepts, scaling and validation","Pumps, motors, valves/actuators and process sequencing","Manual/Automatic, interlocks, permissives, trips and ESD concepts","Alarms, HMI, SCADA, trends and history","PLC/HMI communications, Ethernet and network diagnostics","Commissioning, FAT/SAT-style testing and structured fault-finding"])
    story += [PageBreak(),P("Project 3 - integrated architecture","h1"),
              table(["Layer","Reused/expanded implementation","Evidence"],[("Physical process","Project 1 conveyor/motor representation plus Project 2 tank/process rig","Photos, labels, limitations and process diagram"),("Field devices","Buttons, jumpers, pots, hobby sensors and software values","Real/simulated register and loop checks"),("Control","PLC simulation and/or clearly separated hobby-controller I/O emulator","I/O list, logic, sequence and diagnostics"),("Supervision","Laptop HMI/SCADA with alarms, trends and historian concepts","Screens, tag quality, alarm and trend evidence"),("Network","Laptop loopback/Wi-Fi/Ethernet or software endpoints","Network diagram, IP/protocol map and fault evidence"),("Documentation","Coordinated engineering and commissioning pack","Revisioned final release")],[34*mm,83*mm,59*mm],7.1,8.8),
              P("HMI/SCADA requirements","h2")]+checklist(["Overview, equipment detail, alarm and trend navigation","Command, mode, owner, permissive, feedback and fault visibility","Bad/stale quality indication; no plausible frozen values presented as live","Alarm priority, acknowledgement and operator response","Useful trends for PV, SP, output, pump/valve status and faults"])
    story += [PageBreak(),P("Project 3 - communications and fault campaign","h1"),
              P("Network requirements","h2")]+checklist(["Labelled topology and address/protocol schedule","PLC/HMI communications path and ownership","Ethernet/IP fundamentals without falsely claiming proprietary EtherNet/IP implementation","Modbus TCP/RTU or OPC UA concept/implementation where available","Layered troubleshooting: physical, link, address, transport, protocol, mapping and application"])
    faults=[("Failed sensor","Stuck, disconnected or implausible field value"),("Abnormal analog value","Under/over-range or incorrect scaling"),("Failed pump","Command without feedback/process response"),("Valve failure","Command without position/process effect"),("Missing permissive","Start correctly blocked with visible cause"),("E-stop/ESD condition","Training input produces defined trip response"),("PLC logic fault","Controlled defect, change record and regression"),("HMI communication failure","Bad/stale quality and command inhibition"),("Network fault","Address/protocol/connectivity issue isolated by layer")]
    story += [table(["Fault","Training implementation"],faults,[48*mm,128*mm],7.4,9.2),Spacer(1,6),box("Required troubleshooting chain","For every fault: Symptom -> initial checks -> evidence -> isolation -> diagnosis -> root cause -> correction -> verification -> documentation.",True)]
    story += [PageBreak(),P("Project 3 - flagship documentation and demonstration","h1"),
              two_col("Engineering package",["P&ID","Electrical/control schematic","PLC I/O and instrument lists","Loop diagrams","Control narrative","Sequence description","Cause/effect matrix","Trip/interlock matrix","Alarm list","Network diagram"],"Commissioning package",["FAT/SAT-style procedure","Loop/I/O check sheets","Commissioning punch list","Troubleshooting reports","Test and regression results","HMI/SCADA screenshots","PLC screenshots/code","Final project report","5-10 minute demonstration","Backups and evidence index"]),
              P("Demonstration sequence","h2"),table(["Stage","What to show"],[("1 - Scope","Low-voltage DIY/simulation boundary and process purpose"),("2 - Architecture","Field signal through PLC, HMI and actuator/process response"),("3 - Normal operation","Manual and automatic cycle with trends"),("4 - Protection","Permissive/interlock/trip preventing unsafe simulated behavior"),("5 - Fault","One deliberate fault diagnosed using evidence"),("6 - Recovery","Correction, verification and regression"),("7 - Close","Limitations, lessons, files and next improvement")],[35*mm,141*mm],7.5,9.3),
              box("Flagship release","The system must prove integration and disciplined troubleshooting, not imitate the appearance of a real offshore facility. Honest low-voltage evidence is stronger than exaggerated industrial claims.",True)]

    story += [PageBreak(),P("Portfolio packaging and final release","h1"),box("Folder pattern","00_README | 01_Requirements | 02_Design | 03_PLC | 04_HMI_SCADA | 05_Network | 06_Testing | 07_Faults | 08_Demo | 09_Backups"),
              P("Evidence index fields","h2")]+checklist(["Evidence ID and project","Document/file title","Revision and date","Real/DIY/hobby/simulated label","Requirement or test linked","What the artifact proves","Known limitation","File path and backup"])
    story += [P("Final release checklist","h2")]+checklist(["Exactly three projects only","One evolving low-voltage rig","Every claim supported by evidence","Drawings, tags, logic, HMI and tests agree","Normal, fault and recovery demonstrated","No unsafe or overstated industrial/offshore claims","Flagship demonstration lasts 5-10 minutes"])
    story += [box("Portfolio statement","These are personal low-voltage DIY and software training projects created to demonstrate junior automation and controls reasoning. They were not commissioned on a live industrial plant and do not represent certified safety, hazardous-area or offshore experience.",True)]
    doc.build(story)
    return PORTFOLIO_PATH


if __name__ == "__main__":
    for path in (build_syllabus(), build_portfolio(), build_guide()):
        print(path)
