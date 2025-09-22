// Enhanced Progressive Disclosure UI System
class ProgressiveDisclosure {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.sections = [];
        this.currentSection = 0;
        if (this.form) this.init();
    }

    init() {
        // Find all collapsible sections
        this.sections = Array.from(this.form.querySelectorAll('[data-section]'));
        
        if (this.sections.length === 0) return;

        // Set up sections
        this.sections.forEach((section, index) => {
            const header = section.querySelector('[data-section-header]');
            const content = section.querySelector('[data-section-content]');
            
            if (index === 0) {
                this.expandSection(section);
            } else {
                this.collapseSection(section);
            }
            
            // Add click handler to header
            if (header) {
                header.style.cursor = 'pointer';
                header.onclick = () => this.toggleSection(section);
            }
            
            // Add completion detection
            this.addCompletionDetection(section, index);
        });
    }

    expandSection(section) {
        const content = section.querySelector('[data-section-content]');
        const arrow = section.querySelector('.section-arrow');
        
        if (content) {
            content.classList.remove('hidden');
            content.style.display = 'block';
        }
        
        if (arrow) {
            arrow.textContent = '▼';
        }
        
        section.classList.add('section-expanded');
    }

    collapseSection(section) {
        const content = section.querySelector('[data-section-content]');
        const arrow = section.querySelector('.section-arrow');
        
        if (content) {
            content.classList.add('hidden');
            content.style.display = 'none';
        }
        
        if (arrow) {
            arrow.textContent = '▶';
        }
        
        section.classList.remove('section-expanded');
    }

    toggleSection(section) {
        if (section.classList.contains('section-expanded')) {
            this.collapseSection(section);
        } else {
            this.expandSection(section);
        }
    }

    addCompletionDetection(section, index) {
        const inputs = section.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                if (this.isSectionComplete(section)) {
                    this.markSectionComplete(section);
                    
                    // Auto-expand next section
                    if (index < this.sections.length - 1) {
                        this.expandSection(this.sections[index + 1]);
                    }
                }
            });
        });
    }

    isSectionComplete(section) {
        const requiredInputs = section.querySelectorAll('[required]');
        return Array.from(requiredInputs).every(input => {
            if (input.type === 'checkbox') return input.checked;
            return input.value.trim() !== '';
        });
    }

    markSectionComplete(section) {
        const header = section.querySelector('[data-section-header]');
        if (header && !header.querySelector('.completion-check')) {
            const check = document.createElement('span');
            check.className = 'completion-check text-green-400 ml-2';
            check.textContent = '✓';
            header.appendChild(check);
        }
    }

    showAllSections() {
        this.sections.forEach(section => this.expandSection(section));
    }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    const progressiveForms = document.querySelectorAll('[data-progressive-form]');
    progressiveForms.forEach(form => {
        new ProgressiveDisclosure(form.id);
    });
});
