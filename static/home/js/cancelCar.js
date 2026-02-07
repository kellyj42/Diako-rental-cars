  function openCancelDialog(e) {
    if (e) e.preventDefault();
    var mainCarInput = document.querySelector('input[name="car_id"]');
    if (!mainCarInput) return;
    var modal = document.getElementById("cancelModal");
    modal.dataset.carId = mainCarInput.value || "";
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    document.addEventListener("keydown", escHandler);
  }

  function closeCancelDialog() {
    var modal = document.getElementById("cancelModal");
    if (!modal) return;
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    delete modal.dataset.carId;
    document.removeEventListener("keydown", escHandler);
  }

  function confirmCancelSelection() {
    var modal = document.getElementById("cancelModal");
    var cancelId = document.getElementById("cancelCarId");
    var cancelForm = document.getElementById("cancelSelectionForm");
    if (!modal || !cancelId || !cancelForm) return;
    cancelId.value = modal.dataset.carId || "";
    cancelForm.submit();
  }

  function escHandler(e) {
    if (e.key === "Escape") closeCancelDialog();
  }