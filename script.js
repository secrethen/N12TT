
const filterButtons = document.querySelectorAll("[data-filter]");
const cards = document.querySelectorAll("[data-category]");
filterButtons.forEach(btn => btn.addEventListener("click", () => {
  filterButtons.forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  const value = btn.dataset.filter;
  cards.forEach(card => {
    card.style.display = value === "all" || card.dataset.category.includes(value) ? "" : "none";
  });
}));

// Mobile hamburger navigation
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.getElementById("nav-links");
if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const open = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  // Reset state if the window is resized back up to desktop
  window.addEventListener("resize", () => {
    if (window.innerWidth > 800) {
      navLinks.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });
}
