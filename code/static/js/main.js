// AudEasy Main JavaScript - Phase 6 Week 1
document.addEventListener('DOMContentLoaded', function() {
    console.log('AudEasy initialized');
    initializeNavigation();
    initializeTimeDisplay();
    initializePWA();
});

function initializeNavigation() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });
}

function initializeTimeDisplay() {
    function updateTime() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = `${hours}:${minutes}`;
        }
    }
    updateTime();
    setInterval(updateTime, 60000);
}

let deferredPrompt;
function initializePWA() {
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
    });
}
