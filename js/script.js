"use strict";

const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector(".nav-menu");

if (navToggle && navMenu) {
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isOpen));
    navToggle.setAttribute("aria-label", isOpen ? "Open navigation menu" : "Close navigation menu");
    navMenu.classList.toggle("open", !isOpen);
  });

  navMenu.addEventListener("click", (event) => {
    if (event.target.matches("a")) {
      navMenu.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Open navigation menu");
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navMenu.classList.contains("open")) {
      navMenu.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Open navigation menu");
      navToggle.focus();
    }
  });
}

document.querySelectorAll(".project-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const details = document.getElementById(button.getAttribute("aria-controls"));
    const isOpen = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!isOpen));
    button.innerHTML = isOpen
      ? 'View details <span aria-hidden="true">+</span>'
      : 'Hide details <span aria-hidden="true">−</span>';
    details?.classList.toggle("open", !isOpen);
  });
});

const sections = [...document.querySelectorAll("main section[id]")];
const navLinks = [...document.querySelectorAll(".nav-menu a")];

if ("IntersectionObserver" in window) {
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((link) => {
        link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
      });
    });
  }, { rootMargin: "-25% 0px -65%", threshold: 0 });

  sections.forEach((section) => sectionObserver.observe(section));
}

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const documentationTypes = [
  { code: "PID", title: "P&ID", purpose: "Process and instrumentation representation.", placeholder: "[ADD P&ID PDF]", caption: "P&ID — process equipment, piping, instruments, and control relationships." },
  { code: "I/O", title: "I/O List", purpose: "Maps field devices to PLC inputs and outputs.", placeholder: "[ADD I/O LIST]", caption: "I/O list — signals, addresses, tags, ranges, and descriptions." },
  { code: "INS", title: "Instrument List", purpose: "Documents instruments, tags, ranges, and signals.", placeholder: "[ADD INSTRUMENT LIST]", caption: "Instrument list — service, tag, range, units, and signal type." },
  { code: "ESD", title: "Electrical Schematic", purpose: "Represents power, protection, and control circuits.", placeholder: "[ADD ELECTRICAL SCHEMATIC]", caption: "Electrical schematic — power and control relationships." },
  { code: "WDG", title: "Wiring Diagram", purpose: "Defines terminal, conductor, panel, and field connections.", placeholder: "[ADD WIRING DIAGRAM]", caption: "Wiring diagram — connection and termination details." },
  { code: "LOP", title: "Loop Diagram", purpose: "Traces an instrument loop from field to control system.", placeholder: "[ADD LOOP DIAGRAM]", caption: "Loop diagram — full instrument signal and wiring path." },
  { code: "CN", title: "Control Narrative", purpose: "Defines operating sequence and control intent.", placeholder: "[ADD CONTROL NARRATIVE]", caption: "Control narrative — plain-language process and equipment behavior." },
  { code: "C&E", title: "Cause & Effect", purpose: "Maps initiating events to required system responses.", placeholder: "[ADD CAUSE & EFFECT DOCUMENT]", caption: "Cause & Effect — alarm, trip, and shutdown responses." },
  { code: "ALM", title: "Alarm List", purpose: "Records priority, setpoint, delay, message, and response.", placeholder: "[ADD ALARM LIST]", caption: "Alarm list — configured limits and operator response guidance." },
  { code: "NET", title: "Network Diagram", purpose: "Shows control devices, links, protocols, and addressing.", placeholder: "[ADD NETWORK DIAGRAM]", caption: "Network diagram — PLC, HMI/SCADA, switches, and protocol boundaries." },
  { code: "TST", title: "Test Procedure", purpose: "Records preconditions, steps, expectations, and evidence.", placeholder: "[ADD TEST PROCEDURE]", caption: "Test procedure — expected versus actual system behavior." },
  { code: "FFR", title: "Troubleshooting Report", purpose: "Records symptoms, investigation, cause, action, and verification.", placeholder: "[ADD TROUBLESHOOTING REPORT]", caption: "Troubleshooting report — evidence-based fault diagnosis." },
  { code: "CHG", title: "Change Log", purpose: "Tracks revision, reason, author, date, and approval.", placeholder: "[ADD CHANGE LOG]", caption: "Change log — controlled history of technical updates." }
];

