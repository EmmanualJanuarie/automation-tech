from pathlib import Path

from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Spacer

from generate_three_project_college_edition import (
    CollegeDoc,
    P,
    box,
    checklist,
    cover,
    table,
    two_col,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "02_Junior_Automation_Controls_Portfolio_Projects_COLLEGE_EDITION.pdf"


def title_page(title, window, modules, scenario):
    return [
        P(title, "h1"),
        table(
            ["RECOMMENDED WINDOW", "SYLLABUS ALIGNMENT", "SUBMISSION TYPE"],
            [(window, modules, "Individual industrial simulation project")],
            [48 * mm, 61 * mm, 67 * mm], 7.4, 9.1,
        ),
        Spacer(1, 6),
        box("Project scenario", scenario),
    ]


def rubric(rows, release):
    return [
        P("Project-specific marking rubric", "h2"),
        table(
            ["Category", "Weight", "What earns strong marks"],
            rows,
            [48 * mm, 20 * mm, 108 * mm], 7.1, 8.8,
        ),
        Spacer(1, 6),
        box("Release standard", release, True),
    ]


def build_portfolio():
    doc = CollegeDoc(
        OUTPUT,
        "Junior Automation & Controls Technician Simulated Portfolio Projects - College Edition",
        "COLLEGE EDITION PORTFOLIO",
    )
    story = cover(
        "Junior Automation & Controls Technician",
        "Four University-Structured Industrial Simulation Project Briefs",
        [
            ("PROGRAMME WINDOW", "7 September 2026 - 28 February 2027"),
            ("PORTFOLIO", "Exactly four substantial, progressively advanced projects"),
            ("DELIVERY MODEL", "Software simulation only - no physical construction required"),
            ("TARGET ROLES", "Junior automation, controls, PLC, instrumentation and E&I technician"),
        ],
        "Demonstrate industrial reasoning through requirements, PLC engineering, process simulation, HMI/SCADA, networking, structured testing, troubleshooting, commissioning and traceable documentation.",
    )

    story += [
        PageBreak(),
        P("Portfolio purpose and progression", "h1"),
        P("These projects are assessment briefs for entry-level Junior Automation Technician, Junior Controls Technician, Automation & Controls Technician, Instrumentation & Controls Technician, PLC Technician, E&I Technician and related roles. They assess applied ability rather than the ability to copy a tutorial."),
        table(
            ["Project", "Progression", "Syllabus relationship"],
            [
                ("1 - Motor & Conveyor Control", "Electrical control -> PLC I/O -> Ladder Logic -> motor/process sequence", "M1 Electrical Fundamentals + M2 PLC & Automation"),
                ("2 - Process & Instrumentation", "Analog measurement -> scaling -> sequencing -> process control -> PID", "M3 Instrumentation + M4 Process Control"),
                ("3 - SCADA & Communications", "PLC data -> HMI/SCADA -> alarms -> historian -> industrial protocols", "M5 SCADA/HMI + M6 Industrial Networking"),
                ("4 - Integrated Remote Process Package", "Documentation -> integration -> commissioning -> structured fault-finding", "M7 Documentation + M8 Safety/Commissioning, integrating M1-M6"),
            ],
            [48 * mm, 70 * mm, 58 * mm], 7.1, 8.8,
        ),
        Spacer(1, 7),
        box("Progressive standard", "Each project must reuse concepts and selected software artifacts from earlier work. Project 4 is the flagship integration and must not be four unrelated demonstrations placed in one folder."),
        P("University-brief principle", "h2"),
        P("The document specifies the problem, required functions, constraints, evidence and marking criteria. It intentionally does not prescribe rung-by-rung logic, screen layouts, tag names, database schemas or fault solutions. Those engineering decisions are part of the assessment."),
    ]

    story += [
        PageBreak(),
        P("Simulation environment and approved software", "h1"),
        P("No physical components are required. Motors, pumps, valves, switches, transmitters, analog loops, process dynamics and communication failures are represented through software I/O, process models and controlled fault injection."),
        table(
            ["Capability", "Preferred industrial platform", "Acceptable equivalent / fallback"],
            [
                ("PLC engineering", "Siemens TIA Portal + S7-PLCSIM for S7-1200/S7-1500", "CODESYS Control or another IEC 61131-3 environment; record differences"),
                ("Process/machine simulation", "Factory I/O connected to the PLC simulator", "A documented dynamic process simulator or custom signal model with credible behavior"),
                ("HMI/SCADA", "Ignition Perspective / Maker Edition for personal study", "WinCC, AVEVA, FactoryTalk View, CODESYS Visualization or equivalent if legitimately available"),
                ("Historian/data", "Ignition Historian or SQL Historian", "A documented SQL/time-series store linked to the SCADA model"),
                ("Industrial protocols", "OPC UA and Modbus TCP/RTU simulation", "Platform-native simulator or protocol server/client with register/tag map"),
                ("Network diagnostics", "Wireshark plus operating-system IP tools", "Equivalent packet/connection diagnostics with saved evidence"),
                ("Engineering documents", "EPLAN/AutoCAD Electrical where accessible", "QElectroTech, diagrams.net or another controlled drawing tool"),
            ],
            [39 * mm, 67 * mm, 70 * mm], 6.9, 8.5,
        ),
        P("Software-selection rules", "h2"),
    ]
    story += checklist([
        "Confirm version, licence and connector compatibility before committing to the architecture.",
        "Record the exact software versions, drivers, protocol endpoints and limitations used.",
        "Use one primary PLC platform consistently unless vendor translation is an explicit task.",
        "Do not claim a platform connection, protocol or test that was not demonstrated.",
        "If a preferred product is unavailable, preserve the engineering requirement and document the substitute.",
    ])
    story += [
        box("Verified capability basis", "Current Siemens S7-PLCSIM supports debugging and validation without PLC hardware. Factory I/O documents connections to S7-PLCSIM. Ignition Maker provides personal, non-commercial access to Perspective, OPC UA and historian-related capabilities. Wireshark supports capture and display-filter analysis."),
    ]

    story += [
        PageBreak(),
        P("Industrial simulation and evidence standards", "h1"),
        two_col(
            "Required simulation qualities",
            [
                "Defined scan/update behavior",
                "Engineering-unit ranges",
                "Command and feedback separated",
                "Manual/Automatic ownership",
                "Permissives and interlocks",
                "Alarm/trip recovery rules",
                "Bad/stale data quality",
                "Repeatable injected faults",
            ],
            "Prohibited claims",
            [
                "No live-plant commissioning claim",
                "No certified safety validation",
                "No hazardous-area competence claim",
                "No real offshore experience claim",
                "No hardware installation claim",
                "No protocol claim without evidence",
                "No fabricated screenshots",
                "No hidden unperformed tests",
            ],
        ),
        P("Evidence labels", "h2"),
        table(
            ["Label", "Meaning"],
            [
                ("SIMULATED", "The behavior was executed in software with defined inputs, outputs and model assumptions."),
                ("IMPLEMENTED", "The configuration, logic, display, communications or database artifact exists and is reviewable."),
                ("TESTED", "Expected and actual results, evidence, defects and retest status were recorded."),
                ("DOCUMENTED", "A revision-controlled artifact is included and coordinated with related documents."),
                ("CONCEPT ONLY", "The subject is explained but not configured or executed."),
                ("NOT TESTED", "The requirement or condition was not performed and is excluded from the claim."),
            ],
            [42 * mm, 134 * mm], 7.5, 9.2,
        ),
        Spacer(1, 6),
        box("Safety representation", "E-stop, ESD, trips, permissives and hazardous-area boundaries are functional simulations for learning. They are not safety-rated designs and must never be presented as certified protective systems.", True),
    ]

    story += [
        PageBreak(),
        P("Common project instructions", "h1"),
        P("Apply this lifecycle to every project. The sequence defines required engineering stages, not a software walkthrough."),
        table(
            ["Stage", "Required decision or output"],
            [
                ("1 - Interpret", "Extract process intent, users, modes, constraints, exclusions and measurable success criteria."),
                ("2 - Specify", "Create functional requirements, I/O, tags, signal ranges, states, alarms and interfaces."),
                ("3 - Design", "Select architecture; define control philosophy, sequences, ownership and protective behavior."),
                ("4 - Implement", "Configure the PLC, process model, HMI/SCADA, communications and data functions."),
                ("5 - Verify", "Trace every requirement to normal, boundary, fault and recovery tests."),
                ("6 - Diagnose", "Introduce controlled faults; preserve symptom, evidence, isolation, cause and verification."),
                ("7 - Release", "Resolve defects, run regression, update as-built documents, back up and demonstrate."),
            ],
            [35 * mm, 141 * mm], 7.5, 9.3,
        ),
        P("Required folder pattern", "h2"),
        box("Portfolio structure", "00_README | 01_Brief_and_Requirements | 02_Design | 03_PLC | 04_Process_Model | 05_HMI_SCADA | 06_Network_Data | 07_Testing | 08_Faults | 09_Demo | 10_Backups"),
        P("Minimum evidence index fields", "h2"),
    ]
    story += checklist([
        "Evidence ID, project, title, revision and date",
        "Software/platform/version and simulation label",
        "Requirement, interface or test proved",
        "Expected result, actual result and pass/fail state",
        "Known limitation, unresolved defect or NOT TESTED statement",
        "File path, screenshot/source relationship and backup location",
    ])

    story += [
        PageBreak(),
        P("Common assessment model", "h1"),
        P("Each project is marked out of 100. Project-specific rubrics refine these categories without changing the expectation of traceability and independent engineering judgment."),
        table(
            ["Category", "Weight", "Common evidence standard"],
            [
                ("Requirements and scope", "10%", "Requirements are measurable; assumptions, exclusions and limitations are explicit."),
                ("Architecture and design", "15%", "Interfaces, ownership, data paths, states and protective intent are coherent."),
                ("Technical implementation", "25%", "PLC/process/HMI/network behavior is correct, readable and maintainable."),
                ("Fault handling and diagnostics", "15%", "Abnormal states are detected, explained, protected and recoverable."),
                ("Verification and evidence", "20%", "Tests trace to requirements and include expected/actual results and regression."),
                ("Engineering documentation", "10%", "Documents agree with configuration, logic, tags and tests."),
                ("Technical defence", "5%", "The learner explains decisions, tradeoffs, faults and limitations independently."),
            ],
            [48 * mm, 20 * mm, 108 * mm], 7.3, 9.1,
        ),
        P("Grade descriptors", "h2"),
        table(
            ["Band", "Descriptor"],
            [
                ("85-100 | Distinction", "Integrated, traceable and professionally presented; fault reasoning and limitations are unusually strong."),
                ("75-84 | Competent", "Requirements are met with sound implementation, testing and documentation; minor gaps do not undermine claims."),
                ("60-74 | Developing", "Core operation works, but integration, diagnostics, evidence or document consistency needs improvement."),
                ("Below 60 | Not released", "Important functions are incomplete, unproved or poorly understood."),
            ],
            [42 * mm, 134 * mm], 7.5, 9.3,
        ),
        Spacer(1, 7),
        box("Safety-critical release rule", "Any unresolved simulated E-stop/ESD, trip, restart, command-ownership or bad-quality-data defect prevents release regardless of total score.", True),
    ]

    # Project 1 - pages 7-10
    story += [PageBreak()] + title_page(
        "Project 1 - Industrial Motor & Conveyor Control Simulation",
        "5 October - 15 November 2026",
        "M1 Electrical Fundamentals + M2 PLC & Automation",
        "A distribution facility requires a two-zone conveyor controller that moves items from an infeed point to a discharge point. The simulated system must provide safe starting, clear command ownership, object tracking, controlled stopping and diagnosable faults.",
    )
    story += [
        P("Assessment purpose", "h2"),
        P("Establish the industrial chain: electrical/control intent -> field I/O -> PLC scan and Ladder Logic -> output command -> simulated motor/process response."),
        P("Required software", "h2"),
        table(
            ["Function", "Preferred tool", "Evidence expected"],
            [
                ("PLC", "TIA Portal + S7-PLCSIM", "Hardware configuration, tag table, blocks, monitoring and diagnostics"),
                ("Machine/process", "Factory I/O conveyor scene or equivalent", "Mapped sensors/actuators and repeatable object behavior"),
                ("Operator interface", "Ignition Perspective or equivalent HMI", "Overview, modes, commands, status, faults and count"),
                ("Documentation", "Controlled drawing/document tool", "Schematic, I/O list, narrative, sequence and tests"),
            ],
            [36 * mm, 60 * mm, 80 * mm], 7.1, 8.8,
        ),
        P("Learning outcomes", "h2"),
    ]
    story += checklist([
        "Translate an operating description into I/O, Ladder Logic, modes and tests.",
        "Apply start/stop, seal-in, timers, counters, one-shots, permissives and interlocks.",
        "Separate commands, outputs and simulated running feedback.",
        "Diagnose electrical-control, I/O, logic and sequence faults by layer.",
    ])

    story += [
        PageBreak(),
        P("Project 1 - functional specification", "h1"),
        P("Develop the implementation independently. Your solution must meet the following outcomes; the brief does not prescribe rung structure or tag naming."),
        P("Required functions", "h2"),
    ]
    story += checklist([
        "Two conveyor zones or equivalent motor sections with independent command and feedback states.",
        "Start, Stop, Reset and training E-stop/healthy-chain simulation.",
        "Local/Remote and Manual/Automatic command ownership with defined transition behavior.",
        "Start permissives, motor interlocks and restart inhibition after a trip or simulated power cycle.",
        "Entry, transfer and exit detection with one count per item.",
        "Start-failure, transfer timeout/jam, sensor discrepancy and overload/VFD-fault representation.",
        "Alarm acknowledgement separated from fault correction and reset.",
        "HMI indication of command, feedback, mode, owner, permissives, interlocks and first relevant fault.",
    ])
    story += [
        P("Engineering constraints", "h2"),
        table(
            ["Constraint", "Requirement"],
            [
                ("Control authority", "The PLC retains sequencing and protection; the HMI requests actions but does not replace PLC logic."),
                ("Feedback", "Motor running feedback must not be derived directly from the run command."),
                ("Restart", "No automatic restart after training E-stop, overload/trip or simulated power restoration."),
                ("Counting", "A maintained or chattering sensor must not increment the counter repeatedly."),
                ("Traceability", "Every I/O, tag, alarm and test uses a consistent identifier."),
            ],
            [43 * mm, 133 * mm], 7.4, 9.1,
        ),
        box("Challenge", "Objects arrive at irregular intervals. Design sequence and count logic that remains correct when sensors stay active across several PLC scans and when an item stalls between zones.", True),
    ]

    story += [
        PageBreak(),
        P("Project 1 - required work and submission", "h1"),
        two_col(
            "Engineering work",
            [
                "Define assumptions and exclusions",
                "Create architecture and I/O list",
                "Write control narrative and sequence",
                "Develop commented PLC logic",
                "Configure the conveyor/process model",
                "Create the operator interface",
                "Design normal/fault/recovery tests",
                "Resolve defects and issue as-built files",
            ],
            "Submission package",
            [
                "Requirements specification",
                "Electrical/control schematic",
                "PLC I/O and tag lists",
                "Control narrative",
                "Sequence/state diagram",
                "PLC source/export and screenshots",
                "HMI screens",
                "Test and fault reports",
                "Evidence index and 5-minute demonstration",
            ],
        ),
        P("Mandatory fault campaign", "h2"),
        table(
            ["Fault", "Required evidence"],
            [
                ("Sensor stuck on/off", "Symptom, I/O/tag state, sequence effect, diagnosis and verified recovery"),
                ("Motor command without feedback", "Start-failure timing, alarm/trip behavior and reset conditions"),
                ("Missing permissive", "Blocked start plus operator-visible cause"),
                ("Transfer jam", "Timeout, stopped outputs, retained diagnostic cause and controlled restart"),
                ("HMI request in Local", "Command rejection and ownership indication"),
                ("Logic defect", "Change record, corrected logic and regression of unaffected functions"),
            ],
            [47 * mm, 129 * mm], 7.4, 9.1,
        ),
    ]

    story += [PageBreak(), P("Project 1 - verification and marking", "h1")]
    story += rubric(
        [
            ("Requirements/I/O design", "15%", "Complete, consistent I/O, modes, sequence and measurable acceptance criteria."),
            ("PLC implementation", "25%", "Readable Ladder Logic correctly handles scan behavior, timers, counters and state."),
            ("Modes/protection", "20%", "Ownership, permissives, interlocks, trips and restart behavior are explicit."),
            ("Simulation/HMI", "15%", "Process behavior and operator information agree with PLC states."),
            ("Fault tests", "15%", "Six faults are diagnosed and recovered using evidence."),
            ("Documentation/defence", "10%", "Documents agree and the learner explains decisions without a walkthrough."),
        ],
        "Minimum 75/100, all mandatory functions demonstrated, all six faults closed, and no unresolved restart, ownership or protective-response defect.",
    )
    story += [
        P("Examiner questions", "h2"),
    ]
    story += checklist([
        "Why is running feedback independent of the command?",
        "How does the design prevent one object from being counted repeatedly?",
        "What prevents a restart after a trip?",
        "Where would you investigate if the process sensor is true but the PLC tag is false?",
        "Which project claim remains simulated rather than industrially validated?",
    ])

    # Project 2 - pages 11-14
    story += [PageBreak()] + title_page(
        "Project 2 - Automated Process & Instrumentation Simulation",
        "16 November - 27 December 2026",
        "M3 Instrumentation + M4 Process Control, extending Project 1 PLC skills",
        "A process package transfers liquid from a feed reservoir through duty/standby pumps into a process vessel, then through a controlled outlet to storage. Instrumentation, sequencing and protective functions must keep the simulated process within defined operating limits.",
    )
    story += [
        P("Assessment purpose", "h2"),
        P("Establish the chain: process -> instrument -> signal -> PLC scaling/control -> final element -> process response."),
        P("Required software", "h2"),
        table(
            ["Function", "Preferred tool", "Evidence expected"],
            [
                ("PLC", "TIA Portal + S7-PLCSIM", "Analog/digital configuration, sequencing, scaling, alarms and PID fundamentals"),
                ("Process model", "Factory I/O fluid scene or equivalent dynamic model", "Level/flow/pressure/temperature response and disturbances"),
                ("HMI", "Ignition Perspective or equivalent", "P&ID-style overview, faceplates, alarms and trends"),
                ("Signals", "Simulator tags/math representing 4-20 mA and failures", "Raw value, current, percent, engineering value and quality"),
            ],
            [36 * mm, 61 * mm, 79 * mm], 7.1, 8.8,
        ),
        P("Learning outcomes", "h2"),
    ]
    story += checklist([
        "Select and document simulated measurement ranges and signal types.",
        "Scale and validate analog values, including under/over-range and bad quality.",
        "Develop pump/valve sequencing, Manual/Automatic control and protective responses.",
        "Interpret PV/SP/MV and PID response without confusing process faults with instrument faults.",
    ])

    story += [
        PageBreak(),
        P("Project 2 - functional specification", "h1"),
        P("The process model must be dynamic enough for operator action, controller output and disturbances to produce visible trends."),
        P("Required measurements and control", "h2"),
    ]
    story += checklist([
        "Continuous vessel level plus independent low-low and high-high protective inputs.",
        "Temperature measurement with defined range, units, normal band and alarm limits.",
        "Flow measurement or credible calculated flow with a no-flow condition.",
        "Pressure measurement concept using a simulated 4-20 mA transmitter.",
        "Raw-to-engineering scaling and reverse calculation for at least three analog signals.",
        "Duty/standby pump selection, automatic failover and unavailable-device handling.",
        "Outlet valve command/position discrepancy and defined fail-state assumption.",
        "Level control using PID fundamentals or a justified alternative control strategy.",
        "Alarm, interlock, permissive and trip behavior coordinated through cause/effect.",
    ])
    story += [
        P("Calibration and loop requirements", "h2"),
        table(
            ["Activity", "Minimum evidence"],
            [
                ("Three-point verification", "Low, midpoint and high input with expected/actual raw, mA, percent and engineering value"),
                ("As-found/as-left", "One intentionally incorrect range or bias, identified and corrected without hiding the original result"),
                ("Loop check", "Process value -> transmitter model -> PLC raw/scaled tag -> HMI display/alarm"),
                ("Plausibility", "Detection or documented handling for frozen, noisy, under-range and over-range values"),
            ],
            [47 * mm, 129 * mm], 7.4, 9.1,
        ),
        box("Challenge", "Maintain vessel level through a changing outlet disturbance while one duty pump becomes unavailable. The design must avoid high-high level, indicate degraded operation and recover without an uncontrolled output step.", True),
    ]

    story += [
        PageBreak(),
        P("Project 2 - required work and submission", "h1"),
        two_col(
            "Engineering work",
            [
                "Define process and ranges",
                "Create P&ID and instrument list",
                "Develop I/O and loop architecture",
                "Write sequence/control narrative",
                "Configure scaling and process model",
                "Develop PLC and HMI functions",
                "Perform calibration/loop checks",
                "Run faults, regression and release",
            ],
            "Submission package",
            [
                "Requirements and process assumptions",
                "P&ID and control schematic",
                "Instrument/I/O/tag lists",
                "Loop diagrams",
                "Control narrative and sequence",
                "Alarm list and cause/effect",
                "Calibration and loop sheets",
                "PLC/HMI/process-model files",
                "Test/fault reports and demonstration",
            ],
        ),
        P("Mandatory fault campaign", "h2"),
        table(
            ["Fault", "Required evidence"],
            [
                ("Incorrect scaling", "As-found value, calculation, configuration cause, correction and three-point retest"),
                ("Frozen/noisy level", "Trend evidence, quality/plausibility response and safe process action"),
                ("Duty pump failure", "Failover behavior, alarm, capacity limitation and recovery"),
                ("Valve fails to move", "Command/feedback discrepancy and process consequence"),
                ("No-flow condition", "Pump command, flow response, delay, trip/alarm and diagnosis"),
                ("High-high level", "Independent protective response and controlled restoration"),
            ],
            [47 * mm, 129 * mm], 7.3, 9.0,
        ),
    ]

    story += [PageBreak(), P("Project 2 - verification and marking", "h1")]
    story += rubric(
        [
            ("Process/instrument design", "15%", "P&ID, ranges, signal types, loops and assumptions form a coherent process."),
            ("PLC/process control", "25%", "Sequences, scaling, modes, pump/valve logic and PID fundamentals behave correctly."),
            ("Protection/alarms", "15%", "Permissives, interlocks, alarms, trips and recovery are coordinated."),
            ("Calibration/loop evidence", "15%", "Raw-to-display traceability and as-found/as-left evidence are correct."),
            ("Fault tests", "20%", "Instrument and process faults are distinguished using trends and layered evidence."),
            ("Documentation/defence", "10%", "The package is coordinated and engineering choices are independently defended."),
        ],
        "Minimum 75/100, all three analog chains verified, all six mandatory faults closed, and no unresolved high-high, failover, scaling or recovery defect.",
    )
    story += [P("Examiner questions", "h2")]
    story += checklist([
        "How do you distinguish a true process change from a failed instrument?",
        "Why is 4 mA a useful live zero?",
        "What prevents a controller from hiding a high-high protection requirement?",
        "How was the chosen process model validated as credible enough for this project?",
        "What evidence proves that the displayed engineering value is correct?",
    ])

    # Project 3 - pages 15-18
    story += [PageBreak()] + title_page(
        "Project 3 - SCADA, Historian & Communications Simulation",
        "28 December 2026 - 24 January 2027",
        "M5 SCADA/HMI + M6 Industrial Networking, supervising Projects 1 and 2",
        "A central supervisory system must monitor the conveyor and process package as two areas. It must provide clear operator navigation, alarm management, historical context and diagnosable communications while control authority remains in the PLC simulations.",
    )
    story += [
        P("Assessment purpose", "h2"),
        P("Prove that PLC data can be transformed into reliable operator information and historical evidence without concealing quality, ownership or communication failures."),
        P("Required software", "h2"),
        table(
            ["Function", "Preferred tool", "Evidence expected"],
            [
                ("SCADA/HMI", "Ignition Perspective / Maker Edition", "Gateway, tag providers, views, faceplates, alarms, trends and security awareness"),
                ("Controller/process", "Project 1 and 2 PLC/process simulations", "At least two supervised areas with reusable tag structures"),
                ("Protocols", "OPC UA plus Modbus TCP/RTU simulation", "Endpoint/configuration and controlled mapping evidence"),
                ("Historian", "Ignition Historian or SQL Historian", "Stored data, retrieval, time range and quality-aware trend evidence"),
                ("Diagnostics", "Wireshark and OS network tools", "Filtered capture/connection evidence and layered diagnosis"),
            ],
            [36 * mm, 60 * mm, 80 * mm], 7.0, 8.7,
        ),
        P("Learning outcomes", "h2"),
    ]
    story += checklist([
        "Design usable overview, detail, faceplate, alarm and trend navigation.",
        "Configure meaningful alarm, historian and data-quality behavior.",
        "Document Ethernet, IP, TCP, OPC UA, Modbus and serial concepts in the implemented context.",
        "Diagnose communication failures without immediately blaming PLC logic.",
    ])

    story += [
        PageBreak(),
        P("Project 3 - functional specification", "h1"),
        P("The SCADA project must supervise the prior simulations rather than becoming an unrelated dashboard."),
        P("Required supervisory functions", "h2"),
    ]
    story += checklist([
        "Site overview showing both areas, overall health, active alarms and communication state.",
        "Area and equipment views with command, mode, owner, feedback, permissive and fault information.",
        "PLC-enforced command authority; commands disabled or rejected when ownership/conditions are invalid.",
        "Alarm priorities, meaningful messages, acknowledgement, return-to-normal and operator response guidance.",
        "Trends for selected process variables, setpoints, outputs, states and fault events.",
        "Historical storage and retrieval with documented sampling/deadband assumptions.",
        "Bad/stale quality visualization that cannot be mistaken for a healthy live value.",
        "At least one OPC UA connection and one Modbus mapping or documented equivalent.",
    ])
    story += [
        P("Network and data requirements", "h2"),
        table(
            ["Artifact", "Required content"],
            [
                ("Network diagram", "Nodes, interfaces, IP/subnet, protocols, ports, trust/security boundary and failure impact"),
                ("Address schedule", "Unique addresses, role, owner, gateway requirement and status"),
                ("Protocol map", "Tag/register, direction, datatype, scale, byte/word order, update rate and quality"),
                ("Historian definition", "Tags, sample/deadband, retention assumption, timestamp source and retrieval test"),
            ],
            [48 * mm, 128 * mm], 7.4, 9.1,
        ),
        box("Challenge", "A communication outage must make current values visibly bad/stale while preserving historical context. When communications recover, command authority and data quality must recover in a controlled, observable manner.", True),
    ]

    story += [
        PageBreak(),
        P("Project 3 - required work and submission", "h1"),
        two_col(
            "Engineering work",
            [
                "Define operator tasks and hierarchy",
                "Create tag/alarm conventions",
                "Configure PLC/protocol connections",
                "Develop reusable faceplates/views",
                "Configure alarm and historian functions",
                "Create network/protocol documents",
                "Inject communications/data faults",
                "Audit usability and release",
            ],
            "Submission package",
            [
                "SCADA requirements and style guide",
                "Screen hierarchy/wireframes",
                "Tag and alarm registers",
                "Network/address/protocol maps",
                "Historian configuration record",
                "HMI/SCADA export and screenshots",
                "Packet/diagnostic evidence",
                "Communication fault reports",
                "Usability review and demonstration",
            ],
        ),
        P("Mandatory fault campaign", "h2"),
        table(
            ["Fault", "Required evidence"],
            [
                ("PLC connection loss", "Quality change, screen behavior, alarm and controlled recovery"),
                ("Wrong IP/subnet", "Layered checks and corrected address schedule"),
                ("Wrong Modbus mapping", "Register/datatype/byte-order evidence and verified value"),
                ("Stale data", "Timestamp/quality behavior and prevention of misleading display"),
                ("Invalid remote command", "Ownership rejection and audit/diagnostic indication"),
                ("Historian gap", "Detection, explanation and honest representation on trend/report"),
            ],
            [48 * mm, 128 * mm], 7.3, 9.0,
        ),
    ]

    story += [PageBreak(), P("Project 3 - verification and marking", "h1")]
    story += rubric(
        [
            ("Operator requirements/design", "15%", "Hierarchy, faceplates and interactions support defined operator tasks."),
            ("SCADA implementation", "25%", "Tags, views, commands, alarms, trends and quality behavior are robust."),
            ("Historian/alarm management", "15%", "Data and events are stored, retrieved and presented meaningfully."),
            ("Network/protocol engineering", "15%", "Topology, addressing, mappings and diagnostics are technically coherent."),
            ("Fault tests", "20%", "Six communication/data faults are isolated by layer and recovered."),
            ("Documentation/defence", "10%", "Configuration and documents agree; design tradeoffs are explained."),
        ],
        "Minimum 75/100, both prior areas supervised, all six mandatory faults closed, and no unresolved command-ownership, bad-quality or misleading stale-data defect.",
    )
    story += [P("Examiner questions", "h2")]
    story += checklist([
        "Which control decisions remain in the PLC, and why?",
        "How does the display distinguish bad, stale and healthy data?",
        "Why can ping succeed while an OPC/Modbus connection fails?",
        "How were alarm priority and historian sampling decisions justified?",
        "What evidence isolates a mapping error from a process error?",
    ])

    # Project 4 - pages 19-23
    story += [PageBreak()] + title_page(
        "Project 4 - Integrated Remote/Offshore Process Package Simulation",
        "25 January - 28 February 2027",
        "M7 Engineering Documentation + M8 Safety, Commissioning & Troubleshooting; integrates M1-M6",
        "A remote process package receives feed, operates pump and motor equipment, controls a process vessel, represents separator/filter duty and transfers product to storage. The learner must commission, operate, diagnose and hand over the complete simulated system.",
    )
    story += [
        box("Representation boundary", "This is an industrially inspired software simulation. It is not an oil rig, a certified offshore system, a hazardous-area design or proof of site authorization. Safety and ESD behavior is assessed only as control-system logic and documentation.", True),
        P("Assessment purpose", "h2"),
        P("Demonstrate integrated junior-technician competence across PLCs, instrumentation, process control, SCADA, networking, engineering documentation, FAT/SAT-style testing and structured troubleshooting."),
        P("Required integrated software", "h2"),
        table(
            ["Layer", "Expected platform"],
            [
                ("PLC/control", "TIA Portal + S7-PLCSIM or declared IEC equivalent"),
                ("Process", "Factory I/O or credible dynamic process model"),
                ("HMI/SCADA/historian", "Ignition Perspective/Maker or equivalent industrial platform"),
                ("Protocols/network", "OPC UA/Modbus simulation, Wireshark and OS diagnostics"),
                ("Documents", "Controlled drawing, spreadsheet and report tools"),
            ],
            [46 * mm, 130 * mm], 7.5, 9.2,
        ),
    ]

    story += [
        PageBreak(),
        P("Project 4 - system and control requirements", "h1"),
        P("The flagship must reuse and extend selected controller, process, HMI, alarm, historian and diagnostic patterns from Projects 1-3."),
        two_col(
            "Process/control scope",
            [
                "Feed and storage boundaries",
                "Duty/standby pump service",
                "Motor/conveyor or transfer equipment",
                "Process vessel instrumentation",
                "Valve/final-element behavior",
                "Separator/filter representation",
                "Manual/Automatic sequences",
                "Defined disturbances and limits",
            ],
            "Protective/diagnostic scope",
            [
                "Start permissives",
                "Operating interlocks",
                "Alarm and trip priorities",
                "Training E-stop/ESD logic",
                "First-out/cause retention",
                "Bad-value validation",
                "Communications fallback",
                "Controlled reset and restart",
            ],
        ),
        P("Operational requirements", "h2"),
    ]
    story += checklist([
        "Provide a defined startup, normal operation, controlled shutdown, trip and recovery sequence.",
        "Make command source, equipment availability and unmet conditions visible at PLC and HMI levels.",
        "Keep protective logic independent enough that a routine controller or HMI defect cannot silently bypass it.",
        "Represent instrument quality, limits, alarm/trip deadbands and final-element feedback.",
        "Preserve diagnostic cause through a fault cascade and require verified healthy conditions before reset.",
    ])
    story += [box("Challenge", "Create at least two interacting fault scenarios in which the first symptom is not the root cause. The diagnosis must use chronology, signal traces, trends and communication evidence rather than trial-and-error changes.", True)]

    story += [
        PageBreak(),
        P("Project 4 - engineering documentation package", "h1"),
        two_col(
            "Design and control",
            [
                "System requirements specification",
                "P&ID",
                "Electrical/control schematic",
                "PLC I/O list",
                "Instrument list",
                "Loop diagrams",
                "Control narrative",
                "Sequence description",
                "Cause/effect matrix",
                "Trip/interlock matrix",
            ],
            "Operations and commissioning",
            [
                "Alarm list and response",
                "Network diagram/address schedule",
                "Protocol/tag map",
                "FAT/SAT-style procedure",
                "I/O and loop-check sheets",
                "Commissioning plan",
                "Punch list",
                "Troubleshooting reports",
                "As-built change register",
                "Backup and handover index",
            ],
        ),
        P("Document coordination checks", "h2"),
        table(
            ["Cross-check", "Acceptance question"],
            [
                ("Tag", "Does the same identifier appear on P&ID, I/O, logic, HMI, alarm and test records?"),
                ("Range/unit", "Do instrument, PLC scaling, HMI and alarm settings agree?"),
                ("Cause/effect", "Does implemented logic and tested response match the approved matrix?"),
                ("Network", "Do addresses, protocols, mappings and actual connections agree?"),
                ("Revision", "Can every as-built change be traced to reason, evidence and retest?"),
            ],
            [45 * mm, 131 * mm], 7.5, 9.2,
        ),
    ]

    story += [
        PageBreak(),
        P("Project 4 - commissioning and acceptance", "h1"),
        P("Treat commissioning as a controlled verification programme. The simulation does not remove the need for prerequisites, hold points, expected results, defect control and restoration checks."),
        table(
            ["Stage", "Required evidence"],
            [
                ("Readiness review", "Approved scope, architecture, software versions, document baseline and open risks"),
                ("Visual/configuration check", "Tag/range/address/module/connection consistency before execution"),
                ("I/O checks", "Stimulus -> PLC input -> logic; command -> output -> feedback for every critical point"),
                ("Loop checks", "Process model -> signal/raw/scaled value -> HMI/alarm/trend"),
                ("FAT", "Requirement-based normal, boundary, fault, recovery and sequence tests"),
                ("SAT-style integration", "PLC/process/SCADA/network start-up, failure and restoration in the final environment"),
                ("Punch close-out", "Priority, owner, correction, retest evidence, status and residual limitation"),
                ("Handover", "As-built files, backups, evidence index, known limitations and demonstration"),
            ],
            [45 * mm, 131 * mm], 7.3, 9.0,
        ),
        P("Acceptance conditions", "h2"),
    ]
    story += checklist([
        "Every critical requirement has a passed test or explicit NOT TESTED disposition.",
        "No open simulated E-stop/ESD, trip, restart, ownership or bad-quality defect remains.",
        "All punch items have severity, owner, status and verification evidence.",
        "A clean backup can restore the PLC, process model and SCADA configuration.",
        "The final demonstration can be completed in 5-10 minutes without hiding limitations.",
    ])

    story += [
        PageBreak(),
        P("Project 4 - structured fault campaign", "h1"),
        P("Introduce at least ten repeatable faults across the layers below. At least two must be interacting or cascading scenarios."),
        table(
            ["Layer", "Representative faults"],
            [
                ("Electrical/control representation", "Open healthy chain, unavailable output supply state, feedback discrepancy"),
                ("Digital I/O", "Stuck input, inverted fail-safe state, incorrect address or mapping"),
                ("Analog/instrument", "Disconnected, biased, frozen, noisy, under-range, over-range or wrong scaling"),
                ("Equipment/process", "Pump failure, valve failure, no-flow, high-high level or filter restriction"),
                ("PLC/sequence", "Missing permissive, incorrect transition, retained state or reset defect"),
                ("HMI/SCADA", "Invalid command, stale value, misleading state or alarm configuration defect"),
                ("Network/protocol", "Connection loss, wrong IP/subnet, wrong register/datatype or service failure"),
                ("Historian/time", "Data gap, timestamp inconsistency or unsuitable sampling/deadband"),
            ],
            [48 * mm, 128 * mm], 7.3, 9.0,
        ),
        P("Required report chain for every fault", "h2"),
        box("Troubleshooting method", "Symptom -> immediate simulated process protection -> initial checks -> evidence -> isolation boundary -> diagnosis -> root cause -> controlled correction -> verification -> regression -> documentation."),
        P("Fault-report minimum", "h2"),
    ]
    story += checklist([
        "Timestamped chronology and operating state",
        "Observed PLC/HMI/process/network evidence",
        "Tests considered and why they were ordered",
        "Verified root cause and rejected alternatives",
        "Correction authorization/change record in the simulation context",
        "Normal, fault, recovery and regression outcomes",
    ])

    story += [PageBreak(), P("Project 4 - verification and marking", "h1")]
    story += rubric(
        [
            ("Requirements/architecture", "15%", "The integrated package is coherent, bounded and traceable across all layers."),
            ("PLC/process implementation", "20%", "Sequences, modes, analog control and protective behavior operate correctly."),
            ("HMI/SCADA/network", "15%", "Supervision, quality, historian and communications support operation and diagnosis."),
            ("Commissioning evidence", "20%", "I/O, loops, FAT/SAT-style tests, punch control and restoration are disciplined."),
            ("Troubleshooting", "20%", "Ten faults, including two interacting cases, are isolated and verified systematically."),
            ("Documentation/defence", "10%", "As-built records agree and the learner defends decisions and limitations."),
        ],
        "Minimum 80/100 for flagship release, no category below 65%, all critical tests passed or honestly dispositioned, ten fault reports closed and no unresolved protective, restart, ownership or data-quality defect.",
    )
    story += [
        P("Five-to-ten-minute demonstration", "h2"),
        table(
            ["Stage", "Demonstration requirement"],
            [
                ("Scope", "State process purpose, software architecture and simulation limitations."),
                ("Normal operation", "Run a meaningful sequence and show PLC, HMI and trends."),
                ("Protection", "Show one permissive/interlock/trip preventing an invalid action."),
                ("Fault", "Introduce one representative fault and diagnose it from evidence."),
                ("Recovery", "Correct, verify, regress and show the updated record."),
                ("Close", "Present remaining limitations, backups and next improvement."),
            ],
            [38 * mm, 138 * mm], 7.4, 9.1,
        ),
    ]

    story += [
        PageBreak(),
        P("Portfolio final release and recruiter presentation", "h1"),
        P("Present the portfolio as four coordinated industrial simulations, with Project 4 demonstrating integration and commissioning discipline."),
        two_col(
            "Final quality check",
            [
                "Exactly four projects",
                "All work software-simulated",
                "Each project maps to syllabus modules",
                "Requirements trace to tests",
                "Normal/fault/recovery proven",
                "Documents and tags agree",
                "Sources and exports included",
                "Limitations stated honestly",
            ],
            "Interview evidence",
            [
                "One architecture diagram",
                "One PLC routine explained",
                "One analog calculation",
                "One HMI/alarm/trend example",
                "One network diagnosis",
                "One commissioning extract",
                "One fault report",
                "Flagship demonstration video",
            ],
        ),
        P("Official software reference starting points - verified 14 September 2026", "h2"),
        table(
            ["Platform", "Official reference"],
            [
                ("Siemens S7-PLCSIM", "https://cache.industry.siemens.com/dl/files/161/109997161/att_1348284/v1/S7-PLCSIM_Help_en-US.pdf"),
                ("Factory I/O + Siemens", "https://docs.factoryio.com/tutorials/siemens/"),
                ("Ignition Maker", "https://inductiveautomation.com/ignition/maker-edition"),
                ("Ignition modules", "https://docs.inductiveautomation.com/docs/8.3/getting-started/modules-overview"),
                ("Wireshark guide", "https://www.wireshark.org/download/docs/Wireshark%20User%27s%20Guide.pdf"),
            ],
            [45 * mm, 131 * mm], 6.9, 8.5,
        ),
        Spacer(1, 7),
        box("Required portfolio statement", "These are personal software simulation projects created to demonstrate junior automation and controls engineering reasoning. They were not commissioned on a live industrial plant and do not represent certified safety, hazardous-area, offshore or site experience.", True),
    ]

    doc.build(story)
    print(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    build_portfolio()
