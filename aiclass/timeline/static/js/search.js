/**
 * Search functionality for the Historical Time Machine
 * Handles search suggestions and enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="q"]');
    const searchForm = document.querySelector('.search-form');
    
    if (searchInput && searchForm) {
        // Add search input enhancements
        setupSearchEnhancements(searchInput, searchForm);
        
        // Add keyboard shortcuts
        setupKeyboardShortcuts(searchInput);
        
        console.log('Search functionality initialized');
    }
});

/**
 * Set up search input enhancements
 */
function setupSearchEnhancements(input, form) {
    // Auto-focus search input on page load (except on mobile)
    if (window.innerWidth > 768) {
        input.focus();
    }
    
    // Add search validation
    form.addEventListener('submit', function(e) {
        const query = input.value.trim();
        
        if (query.length === 0) {
            e.preventDefault();
            showSearchError('Please enter a search term');
            return;
        }
        
        if (query.length < 2) {
            e.preventDefault();
            showSearchError('Search term must be at least 2 characters long');
            return;
        }
        
        // Show loading state
        showSearchLoading(form);
    });
    
    // Clear error states on input
    input.addEventListener('input', function() {
        clearSearchError();
    });
    
    // Add search suggestions on input
    let searchTimeout;
    input.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => {
                showSearchSuggestions(query, input);
            }, 300);
        } else {
            hideSearchSuggestions();
        }
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-form')) {
            hideSearchSuggestions();
        }
    });
}

/**
 * Set up keyboard shortcuts
 */
function setupKeyboardShortcuts(input) {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            input.focus();
            input.select();
        }
        
        // Escape to clear search
        if (e.key === 'Escape' && document.activeElement === input) {
            input.value = '';
            input.blur();
            hideSearchSuggestions();
        }
    });
}

/**
 * Show search error message
 */
function showSearchError(message) {
    clearSearchError();
    
    const searchForm = document.querySelector('.search-form');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger mt-2 search-error';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${message}`;
    
    searchForm.appendChild(errorDiv);
    
    // Auto-hide after 3 seconds
    setTimeout(clearSearchError, 3000);
}

/**
 * Clear search error message
 */
function clearSearchError() {
    const errorDiv = document.querySelector('.search-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Show loading state during search
 */
function showSearchLoading(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
    submitButton.disabled = true;
    
    // Reset after 5 seconds (in case something goes wrong)
    setTimeout(() => {
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    }, 5000);
}

/**
 * Show search suggestions (simple implementation)
 */
function showSearchSuggestions(query, input) {
    // Simple suggestions based on common historical terms
    const suggestions = [
        'French Revolution', 'American Revolution', 'Industrial Revolution',
        'World War I', 'World War II', 'Cold War',
        'Renaissance', 'Medieval Period', 'Ancient Rome',
        'Space Race', 'Great Depression', 'Civil Rights Movement',
        'Napoleon', 'Alexander the Great', 'Julius Caesar',
        'Leonardo da Vinci', 'Galileo', 'Newton'
    ];
    
    // Filter suggestions based on query
    const filteredSuggestions = suggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(query.toLowerCase()) &&
        suggestion.toLowerCase() !== query.toLowerCase()
    ).slice(0, 5);
    
    if (filteredSuggestions.length > 0) {
        showSuggestionsList(filteredSuggestions, input);
    } else {
        hideSearchSuggestions();
    }
}

/**
 * Show suggestions list
 */
function showSuggestionsList(suggestions, input) {
    hideSearchSuggestions(); // Remove existing suggestions
    
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'search-suggestions position-absolute w-100 bg-dark border rounded mt-1';
    suggestionsDiv.style.zIndex = '1000';
    suggestionsDiv.style.top = '100%';
    
    suggestions.forEach(suggestion => {
        const suggestionItem = document.createElement('a');
        suggestionItem.className = 'suggestion-item d-block text-decoration-none text-light p-2 border-bottom';
        suggestionItem.href = `/search?q=${encodeURIComponent(suggestion)}`;
        suggestionItem.innerHTML = `<i class="fas fa-search me-2 text-muted"></i>${suggestion}`;
        
        suggestionItem.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'var(--bs-primary)';
        });
        
        suggestionItem.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
        });
        
        suggestionsDiv.appendChild(suggestionItem);
    });
    
    // Position relative to input
    const inputGroup = input.closest('.input-group');
    inputGroup.style.position = 'relative';
    inputGroup.appendChild(suggestionsDiv);
}

/**
 * Hide search suggestions
 */
function hideSearchSuggestions() {
    const suggestionsDiv = document.querySelector('.search-suggestions');
    if (suggestionsDiv) {
        suggestionsDiv.remove();
    }
}

/**
 * Add search keyboard navigation
 */
function setupSuggestionNavigation(input) {
    let currentSelection = -1;
    
    input.addEventListener('keydown', function(e) {
        const suggestions = document.querySelectorAll('.suggestion-item');
        
        if (suggestions.length === 0) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentSelection = Math.min(currentSelection + 1, suggestions.length - 1);
                updateSuggestionSelection(suggestions, currentSelection);
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                currentSelection = Math.max(currentSelection - 1, -1);
                updateSuggestionSelection(suggestions, currentSelection);
                break;
                
            case 'Enter':
                if (currentSelection >= 0 && suggestions[currentSelection]) {
                    e.preventDefault();
                    suggestions[currentSelection].click();
                }
                break;
                
            case 'Escape':
                hideSearchSuggestions();
                currentSelection = -1;
                break;
        }
    });
}

/**
 * Update suggestion selection highlight
 */
function updateSuggestionSelection(suggestions, selectedIndex) {
    suggestions.forEach((suggestion, index) => {
        if (index === selectedIndex) {
            suggestion.style.backgroundColor = 'var(--bs-primary)';
        } else {
            suggestion.style.backgroundColor = 'transparent';
        }
    });
}

// Add CSS for search suggestions
const style = document.createElement('style');
style.textContent = `
    .search-suggestions {
        max-height: 300px;
        overflow-y: auto;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    
    .suggestion-item:last-child {
        border-bottom: none !important;
    }
    
    .suggestion-item:hover {
        background-color: var(--bs-primary) !important;
    }
    
    .search-error {
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Search input focus effects */
    .search-form .form-control:focus {
        box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
        border-color: var(--bs-primary);
    }
    
    /* Responsive search suggestions */
    @media (max-width: 768px) {
        .search-suggestions {
            font-size: 0.9rem;
        }
        
        .suggestion-item {
            padding: 0.75rem !important;
        }
    }
`;
document.head.appendChild(style);