const evidenceTypes = [
  { code: "PROCESS", title: "Add process diagram", note: "Process flow, equipment tags and system boundaries." },
  { code: "PLC", title: "Add PLC screenshot", note: "Program logic, sequencing, permissives and interlocks." },
  { code: "HMI / SCADA", title: "Add HMI screenshot", note: "Operator view, process values, alarms and equipment states." },
  { code: "INSTRUMENTATION", title: "Add instrument configuration / simulation screenshot", note: "Signal range, scaling, units and validation points." },
  { code: "ELECTRICAL", title: "Add electrical schematic", note: "Power, protection, control and field connections." }
];

const projectProfiles = {
  "project-conveyor": {
    name: "Automated Conveyor System",
    description: "A discrete-control training project for safe conveyor operation, product detection and counting. The design covers Start/Stop priority, operating modes, motor interlocks, feedback monitoring and controlled fault recovery.",
    tests: [
      ["CV-T01", "Start with all permissives healthy", "Conveyor starts and run feedback is confirmed"],
      ["CV-T02", "Activate emergency stop", "Motor output drops and restart is inhibited"],
      ["CV-T03", "Pass an object sensor target", "Counter increments once per detected object"]
    ],
    faults: [
      ["CV-FF01", "Conveyor motor will not start", "Run command present but motor feedback remains off", "Check mode, E-stop, overload, output command and feedback path"],
      ["CV-FF02", "Product count is incorrect", "Count is missed or increments more than once", "Check sensor state, edge detection, scan logic and counter reset"]
    ]
  },
  "project-tank": {
    name: "Automated Tank / Filling System",
    description: "A process-control simulation for filling, monitoring and discharging a tank. It combines analog level, pressure, temperature and flow values with pump and valve control, alarm thresholds, permissives and safe shutdown logic.",
    tests: [
      ["TK-T01", "Run automatic fill sequence", "Inlet opens and closes at the defined level setpoint"],
      ["TK-T02", "Simulate high-high level", "Inflow stops and high-high alarm is latched"],
      ["TK-T03", "Simulate loss of level signal", "Signal fault is shown and automatic operation is inhibited"]
    ],
    faults: [
      ["TK-FF01", "Tank does not stop filling", "Level rises beyond the normal stop setpoint", "Check scaled level, setpoint comparison, valve command and feedback"],
      ["TK-FF02", "Pump will not start", "Start request is active but pump command remains off", "Check low-level inhibit, overload, E-stop, mode and discharge path"]
    ]
  },
  "project-scada": {
    name: "SCADA Process Control System",
    description: "An operator-interface and communications project focused on clear process status, alarm handling, trends, modes and PLC data quality. It demonstrates how control data is presented without transferring safety responsibility to the HMI.",
    tests: [
      ["SC-T01", "Verify PLC tag updates", "Values and equipment states refresh correctly on the HMI"],
      ["SC-T02", "Trigger a configured alarm", "Alarm appears with priority, timestamp and acknowledgement state"],
      ["SC-T03", "Interrupt communications", "Bad quality is shown and stale commands are prevented"]
    ],
    faults: [
      ["SC-FF01", "SCADA values are stale", "Values stop updating while the screen remains available", "Check PLC availability, network path, driver session and tag quality"],
      ["SC-FF02", "Alarm is not displayed", "PLC alarm condition is active but no HMI alarm appears", "Check alarm expression, tag mapping, enabled state and priority filters"]
    ]
  },
  "project-water": {
    name: "Automated Water Treatment Plant",
    description: "A flagship training simulation connecting raw-water intake, treatment, filtration, storage and monitored output. It brings PLC sequencing, instrumentation, SCADA, networking, electrical control and diagnostic thinking into one traceable system.",
    tests: [
      ["WT-T01", "Run normal treatment sequence", "Each stage advances only when its permissives are satisfied"],
      ["WT-T02", "Simulate pump overload", "Pump stops, alarm latches and dependent stages hold safely"],
      ["WT-T03", "Simulate invalid transmitter signal", "Bad signal is identified and affected control is inhibited"]
    ],
    faults: [
      ["WT-FF01", "Treatment pump will not start", "Sequence requests the pump but no run feedback is received", "Trace permissives, PLC output, overload state and motor feedback"],
      ["WT-FF02", "Outlet flow reading is incorrect", "Displayed flow differs from the simulated reference", "Check raw value, input range, engineering-unit scaling and HMI tag"]
    ]
  }
};

function projectSectionHeading(index, title, note) {
  return `<div class="project-subheading"><span>${String(index).padStart(2, "0")}</span><div><h4>${title}</h4><p>${note}</p></div></div>`;
}

