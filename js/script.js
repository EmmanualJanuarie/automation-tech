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
    feedback.textContent = "Please complete your name, valid email, and message.";
    contactForm.reportValidity();
    return;
  }

  const formData = new FormData(contactForm);
  const name = formData.get("name");
  const email = formData.get("email");
  const company = formData.get("company") || "Not provided";
  const message = formData.get("message");
  const subject = encodeURIComponent(`Portfolio enquiry from ${name}`);
  const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\nCompany: ${company}\n\n${message}`);

  feedback.textContent = "Opening your email application…";
  window.location.href = `mailto:emmanuel@example.com?subject=${subject}&body=${body}`;
});
