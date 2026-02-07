document.addEventListener("DOMContentLoaded", () => {
  // --- Vehicles horizontal scroll behavior (safe-guarded, no template vars) ---
  const scrollContainer = document.getElementById("vehicleScroll");
  if (!scrollContainer) return;

  const leftBtn = document.querySelector(".left-btn");
  const rightBtn = document.querySelector(".right-btn");
  const dots = document.querySelectorAll(".dot");

  // Card width + gap (assuming Tailwind gap-6 = 1.5rem)
  const cardWidth = 320; // w-80 = 20rem = 320px (adjust if needed)
  const gap = 24; // gap-6 = 1.5rem = 24px
  const scrollAmount = cardWidth + gap;

  let currentIndex = 0;
  const totalItems = scrollContainer.children.length || 0;

  if (dots.length > 0) {
    dots[0].classList.add("bg-orange-400", "w-4");
  }

  function updateDots() {
    if (dots.length) {
      dots.forEach((dot, index) => {
        if (index === currentIndex) {
          dot.classList.add("bg-orange-400", "w-4");
          dot.classList.remove("bg-gray-300", "w-2");
        } else {
          dot.classList.remove("bg-orange-400", "w-4");
          dot.classList.add("bg-gray-300", "w-2");
        }
      });
    }

    if (leftBtn) {
      leftBtn.disabled = currentIndex === 0;
      leftBtn.classList.toggle("opacity-50", currentIndex === 0);
    }
    if (rightBtn) {
      rightBtn.disabled = currentIndex === totalItems - 1;
      rightBtn.classList.toggle("opacity-50", currentIndex === totalItems - 1);
    }
  }

  if (rightBtn) {
    rightBtn.addEventListener("click", () => {
      if (currentIndex < totalItems - 1) {
        currentIndex++;
        scrollContainer.scrollTo({
          left: currentIndex * scrollAmount,
          behavior: "smooth",
        });
        updateDots();
      }
    });
  }

  if (leftBtn) {
    leftBtn.addEventListener("click", () => {
      if (currentIndex > 0) {
        currentIndex--;
        scrollContainer.scrollTo({
          left: currentIndex * scrollAmount,
          behavior: "smooth",
        });
        updateDots();
      }
    });
  }

  if (dots.length) {
    dots.forEach((dot) => {
      dot.addEventListener("click", () => {
        const index = parseInt(dot.getAttribute("data-index"), 10);
        if (Number.isInteger(index) && index >= 0 && index < totalItems) {
          currentIndex = index;
          scrollContainer.scrollTo({
            left: index * scrollAmount,
            behavior: "smooth",
          });
          updateDots();
        }
      });
    });
  }

  // Touch/swipe support
  let startX = 0;
  let scrollLeft = 0;

  scrollContainer.addEventListener(
    "touchstart",
    (e) => {
      startX = e.touches[0].pageX - scrollContainer.offsetLeft;
      scrollLeft = scrollContainer.scrollLeft;
    },
    { passive: true },
  );

  scrollContainer.addEventListener(
    "touchmove",
    (e) => {
      // allow default touch behavior; handle only if desired
      const x = e.touches[0].pageX - scrollContainer.offsetLeft;
      const walk = (x - startX) * 2;
      scrollContainer.scrollLeft = scrollLeft - walk;
    },
    { passive: true },
  );

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft" && leftBtn) {
      leftBtn.click();
    } else if (e.key === "ArrowRight" && rightBtn) {
      rightBtn.click();
    }
  });

  // Initial state
  updateDots();
});