Object.entries(projectProfiles).forEach(([projectId, profile]) => {
  const details = document.getElementById(projectId);
  if (!details) return;

  const evidenceCards = evidenceTypes.map((item) => `
    <article>
      <span>${item.code}</span>
      <h4>[${item.title.toUpperCase()}]</h4>
      <p>${item.note}</p>
      <button class="preview-button" type="button" data-preview="[${item.title.toUpperCase()}]" data-caption="${profile.name}: ${item.note}">Preview placeholder</button>
    </article>`).join("");

  const testRows = profile.tests.map(([id, test, expected]) => `
    <tr><td>${id}</td><td>${test}</td><td>${expected}</td><td>[ADD ACTUAL RESULT]</td><td><span class="status not-tested">NOT TESTED</span></td></tr>`).join("");

  const faultCards = profile.faults.map(([id, title, symptom, checks]) => `
    <article class="fault-card compact-fault">
      <div class="fault-head"><span>${id}</span><h3>${title}</h3><b>FAULT FINDING</b></div>
      <dl>
        <div><dt>Symptoms</dt><dd>${symptom}</dd></div>
        <div><dt>Checks</dt><dd>${checks}</dd></div>
        <div><dt>Root cause</dt><dd>[ADD CONFIRMED ROOT CAUSE]</dd></div>
        <div><dt>Action</dt><dd>[ADD CORRECTIVE ACTION]</dd></div>
        <div><dt>Verification</dt><dd>[ADD RETEST RESULT AND EVIDENCE]</dd></div>
      </dl>
    </article>`).join("");

  const documentCards = documentationTypes.map((item) => `
    <article>
      <span>${item.code}</span>
      <div><h3>${item.title}</h3><p>${item.purpose}</p><small>Version: [VERSION] · Date: [DATE]</small></div>
      <button class="preview-button" type="button" data-preview="${item.placeholder}" data-caption="${profile.name}: ${item.caption}">Add document</button>
    </article>`).join("");

  details.innerHTML = `
    <section class="project-block project-description" aria-label="Project description">
      ${projectSectionHeading(1, "Project description", "Scope and control objective")}
      <p>${profile.description}</p>
    </section>
    <section class="project-block" aria-label="Project evidence">
      ${projectSectionHeading(2, "Evidence", "Add authentic project files as the work is completed")}
      <div class="evidence-gallery">${evidenceCards}</div>
    </section>
    <section class="project-block" aria-label="Project testing">
      ${projectSectionHeading(3, "Testing", "Expected and actual results kept together")}
      <div class="io-wrap"><div class="testing-table-card"><table><caption>${profile.name} — Functional Test Record</caption><thead><tr><th>Test ID</th><th>Test</th><th>Expected result</th><th>Actual result</th><th>Status</th></tr></thead><tbody>${testRows}</tbody></table></div></div>
    </section>
    <section class="project-block project-troubleshooting" aria-label="Project troubleshooting">
      ${projectSectionHeading(4, "Fault-finding &amp; troubleshooting", "Two structured diagnostic records for this project")}
      <div class="fault-grid">${faultCards}</div>
    </section>
    <section class="project-block project-documentation" aria-label="Project documentation">
      ${projectSectionHeading(5, "Documentation", "Controlled engineering records for design, testing and maintenance")}
      <div class="document-grid">${documentCards}</div>
    </section>
    <div class="project-repository"><p>Keep source files, revisions and supporting evidence together in the project repository.</p><a class="button button-primary placeholder-link" href="https://github.com/your-username" target="_blank" rel="noreferrer">View project on GitHub <span aria-hidden="true">↗</span></a></div>`;
});

document.querySelector('.footer-links a[href="#top"]')?.addEventListener("click", (event) => {
  event.preventDefault();
  window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
});

const lightbox = document.getElementById("evidence-lightbox");
const lightboxTitle = document.getElementById("lightbox-title");
const lightboxCaption = document.getElementById("lightbox-caption");

document.querySelectorAll(".preview-button").forEach((button) => {
  button.addEventListener("click", () => {
    lightboxTitle.textContent = button.dataset.preview || "[ADD ACTUAL EVIDENCE]";
    lightboxCaption.textContent = button.dataset.caption || "Replace this placeholder with real project evidence.";
    lightbox?.showModal();
  });
});

lightbox?.querySelector(".lightbox-close")?.addEventListener("click", () => lightbox.close());
lightbox?.addEventListener("click", (event) => {
  if (event.target === lightbox) lightbox.close();
});
