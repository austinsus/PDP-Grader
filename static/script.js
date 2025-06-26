// Website Content Analyzer JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const analyzeForm = document.getElementById('analyzeForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const urlInput = document.getElementById('url');

    if (analyzeForm && analyzeBtn) {
        // Handle form submission
        analyzeForm.addEventListener('submit', function(e) {
            const url = urlInput.value.trim();
            
            // Basic URL validation
            if (!url) {
                e.preventDefault();
                showAlert('Please enter a URL', 'danger');
                return;
            }
            
            // Show loading state
            showLoadingState();
        });

        // Auto-dismiss alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    // URL input formatting
    if (urlInput) {
        urlInput.addEventListener('blur', function() {
            let url = this.value.trim();
            if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
                this.value = 'https://' + url;
            }
        });
    }
});

function showLoadingState() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const spinner = analyzeBtn.querySelector('.spinner-border');
    
    if (analyzeBtn && btnText && spinner) {
        analyzeBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        spinner.classList.remove('d-none');
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    const firstCard = container.querySelector('.card');
    container.insertBefore(alertDiv, firstCard);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Progress bar animations
document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
            bar.style.transition = 'width 1s ease-in-out';
        }, 300);
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
