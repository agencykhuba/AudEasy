// Tooltip System
class TooltipSystem {
    constructor() {
        this.init();
    }
    init() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-tooltip]')) {
                const topic = e.target.closest('[data-tooltip]').dataset.tooltip;
                alert('Help for: ' + topic);
            }
        });
    }
}
const tooltipSystem = new TooltipSystem();
