  function updateClock() {
    const now = new Date();

    const options = {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    };

    document.getElementById('live-clock').textContent =
      now.toLocaleDateString('en-US', options);
  }

  updateClock(); // initial call
  setInterval(updateClock, 1000); // update every second

