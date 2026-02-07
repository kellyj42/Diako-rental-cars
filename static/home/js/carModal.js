function filterCars() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();
  const categoryFilter = document.getElementById("categoryFilter").value;
  const cards = document.querySelectorAll("#modalCars > div");
  let visibleCount = 0;

  cards.forEach((card) => {
    const searchText = card.getAttribute("data-search").toLowerCase();
    const category = card.getAttribute("data-category");
    const name = card.getAttribute("data-name");
    const transmission = card.getAttribute("data-transmission");
    const seats = parseInt(card.getAttribute("data-seats"));
    const fuel = card.getAttribute("data-fuel");

    const matchesSearch =
      !searchTerm ||
      searchText.includes(searchTerm) ||
      name.includes(searchTerm) ||
      transmission.includes(searchTerm) ||
      fuel.includes(searchTerm);

    const matchesCategory = !categoryFilter || category === categoryFilter;

    if (matchesSearch && matchesCategory) {
      card.style.display = "block";
      visibleCount++;
    } else {
      card.style.display = "none";
    }
  });

  updateResultsCount(visibleCount);

  // Show/hide no results message
  const noResults = document.getElementById("noResults");
  if (visibleCount === 0) {
    noResults.classList.remove("hidden");
  } else {
    noResults.classList.add("hidden");
  }
}

function sortCars() {
  const sortBy = document.getElementById("sortFilter").value;
  const container = document.getElementById("modalCars");
  const cards = Array.from(container.querySelectorAll("div[data-search]"));

  cards.sort((a, b) => {
    if (sortBy === "name") {
      return a
        .getAttribute("data-name")
        .localeCompare(b.getAttribute("data-name"));
    } else if (sortBy === "category") {
      return a
        .getAttribute("data-category")
        .localeCompare(b.getAttribute("data-category"));
    } else if (sortBy === "price") {
      return (
        parseFloat(a.getAttribute("data-price")) -
        parseFloat(b.getAttribute("data-price"))
      );
    }
    return 0;
  });

  // Re-append sorted cards
  cards.forEach((card) => container.appendChild(card));
}

function setQuickFilter(filter) {
  const searchInput = document.getElementById("searchInput");
  searchInput.value = filter;
  filterCars();
}

function clearFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("categoryFilter").value = "";
  filterCars();
}

function updateResultsCount(count) {
  const resultsElement = document.getElementById("resultsCount");
  resultsElement.textContent = `${count} vehicle${count !== 1 ? "s" : ""} available`;
}

function selectFromModal(button) {
  const carId = button.getAttribute("data-car-id");

  // Redirect back to booking form with car ID as parameter
  window.location.href = "/bookings/selectedCar/?car_id=" + carId;
}

// Close modal on ESC key
document.addEventListener("keydown", (e) => {
  if (
    e.key === "Escape" &&
    !document.getElementById("carModal").classList.contains("hidden")
  ) {
    closeModal();
  }
});

// Initialize filters on page load
document.addEventListener("DOMContentLoaded", function () {
  filterCars(); // Initial filter to show all cars
});

function openModalFromURL(url) {
  window.location.href = url || "/cars/list/";
}
