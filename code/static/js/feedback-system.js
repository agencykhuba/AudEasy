// Screenshot Bug Reporting
class FeedbackSystem {
    constructor() {
        this.init();
    }
    init() {
        const button = document.createElement('button');
        button.innerHTML = 'í³¸ Report Issue';
        button.className = 'fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        button.onclick = () => alert('Bug reporting coming soon!');
        document.body.appendChild(button);
    }
}
const feedbackSystem = new FeedbackSystem();
