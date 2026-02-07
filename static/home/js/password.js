function togglePassword(inputId, iconId) {
  const passwordInput = document.getElementById(inputId);
  const toggleIcon = document.getElementById(iconId);

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleIcon.classList.remove("fa-eye");
    toggleIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    toggleIcon.classList.remove("fa-eye-slash");
    toggleIcon.classList.add("fa-eye");
  }
}

function validatePassword() {
  const password = document.getElementById("newPassword1").value;
  const strengthBar = document.getElementById("passwordStrengthBar");
  const strengthText = document.getElementById("passwordStrength");
  const submitBtn = document.getElementById("submitBtn");

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
  strengthBar.style.width = strengthPercent + "%";

  // Update strength text and color
  if (strength <= 1) {
    strengthBar.style.backgroundColor = "#ef4444"; // red
    strengthText.textContent = "Weak";
    strengthText.className = "text-xs font-semibold text-red-500";
  } else if (strength <= 3) {
    strengthBar.style.backgroundColor = "#f59e0b"; // orange
    strengthText.textContent = "Fair";
    strengthText.className = "text-xs font-semibold text-orange-500";
  } else if (strength <= 4) {
    strengthBar.style.backgroundColor = "#10b981"; // green
    strengthText.textContent = "Good";
    strengthText.className = "text-xs font-semibold text-green-500";
  } else {
    strengthBar.style.backgroundColor = "#059669"; // dark green
    strengthText.textContent = "Strong";
    strengthText.className = "text-xs font-semibold text-emerald-600";
  }

  // Check password match
  checkPasswordMatch();
}

function checkPasswordMatch() {
  const password1 = document.getElementById("newPassword1").value;
  const password2 = document.getElementById("newPassword2").value;
  const matchDiv = document.getElementById("passwordMatch");
  const submitBtn = document.getElementById("submitBtn");

  if (!password1 || !password2) {
    matchDiv.innerHTML = "";
    submitBtn.disabled = true;
    return;
  }

  if (password1 === password2) {
    matchDiv.innerHTML =
      '<i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-green-600">Passwords match</span>';
    // Only enable if password is strong enough (at least 3/5 strength)
    const strengthBar = document.getElementById("passwordStrengthBar");
    const width = parseInt(strengthBar.style.width);
    submitBtn.disabled = width < 60; // Less than 60% strength
  } else {
    matchDiv.innerHTML =
      '<i class="fas fa-times-circle text-red-500 mr-2"></i><span class="text-red-600">Passwords do not match</span>';
    submitBtn.disabled = true;
  }
}

// Initialize validation on page load
document.addEventListener("DOMContentLoaded", function () {
  validatePassword();
});
