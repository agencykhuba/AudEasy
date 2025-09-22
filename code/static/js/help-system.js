// Contextual Help System
const helpTopics = {
    'car_description': {
        title: 'Writing Effective CAR Descriptions',
        content: `
            <h3 class="font-semibold mb-2">Best Practices:</h3>
            <ul class="list-disc pl-5 space-y-1 text-sm">
                <li><strong>What:</strong> Clearly state the non-conformance</li>
                <li><strong>When:</strong> Include date and time</li>
                <li><strong>Where:</strong> Specify exact location</li>
                <li><strong>Why:</strong> Explain the food safety impact</li>
                <li><strong>Evidence:</strong> Reference temperature logs, photos, etc.</li>
            </ul>
            <div class="mt-3 p-3 bg-blue-900/20 rounded">
                <strong>Example:</strong><br>
                "During morning inspection at 8:30 AM, walk-in cooler #2 temperature was 8°C (should be 4°C). Chicken and dairy products felt warm. This creates risk of bacterial growth."
            </div>
        `,
        video: '/help/videos/car-description.mp4'
    },
    'severity_levels': {
        title: 'Understanding Severity Levels',
        content: `
            <div class="space-y-3">
                <div class="p-3 border-l-4 border-red-500 bg-red-900/20">
                    <strong>Critical:</strong> Immediate food safety risk, potential for illness
                </div>
                <div class="p-3 border-l-4 border-orange-500 bg-orange-900/20">
                    <strong>Major:</strong> Significant regulatory violation, requires prompt action
                </div>
                <div class="p-3 border-l-4 border-yellow-500 bg-yellow-900/20">
                    <strong>Minor:</strong> Process improvement opportunity, no immediate risk
                </div>
            </div>
        `
    },
    'root_cause': {
        title: 'Root Cause Analysis',
        content: `
            <p class="mb-3">Use the 5 Whys method to identify the true root cause:</p>
            <ol class="list-decimal pl-5 space-y-2 text-sm">
                <li><strong>Why did it happen?</strong> Surface-level cause</li>
                <li><strong>Why did that cause occur?</strong> Contributing factor</li>
                <li><strong>Why did that factor exist?</strong> Systemic issue</li>
                <li><strong>Why did that issue persist?</strong> Process gap</li>
                <li><strong>Root Cause:</strong> Fundamental problem to fix</li>
            </ol>
        `
    }
};

function showContextualHelp(topic) {
    const help = helpTopics[topic];
    if (!help) return;
    
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="bg-gray-800 rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-start mb-4">
                    <h2 class="text-xl font-bold">${help.title}</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-white">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="text-gray-300">${help.content}</div>
                ${help.video ? `<div class="mt-4"><video controls class="w-full rounded"><source src="${help.video}" type="video/mp4"></video></div>` : ''}
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}
