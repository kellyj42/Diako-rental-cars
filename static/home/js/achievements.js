document.addEventListener("DOMContentLoaded", () => {
  // --- achievements counters (safe-guarded) ---
  const section = document.getElementById("achievements");
  const counters = document.querySelectorAll(".counter");
  if (section && counters.length) {
    let animated = false;

    const runCounters = () => {
      counters.forEach((counter) => {
        const target = +counter.dataset.target || 0;
        let current = 0;
        const increment = Math.max(1, Math.ceil(target / 100));

        const update = () => {
          current += increment;
          if (current >= target) {
            counter.textContent = target;
          } else {
            counter.textContent = current;
            requestAnimationFrame(update);
          }
        };

        update();
      });
    };

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0] && entries[0].isIntersecting && !animated) {
          animated = true;
          runCounters();
          observer.disconnect();
        }
      },
      { threshold: 0.4 },
    );

    observer.observe(section);
  }
});
