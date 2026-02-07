function validatePassword() {
    const passwordInput = document.getElementById("password1");
    const strengthText = document.getElementById("passwordStrength");
    const strengthBar = document.getElementById("passwordStrengthBar");

    const password = passwordInput.value;
    let score = 0;

    // Reset when empty
    if (!password) {
      strengthText.textContent = "None";
      strengthText.className = "text-xs font-semibold text-gray-400";
      strengthBar.style.width = "0%";
      strengthBar.className = "h-2 rounded-full transition-all duration-300";
      return;
    }

    // Length check
    if (password.length >= 8) score++;

    // Lowercase
    if (/[a-z]/.test(password)) score++;

    // Uppercase
    if (/[A-Z]/.test(password)) score++;

    // Numbers
    if (/[0-9]/.test(password)) score++;

    // Special characters
    if (/[^A-Za-z0-9]/.test(password)) score++;

    // Map score to UI
    let strength = "";
    let color = "";
    let width = "";

    switch (score) {
      case 1:
      case 2:
        strength = "Weak";
        color = "bg-red-500";
        width = "25%";
        break;
      case 3:
        strength = "Fair";
        color = "bg-yellow-400";
        width = "50%";
        break;
      case 4:
        strength = "Good";
        color = "bg-blue-500";
        width = "75%";
        break;
      case 5:
        strength = "Strong";
        color = "bg-green-500";
        width = "100%";
        break;
      default:
        strength = "Very Weak";
        color = "bg-red-600";
        width = "15%";
    }

    strengthText.textContent = strength;
    strengthText.className = "text-xs font-semibold " + color.replace("bg", "text");

    strengthBar.style.width = width;
    strengthBar.className = "h-2 rounded-full transition-all duration-300 " + color;
  }

