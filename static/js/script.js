// Sends the given action to the server without reloading the page.
function sendAction(action) {
    const formData = new URLSearchParams();
    formData.append("action", action);
    fetch('/run_action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    })
        .then(response => {
            if (!response.ok) {
                console.error('Error triggering action:', response.statusText);
            }
        })
        .catch(error => console.error('Fetch error:', error));
}

// For toggle-able buttons, we call this function.
function toggleAndSend(action, buttonElement) {
    sendAction(action);
    // Optimistically toggle appearance; however, the state is refreshed by polling.
    buttonElement.classList.toggle('active');
    updateFullscreenButton();
}

function getForegroundWindow() {
    fetch('/foreground_window')
        .then(response => response.json())
        .then(data => {
            const foregroundWindow = document.getElementById("foreground-window");
            if (data.title) {
                foregroundWindow.innerText = data.title;
            } else {
                foregroundWindow.innerText = "No window in foreground";
            }
        })
}

// Poll the /state endpoint and update the fullscreen button.
function updateFullscreenButton() {
    fetch('/state')
        .then(response => response.json())
        .then(data => {
            const fsButton = document.getElementById("fullscreen-button");
            if (data.fullscreen) {
                fsButton.classList.add("active");
            } else {
                fsButton.classList.remove("active");
            }
        })
        .catch(err => console.error('Error fetching state:', err));
}

// Start polling every 2 seconds.
setInterval(updateFullscreenButton, 2000);
setInterval(getForegroundWindow, 100);