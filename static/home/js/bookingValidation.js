document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (!form) return;

  const errorBox = document.getElementById("jsErrorBox");
  const errorList = document.getElementById("jsErrorList");

  const textPattern = /^[A-Za-z\s\-\.,']+$/;

  const pickUp = form.pick_up_location;
  const dropOff = form.drop_off_location;
  const pickDate = form.pick_up_date;
  const dropDate = form.drop_off_date;
  const pickTime = form.pick_up_time;
  const dropTime = form.drop_off_time;
  const agree = form.agree_terms;

  const fieldsToHighlight = [pickUp, dropOff, pickDate, dropDate];

  // -------------------------
  // UI HELPERS
  // -------------------------

  function showErrors(errors) {
    errorList.innerHTML = "";

    errors.forEach(msg => {
      const li = document.createElement("li");
      li.textContent = msg;
      errorList.appendChild(li);
    });

    errorBox.classList.remove("hidden");
    errorBox.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function clearErrors() {
    errorList.innerHTML = "";
    errorBox.classList.add("hidden");

    // remove red borders
    fieldsToHighlight.forEach(el => {
      if (!el) return;
      el.classList.remove("border-red-500");
    });
  }

  function markInvalid(field) {
    if (!field) return;
    field.classList.add("border-red-500");
  }

  function markValid(field) {
    if (!field) return;
    field.classList.remove("border-red-500");
  }

  // remove red border while user types
  fieldsToHighlight.forEach(el => {
    if (!el) return;
    el.addEventListener("input", () => markValid(el));
  });

  // -------------------------
  // SUBMIT VALIDATION
  // -------------------------

  form.addEventListener("submit", function (e) {
    clearErrors();

    const errors = [];

    const pickVal = pickUp.value.trim();
    const dropVal = dropOff.value.trim();

    // ---------- LOCATION ----------
    if (!textPattern.test(pickVal) || pickVal.length < 3) {
      errors.push("Pickup location must be at least 3 alphabetic characters.");
      markInvalid(pickUp);
    }

    if (!textPattern.test(dropVal) || dropVal.length < 3) {
      errors.push("Drop-off location must be at least 3 alphabetic characters.");
      markInvalid(dropOff);
    }

    // ---------- DATE ----------
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const pd = new Date(pickDate.value);
    const dd = new Date(dropDate.value);

    if (isNaN(pd.getTime())) {
      errors.push("Pickup date is invalid.");
      markInvalid(pickDate);
    } else if (pd < today) {
      errors.push("Pickup date cannot be in the past.");
      markInvalid(pickDate);
    }

    if (isNaN(dd.getTime())) {
      errors.push("Drop-off date is invalid.");
      markInvalid(dropDate);
    }

    if (!isNaN(pd.getTime()) && !isNaN(dd.getTime())) {
      if (dd < pd) {
        errors.push("Drop-off date must be after pickup date.");
        markInvalid(dropDate);
      }

      const diffDays = Math.ceil((dd - pd) / 86400000);
      if (diffDays > 60) {
        errors.push("Rental period cannot exceed 60 days.");
        markInvalid(dropDate);
      }
    }

    // ---------- TERMS ----------
    if (!agree.checked) {
      errors.push("You must accept the Terms & Conditions.");
    }

    // ---------- RESULT ----------
    if (errors.length) {
      e.preventDefault();
      showErrors(errors);

      // focus first invalid field
      const firstInvalid = form.querySelector(".border-red-500");
      if (firstInvalid) firstInvalid.focus();

      return false;
    }

    return true;
  });
});
