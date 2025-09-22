// Enhanced Screenshot Bug Reporting System
class FeedbackSystem {
    constructor() {
        this.isCapturing = false;
        this.init();
    }

    init() {
        // Create floating feedback button
        const button = document.createElement('button');
        button.id = 'feedbackButton';
        button.innerHTML = 'í³¸ Report Issue';
        button.className = 'fixed bottom-4 right-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 transition';
        button.onclick = () => this.showFeedbackModal();
        document.body.appendChild(button);
    }

    showFeedbackModal() {
        const modal = document.createElement('div');
        modal.id = 'feedbackModal';
        modal.className = 'fixed inset-0 bg-black/80 flex items-center justify-center z-[100] p-4';
        modal.innerHTML = `
            <div class="bg-gray-800 rounded-lg max-w-2xl w-full p-6">
                <h2 class="text-xl font-bold mb-4">Report an Issue</h2>
                
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">What went wrong?</label>
                    <textarea 
                        id="bugDescription" 
                        rows="4" 
                        class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-400"
                        placeholder="Describe what you were trying to do and what happened..."
                    ></textarea>
                </div>
                
                <div class="mb-4 p-3 bg-gray-700 rounded text-sm">
                    <strong>Auto-captured context:</strong>
                    <div class="mt-1 text-gray-400">
                        <div>Page: ${window.location.pathname}</div>
                        <div>Browser: ${navigator.userAgent.split(' ').slice(-2).join(' ')}</div>
                        <div>Time: ${new Date().toLocaleString()}</div>
                    </div>
                </div>
                
                <div class="flex justify-end gap-3">
                    <button onclick="document.getElementById('feedbackModal').remove()" 
                        class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition">
                        Cancel
                    </button>
                    <button onclick="feedbackSystem.submitReport()" 
                        class="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg transition">
                        Submit Report
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    async submitReport() {
        const description = document.getElementById('bugDescription').value;
        
        if (!description.trim()) {
            alert('Please describe the issue before submitting.');
            return;
        }

        const reportData = {
            description: description,
            page_url: window.location.href,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };

        try {
            const response = await fetch('/feedback/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(reportData)
            });

            const result = await response.json();

            if (result.success) {
                alert('âœ… Thank you! Your feedback has been submitted.');
                document.getElementById('feedbackModal').remove();
            } else {
                alert('âŒ Failed to submit report. Please try again.');
            }
        } catch (error) {
            console.error('Report submission failed:', error);
            alert('âŒ Network error. Please try again.');
        }
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.feedbackSystem = new FeedbackSystem();
    });
} else {
    window.feedbackSystem = new FeedbackSystem();
}
