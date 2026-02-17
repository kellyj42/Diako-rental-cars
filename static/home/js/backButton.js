/**
 * Back Button Navigation
 * Handles smart navigation to the previous page
 */

function goBack() {
  // Check if there's history to go back to
  if (window.history.length > 1) {
    window.history.back();
  } else {
    // If no history exists, redirect to home page
    window.location.href = "/";
  }
}

// Optional: Show/hide back button based on navigation history
document.addEventListener("DOMContentLoaded", function () {
  const backButton = document.getElementById("backButton");

  if (backButton) {
    // Hide back button if there's no history to go back to
    // (e.g., user landed directly on this page)
    if (window.history.length <= 1) {
      // Optionally hide the button or change its behavior
      // backButton.style.display = 'none';
    }
  }
});
