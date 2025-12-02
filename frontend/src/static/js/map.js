// map.js

document.addEventListener("DOMContentLoaded", () => {
  // Select all state paths inside the SVG
  const states = document.querySelectorAll("#us-map path");

  states.forEach(state => {
    // Hover effect
    state.addEventListener("mouseenter", () => {
      state.style.fill = "#4facfe"; // highlight color
      state.style.cursor = "pointer";
    });

    state.addEventListener("mouseleave", () => {
      state.style.fill = "#f9f9f9"; // reset to default
    });

    // Click event
    state.addEventListener("click", () => {
      const stateName = state.dataset.name || state.id;
      alert(`You clicked on ${stateName}`);
    });
  });
});
