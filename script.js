
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
