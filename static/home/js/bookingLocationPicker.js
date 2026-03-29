document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("locationPickerModal");
  const mapElement = document.getElementById("bookingLocationMap");
  if (!modal || !mapElement || typeof L === "undefined") return;

  const openButtons = document.querySelectorAll(".location-picker-trigger");
  const closeButton = document.getElementById("closeLocationPicker");
  const cancelButton = document.getElementById("cancelLocationBtn");
  const confirmButton = document.getElementById("confirmLocationBtn");
  const searchButton = document.getElementById("searchLocationBtn");
  const searchInput = document.getElementById("locationSearchInput");
  const resultsBox = document.getElementById("locationSearchResults");
  const selectedLabel = document.getElementById("selectedLocationLabel");

  let activeInput = null;
  let selectedAddress = "";
  let selectedLatLng = null;
  let marker = null;
  let mapInitialized = false;

  const ugandaCenter = [1.3733, 32.2903];
  const map = L.map(mapElement, {
    center: ugandaCenter,
    zoom: 7,
    zoomControl: true,
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  function resetSelection(message) {
    selectedAddress = "";
    selectedLatLng = null;
    selectedLabel.textContent = message || "No location selected yet.";
    confirmButton.disabled = true;
  }

  function setSelection(address, lat, lng) {
    selectedAddress = address;
    selectedLatLng = { lat, lng };
    selectedLabel.textContent = address;
    confirmButton.disabled = false;

    if (marker) {
      marker.setLatLng([lat, lng]);
    } else {
      marker = L.marker([lat, lng]).addTo(map);
    }
  }

  function renderResults(items) {
    resultsBox.innerHTML = "";

    if (!items.length) {
      resultsBox.innerHTML = '<p class="p-2 text-gray-500">No matches found. Try a different search or click on the map.</p>';
      return;
    }

    items.forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "block w-full rounded-lg border border-gray-700 bg-gray-900 px-3 py-2 text-left text-sm text-gray-200 hover:border-yellow-400 hover:bg-gray-800";
      button.textContent = item.display_name;
      button.addEventListener("click", () => {
        const lat = Number(item.lat);
        const lng = Number(item.lon);
        map.setView([lat, lng], 15);
        setSelection(item.display_name, lat, lng);
      });
      resultsBox.appendChild(button);
    });
  }

  async function searchLocations() {
    const query = searchInput.value.trim();
    if (!query) {
      renderResults([]);
      return;
    }

    resultsBox.innerHTML = '<p class="p-2 text-gray-500">Searching...</p>';

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=jsonv2&countrycodes=ug&limit=8&q=${encodeURIComponent(query)}`,
        {
          headers: {
            Accept: "application/json",
          },
        }
      );
      const results = await response.json();
      renderResults(results);
    } catch (error) {
      resultsBox.innerHTML = '<p class="p-2 text-red-400">Could not load search results right now.</p>';
    }
  }

  async function reverseGeocode(lat, lng) {
    selectedLabel.textContent = "Looking up address...";
    confirmButton.disabled = true;

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lng)}`,
        {
          headers: {
            Accept: "application/json",
          },
        }
      );
      const result = await response.json();
      const address = result.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
      setSelection(address, lat, lng);
    } catch (error) {
      setSelection(`${lat.toFixed(5)}, ${lng.toFixed(5)}`, lat, lng);
    }
  }

  function openModal(targetInputId) {
    activeInput = document.getElementById(targetInputId);
    if (!activeInput) return;

    modal.classList.remove("hidden");
    modal.classList.add("flex");
    searchInput.value = activeInput.value || "";
    resetSelection("Search for a place or click directly on the map.");

    if (!mapInitialized) {
      mapInitialized = true;
    }

    window.setTimeout(() => {
      map.invalidateSize();
      map.setView(ugandaCenter, 7);
    }, 50);

    if (searchInput.value.trim()) {
      searchLocations();
    } else {
      resultsBox.innerHTML = '<p class="p-2 text-gray-500">Search for a place or click directly on the map.</p>';
    }
  }

  function closeModal() {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    activeInput = null;
  }

  openButtons.forEach((button) => {
    button.addEventListener("click", () => openModal(button.dataset.locationTarget));
  });

  closeButton.addEventListener("click", closeModal);
  cancelButton.addEventListener("click", closeModal);

  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  searchButton.addEventListener("click", searchLocations);
  searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      searchLocations();
    }
  });

  confirmButton.addEventListener("click", () => {
    if (!activeInput || !selectedAddress) return;
    activeInput.value = selectedAddress;
    activeInput.dispatchEvent(new Event("input", { bubbles: true }));
    closeModal();
  });

  map.on("click", (event) => {
    reverseGeocode(event.latlng.lat, event.latlng.lng);
  });
});
