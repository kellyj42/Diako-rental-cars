function checkPasswordMatch() {
  const password1 = document.getElementById("password1").value;
  const password2 = document.getElementById("password2").value;
  const matchText = document.getElementById("passwordMatch");

  if (!password2) {
    matchText.textContent = "";
    return;
  }

  if (password1 === password2) {
    matchText.innerHTML = `
        <span class="text-green-600 flex items-center gap-2">
          <i class="fas fa-check-circle"></i> Passwords match
        </span>
      `;
  } else {
    matchText.innerHTML = `
        <span class="text-red-600 flex items-center gap-2">
          <i class="fas fa-times-circle"></i> Passwords do not match
        </span>
      `;
  }
}
