/**
 * Timeline JavaScript functionality
 * Handles map integration and interactive timeline features
 */

let map;
let markers = [];

/**
 * Initialize the timeline with map and event data
 */
function initializeTimeline(data) {
    // Initialize map
    initializeMap(data.timeline, data.events);
    
    // Set up event listeners
    setupEventListeners();
    
    // Add event IDs for navigation
    addEventNavigation(data.events);
    
    console.log('Timeline initialized with', data.events.length, 'events');
}

/**
 * Initialize the Leaflet map
 */
function initializeMap(timeline, events) {
    // Default coordinates - use timeline location or world center
    let defaultLat = timeline.coordinates?.lat || 20;
    let defaultLng = timeline.coordinates?.lng || 0;
    let defaultZoom = 2;
    
    // If timeline has specific location, zoom in more
    if (timeline.coordinates && timeline.coordinates.lat !== 0) {
        defaultZoom = 4;
    }
    
    // Initialize map
    map = L.map('historical-map').setView([defaultLat, defaultLng], defaultZoom);
    
    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);
    
    // Add markers for each event
    events.forEach((event, index) => {
        if (event.coordinates && event.coordinates.lat && event.coordinates.lng) {
            addEventMarker(event, index);
        }
    });
    
    // If we have events with coordinates, fit map to show all markers
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

/**
 * Add a marker for an event on the map
 */
function addEventMarker(event, index) {
    const marker = L.marker([event.coordinates.lat, event.coordinates.lng])
        .addTo(map)
        .bindPopup(`
            <div class="popup-content">
                <h6><span class="me-2">${event.avatar}</span>${event.title}</h6>
                <p class="mb-1"><strong>${event.date}</strong></p>
                <p class="mb-1">${event.description}</p>
                <small class="text-muted">${event.location}</small>
            </div>
        `);
    
    markers.push(marker);
    
    // Add click event to highlight corresponding timeline event
    marker.on('click', function() {
        highlightTimelineEvent(index);
    });
}

/**
 * Set up event listeners for interactive elements
 */
function setupEventListeners() {
    // Show on map buttons
    document.querySelectorAll('.show-on-map').forEach(button => {
        button.addEventListener('click', function() {
            const lat = parseFloat(this.dataset.lat);
            const lng = parseFloat(this.dataset.lng);
            const title = this.dataset.title;
            
            if (lat && lng) {
                map.setView([lat, lng], 8);
                
                // Find and open the corresponding marker popup
                markers.forEach(marker => {
                    const markerLat = marker.getLatLng().lat;
                    const markerLng = marker.getLatLng().lng;
                    
                    // Check if this is the right marker (with some tolerance for floating point comparison)
                    if (Math.abs(markerLat - lat) < 0.001 && Math.abs(markerLng - lng) < 0.001) {
                        marker.openPopup();
                    }
                });
            }
        });
    });
    
    // Timeline navigation links
    document.querySelectorAll('.timeline-nav-item').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'center' 
                });
                
                // Highlight the target event
                highlightTimelineEvent(targetId.replace('#event-', '') - 1);
            }
        });
    });
}

/**
 * Add navigation IDs to timeline events
 */
function addEventNavigation(events) {
    const timelineEvents = document.querySelectorAll('.timeline-event');
    timelineEvents.forEach((event, index) => {
        event.id = `event-${index + 1}`;
    });
}

/**
 * Highlight a specific timeline event
 */
function highlightTimelineEvent(index) {
    // Remove previous highlights
    document.querySelectorAll('.timeline-event').forEach(event => {
        event.classList.remove('highlighted');
    });
    
    // Add highlight to target event
    const targetEvent = document.querySelector(`#event-${index + 1}`);
    if (targetEvent) {
        targetEvent.classList.add('highlighted');
        
        // Remove highlight after a few seconds
        setTimeout(() => {
            targetEvent.classList.remove('highlighted');
        }, 3000);
    }
}
document.getElementById('historical-map')  // Check if it exists

/**
 * Handle map marker clicks to scroll to corresponding timeline event
 */
function scrollToTimelineEvent(eventIndex) {
    const targetEvent = document.querySelector(`#event-${eventIndex + 1}`);
    if (targetEvent) {
        targetEvent.scrollIntoView({ 
            behavior: 'smooth',
            block: 'center' 
        });
        highlightTimelineEvent(eventIndex);
    }
}

// Add CSS for highlighted events
const style = document.createElement('style');
style.textContent = `
    .timeline-event.highlighted .card {
        border-left: 4px solid var(--bs-primary);
        box-shadow: 0 0.5rem 1rem rgba(13, 110, 253, 0.25);
        transform: translateX(5px);
        transition: all 0.3s ease;
    }
    
    .popup-content h6 {
        margin-bottom: 0.5rem;
        color: var(--bs-light);
    }
    
    .popup-content p {
        margin-bottom: 0.25rem;
        color: var(--bs-light);
    }
    
    .popup-content small {
        color: var(--bs-secondary);
    }
`;
document.head.appendChild(style);

// Export functions for global access
window.initializeTimeline = initializeTimeline;
window.scrollToTimelineEvent = scrollToTimelineEvent;
