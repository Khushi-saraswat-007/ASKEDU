// JavaScript for plagiarism detector application

document.addEventListener('DOMContentLoaded', function() {
    // Character counter for content textarea
    const contentTextarea = document.getElementById('content');
    const charCountSpan = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisForm = document.getElementById('analysisForm');
    const fileInput = document.getElementById('file');

    // Update character count
    function updateCharCount() {
        const content = contentTextarea.value;
        const charCount = content.length;
        charCountSpan.textContent = charCount;
        
        // Update character count color based on minimum requirement
        if (charCount < 50) {
            charCountSpan.style.color = '#dc3545';
        } else {
            charCountSpan.style.color = '#28a745';
        }
    }

    // Initialize character count
    if (contentTextarea) {
        updateCharCount();
        contentTextarea.addEventListener('input', updateCharCount);
    }

    // Handle file upload
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Clear text area when file is selected
                if (contentTextarea) {
                    contentTextarea.value = '';
                    updateCharCount();
                }
                
                // Auto-detect content type based on file extension
                const fileName = file.name.toLowerCase();
                const codeExtensions = ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c'];
                const isCodeFile = codeExtensions.some(ext => fileName.endsWith(ext));
                
                const textRadio = document.getElementById('text');
                const codeRadio = document.getElementById('code');
                
                if (isCodeFile && codeRadio) {
                    codeRadio.checked = true;
                } else if (textRadio) {
                    textRadio.checked = true;
                }
                
                // Validate file size (16MB limit)
                const maxSize = 16 * 1024 * 1024; // 16MB
                if (file.size > maxSize) {
                    alert('File size exceeds 16MB limit. Please choose a smaller file.');
                    fileInput.value = '';
                    return;
                }
            }
        });
    }

    // Handle form submission
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            const content = contentTextarea.value.trim();
            const hasFile = fileInput && fileInput.files.length > 0;
            
            // Validate that either content or file is provided
            if (!content && !hasFile) {
                e.preventDefault();
                alert('Please provide content to analyze either by typing or uploading a file.');
                return;
            }
            
            // Validate content length if text is provided
            if (content && content.length < 50) {
                e.preventDefault();
                alert('Content must be at least 50 characters long for meaningful analysis.');
                return;
            }
            
            // Show loading state
            if (analyzeBtn) {
                analyzeBtn.disabled = true;
                analyzeBtn.classList.add('btn-loading');
                analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Copy content functionality (if needed)
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            // Show success message
            const toast = document.createElement('div');
            toast.className = 'toast position-fixed top-0 end-0 m-3';
            toast.innerHTML = `
                <div class="toast-body">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    Content copied to clipboard!
                </div>
            `;
            document.body.appendChild(toast);
            
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            
            // Remove toast after it's hidden
            toast.addEventListener('hidden.bs.toast', function() {
                document.body.removeChild(toast);
            });
        }).catch(function() {
            alert('Unable to copy to clipboard. Please copy manually.');
        });
    }

    // Add copy buttons to code blocks (if any)
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(codeBlock) {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Copy code';
        
        const container = codeBlock.closest('pre');
        container.style.position = 'relative';
        container.appendChild(copyBtn);
        
        copyBtn.addEventListener('click', function() {
            copyToClipboard(codeBlock.textContent);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter or Cmd+Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (analysisForm) {
                analysisForm.dispatchEvent(new Event('submit'));
            }
        }
    });

    // Initialize tooltips (if Bootstrap tooltips are used)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
