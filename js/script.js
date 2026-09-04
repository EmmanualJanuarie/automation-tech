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

const contactForm = document.getElementById("contact-form");

contactForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  const feedback = contactForm.querySelector(".form-feedback");
  if (!contactForm.checkValidity()) {
    contactForm.reportValidity();
    if (feedback) feedback.textContent = "Please complete the required fields.";
    return;
  }

  const formData = new FormData(contactForm);
  const name = formData.get("name");
  const email = formData.get("email");
  const company = formData.get("company") || "Not provided";
  const message = formData.get("message");
  const recipient = "your-email@example.com"; // Replace with Emmanual's real email address.
  const subject = encodeURIComponent(`Portfolio enquiry from ${name}`);
  const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\nCompany: ${company}\n\n${message}`);

  if (feedback) feedback.textContent = "Opening your email application…";
  window.location.href = `mailto:${recipient}?subject=${subject}&body=${body}`;
});

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Each project uses the same controlled-document set so files can be replaced independently.
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

document.querySelectorAll("[data-doc-panel]").forEach((panel) => {
  const grid = panel.querySelector(".document-grid");
  const projectName = panel.dataset.projectName;

  documentationTypes.forEach((documentType) => {
    const card = document.createElement("article");
    const code = document.createElement("span");
    const details = document.createElement("div");
    const title = document.createElement("h3");
    const purpose = document.createElement("p");
    const meta = document.createElement("small");
    const button = document.createElement("button");

    code.textContent = documentType.code;
    title.textContent = documentType.title;
    purpose.textContent = `Purpose: ${documentType.purpose}`;
    meta.textContent = `Project: ${projectName} · Version: [VERSION] · Date: [DATE]`;
    button.className = "preview-button";
    button.type = "button";
    button.textContent = "View Document";
    button.dataset.preview = documentType.placeholder;
    button.dataset.caption = `${projectName}: ${documentType.caption}`;

    details.append(title, purpose, meta);
    card.append(code, details, button);
    grid?.append(card);
  });
});

const documentationTabs = [...document.querySelectorAll("[data-doc-tab]")];
const documentationPanels = [...document.querySelectorAll("[data-doc-panel]")];

function activateDocumentationTab(projectId, moveFocus = false) {
  const selectedTab = documentationTabs.find((tab) => tab.dataset.docTab === projectId);
  if (!selectedTab) return;

  documentationTabs.forEach((tab) => {
    const isSelected = tab === selectedTab;
    tab.setAttribute("aria-selected", String(isSelected));
    tab.tabIndex = isSelected ? 0 : -1;
  });

  documentationPanels.forEach((panel) => {
    panel.hidden = panel.dataset.docPanel !== projectId;
  });

  if (moveFocus) selectedTab.focus({ preventScroll: true });
}

documentationTabs.forEach((tab, index) => {
  tab.addEventListener("click", () => activateDocumentationTab(tab.dataset.docTab));
  tab.addEventListener("keydown", (event) => {
    let nextIndex;
    if (event.key === "ArrowRight") nextIndex = (index + 1) % documentationTabs.length;
    if (event.key === "ArrowLeft") nextIndex = (index - 1 + documentationTabs.length) % documentationTabs.length;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = documentationTabs.length - 1;
    if (nextIndex === undefined) return;
    event.preventDefault();
    activateDocumentationTab(documentationTabs[nextIndex].dataset.docTab, true);
  });
});

document.querySelectorAll(".project-document-link").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    activateDocumentationTab(link.dataset.docProject);
    document.getElementById("documentation")?.scrollIntoView({
      behavior: prefersReducedMotion ? "auto" : "smooth",
      block: "start"
    });
  });
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
