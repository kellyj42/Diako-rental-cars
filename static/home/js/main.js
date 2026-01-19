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
      { threshold: 0.4 }
    );

    observer.observe(section);
  }

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
    { passive: true }
  );

  scrollContainer.addEventListener(
    "touchmove",
    (e) => {
      // allow default touch behavior; handle only if desired
      const x = e.touches[0].pageX - scrollContainer.offsetLeft;
      const walk = (x - startX) * 2;
      scrollContainer.scrollLeft = scrollLeft - walk;
    },
    { passive: true }
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
 function togglePassword(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const toggleIcon = document.getElementById(iconId);
    
    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      toggleIcon.classList.remove('fa-eye');
      toggleIcon.classList.add('fa-eye-slash');
    } else {
      passwordInput.type = 'password';
      toggleIcon.classList.remove('fa-eye-slash');
      toggleIcon.classList.add('fa-eye');
    }
  }

  function validatePassword() {
    const password = document.getElementById('newPassword1').value;
    const strengthBar = document.getElementById('passwordStrengthBar');
    const strengthText = document.getElementById('passwordStrength');
    const submitBtn = document.getElementById('submitBtn');
    
    let strength = 0;
    let strengthPercent = 0;
    
    // Check password criteria
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    // Calculate strength percentage
    strengthPercent = (strength / 5) * 100;
    
    // Update strength bar
    strengthBar.style.width = strengthPercent + '%';
    
    // Update strength text and color
    if (strength <= 1) {
      strengthBar.style.backgroundColor = '#ef4444'; // red
      strengthText.textContent = 'Weak';
      strengthText.className = 'text-xs font-semibold text-red-500';
    } else if (strength <= 3) {
      strengthBar.style.backgroundColor = '#f59e0b'; // orange
      strengthText.textContent = 'Fair';
      strengthText.className = 'text-xs font-semibold text-orange-500';
    } else if (strength <= 4) {
      strengthBar.style.backgroundColor = '#10b981'; // green
      strengthText.textContent = 'Good';
      strengthText.className = 'text-xs font-semibold text-green-500';
    } else {
      strengthBar.style.backgroundColor = '#059669'; // dark green
      strengthText.textContent = 'Strong';
      strengthText.className = 'text-xs font-semibold text-emerald-600';
    }
    
    // Check password match
    checkPasswordMatch();
  }

  function checkPasswordMatch() {
    const password1 = document.getElementById('newPassword1').value;
    const password2 = document.getElementById('newPassword2').value;
    const matchDiv = document.getElementById('passwordMatch');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!password1 || !password2) {
      matchDiv.innerHTML = '';
      submitBtn.disabled = true;
      return;
    }
    
    if (password1 === password2) {
      matchDiv.innerHTML = '<i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-green-600">Passwords match</span>';
      // Only enable if password is strong enough (at least 3/5 strength)
      const strengthBar = document.getElementById('passwordStrengthBar');
      const width = parseInt(strengthBar.style.width);
      submitBtn.disabled = width < 60; // Less than 60% strength
    } else {
      matchDiv.innerHTML = '<i class="fas fa-times-circle text-red-500 mr-2"></i><span class="text-red-600">Passwords do not match</span>';
      submitBtn.disabled = true;
    }
  }

  // Initialize validation on page load
  document.addEventListener('DOMContentLoaded', function() {
    validatePassword();
  });
  

