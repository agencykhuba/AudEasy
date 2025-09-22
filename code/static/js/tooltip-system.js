// Enhanced Comprehensive Tooltip & Help System
class TooltipSystem {
    constructor() {
        this.tooltips = this.getTooltipContent();
        this.activeTooltip = null;
        this.init();
    }

    getTooltipContent() {
        return {
            'car_description': {
                title: 'Writing Effective CAR Descriptions',
                content: `
                    <h4 class="font-semibold mb-2">Best Practices:</h4>
                    <ul class="list-disc pl-5 space-y-1 text-sm">
                        <li><strong>What:</strong> Clearly state the non-conformance</li>
                        <li><strong>When:</strong> Include date and time</li>
                        <li><strong>Where:</strong> Specify exact location</li>
                        <li><strong>Why:</strong> Explain the impact</li>
                    </ul>
                    <div class="mt-3 p-2 bg-blue-900/30 rounded text-sm">
                        <strong>Example:</strong> "During morning inspection at 8:30 AM, walk-in cooler temperature was 8°C (should be 4°C). This creates bacterial growth risk."
                    </div>
                `
            },
            'severity': {
                title: 'Severity Levels',
                content: `
                    <div class="space-y-2 text-sm">
                        <div class="p-2 border-l-4 border-red-500 bg-red-900/20">
                            <strong>Critical:</strong> Immediate food safety risk
                        </div>
                        <div class="p-2 border-l-4 border-orange-500 bg-orange-900/20">
                            <strong>Major:</strong> Regulatory violation
                        </div>
                        <div class="p-2 border-l-4 border-yellow-500 bg-yellow-900/20">
                            <strong>Minor:</strong> Improvement opportunity
                        </div>
                    </div>
                `
            },
            'root_cause': {
                title: 'Root Cause Analysis',
                content: `
                    <p class="mb-2 text-sm">Use the 5 Whys method:</p>
                    <ol class="list-decimal pl-5 space-y-1 text-sm">
                        <li>Why did it happen?</li>
                        <li>Why did that occur?</li>
                        <li>Why did that fail?</li>
                        <li>Why wasn't it prevented?</li>
                        <li>Root cause identified!</li>
                    </ol>
                `
            }
        };
    }

    init() {
        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('[data-tooltip]');
            if (trigger) {
                e.preventDefault();
                const topic = trigger.dataset.tooltip;
                this.showTooltip(topic, trigger);
            } else if (!e.target.closest('.tooltip-popup')) {
                this.closeTooltip();
            }
        });

        // Keyboard shortcut
        document.addEventListener('keydown', (e) => {
            if (e.key === '?' && !e.target.matches('input, textarea')) {
                this.showKeyboardShortcuts();
            }
        });
    }

    showTooltip(topic, triggerElement) {
        this.closeTooltip();
        
        const content = this.tooltips[topic];
        if (!content) return;

        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-popup fixed bg-gray-800 border border-gray-600 rounded-lg p-4 shadow-xl z-50 max-w-md';
        tooltip.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-semibold text-white">${content.title}</h3>
                <button class="text-gray-400 hover:text-white ml-2" onclick="this.closest('.tooltip-popup').remove()">×</button>
            </div>
            <div class="text-gray-300">
                ${content.content}
            </div>
        `;

        const rect = triggerElement.getBoundingClientRect();
        tooltip.style.top = `${rect.bottom + 10}px`;
        tooltip.style.left = `${Math.max(10, rect.left)}px`;

        document.body.appendChild(tooltip);
        this.activeTooltip = tooltip;
    }

    closeTooltip() {
        if (this.activeTooltip) {
            this.activeTooltip.remove();
            this.activeTooltip = null;
        }
    }

    showKeyboardShortcuts() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black/50 flex items-center justify-center z-[100]';
        modal.innerHTML = `
            <div class="bg-gray-800 rounded-lg p-6 max-w-md">
                <h2 class="text-xl font-bold mb-4">Keyboard Shortcuts</h2>
                <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                        <kbd class="px-2 py-1 bg-gray-700 rounded">?</kbd>
                        <span>Show this help</span>
                    </div>
                    <div class="flex justify-between">
                        <kbd class="px-2 py-1 bg-gray-700 rounded">Ctrl+Enter</kbd>
                        <span>Submit form</span>
                    </div>
                </div>
                <button onclick="this.closest('.fixed').remove()" 
                    class="mt-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded w-full">
                    Close
                </button>
            </div>
        `;
        document.body.appendChild(modal);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.tooltipSystem = new TooltipSystem();
});
