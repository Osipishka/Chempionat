document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.nav_button');
    const panels = document.querySelectorAll('.panel');

    function switchPanel(targetId) {
        panels.forEach(panel => {
            panel.style.display = 'none';
        });
        navButtons.forEach(button => {
            button.classList.remove('active');
        });
        document.getElementById(targetId).style.display = 'block';
        document.querySelector(`[data-target="${targetId}"]`).classList.add('active');
    }
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            switchPanel(target);
        });
    });

    if (navButtons.length > 0) {
        const firstTarget = navButtons[0].getAttribute('data-target');
        switchPanel(firstTarget);
    }
});