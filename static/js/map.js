/**
 * Initialize map and add markers.
 */
document.addEventListener("DOMContentLoaded", function() {
    // Initialize map
    var map = L.map('map').setView([37.0902, -95.7129], 3);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    /**
     * Add markers to the map.
     */
    function addMarkersToMap() {
        var mapElement = document.getElementById('map');
        var coordinates = JSON.parse(mapElement.getAttribute('data-coordinates'));
        coordinates.forEach(function(coordinate) {
            var popupContent = createMarkerPopupContent(coordinate);
            var icon = createMarkerIcon(coordinate);
            L.marker([coordinate.latitude, coordinate.longitude], { icon: icon })
                .bindPopup(popupContent)
                .addTo(map);
        });
    }
    addMarkersToMap();

    /**
     * Create popup content for markers.
     * @param {Object} coordinate - Coordinate data.
     * @returns {string} Popup HTML content.
     */
    function createMarkerPopupContent(coordinate) {
        // Determine icon based on type
        let iconHTML = '';
        if (coordinate.type === 'SuggestedDestination') {
            iconHTML = '<i class="material-icons" style="color:#0b7bc3;">flight_takeoff</i>';
        } else if (coordinate.type === 'TraveledFrom') {
            iconHTML = '<i class="material-icons" style="color:#0bc336;">public</i>';
        } else {
            iconHTML = '<i class="material-icons" style="color:#808080;">help_outline</i>';
        }
    
        // Format created_on date
        const createdOn = coordinate.created_on ? new Date(coordinate.created_on).toLocaleString() : new Date().toLocaleString();
    
        // Construct popup content
        return `
            <div class="popup-container">
                <div class="popup-summary">Summary</div>
                <div class="popup-content">
                    <div class="popup-header">${iconHTML}&nbsp;&nbsp;${coordinate.type.replaceAll('From', ' From')}</div>
                    <div><b>Latitude:</b> ${coordinate.latitude}</div>
                    <div><b>Longitude:</b> ${coordinate.longitude}</div>
                    <div><b>Created By:</b> ${coordinate.created_by}</div>
                    <div><b>Created On:</b> ${createdOn}</div>
                </div>
            </div>
        `;
    }
    
    /**
     * Create custom marker icon.
     * @param {Object} coordinate - Coordinate data.
     * @returns {Object} Leaflet icon object.
     */
    function createMarkerIcon(coordinate) {
        let iconHTML = '';
        if (coordinate.type === 'SuggestedDestination') {
            iconHTML = `
                <div class="marker-pin" style="background-color:#0b7bc3;"></div>
                <i class="material-icons" style="color:#0b7bc3;">flight_takeoff</i>
            `;
        } else if (coordinate.type === 'TraveledFrom') {
            iconHTML = `
                <div class="marker-pin" style="background-color:#0bc336;"></div>
                <i class="material-icons" style="color:#0bc336;">public</i>
            `;
        } else {
            iconHTML = `
                <div class="marker-pin" style="background-color:#808080;"></div>
                <i class="material-icons" style="color:#808080;">help_outline</i>
            `;
        }
        return L.divIcon({
            className: 'custom-div-icon',
            html: iconHTML,
            iconSize: [30, 42],
            iconAnchor: [15, 42]
        });
    }    

    // Event listener for map click
    map.on('click', function(e) {
        var latlng = e.latlng;
        var contentElement = createPopupContent(latlng);
        L.popup().setLatLng(latlng).setContent(contentElement).openOn(map);
    });

    /**
     * Create popup content for map click.
     * @param {Object} latlng - Latitude and longitude object.
     * @returns {HTMLElement} Popup content element.
     */
    function createPopupContent(latlng) {
        var contentElement = document.createElement('div');
        contentElement.classList.add('custom-popup');

        contentElement.innerHTML = `
            <div class="popup-header">Confirm Location</div>
            <div>You clicked the map at ${latlng.lat.toFixed(2)}, ${latlng.lng.toFixed(2)}</div>
            <div class="checkbox-container">
                <label>
                    <input type="checkbox" name="type" value="TraveledFrom"> Traveled From
                </label>
                <label>
                    <input type="checkbox" name="type" value="SuggestedDestination"> Suggested Destination
                </label>
            </div>
        `;

        var confirmButton = document.createElement('button');
        confirmButton.innerText = 'Confirm';
        confirmButton.classList.add('confirm-button');
        confirmButton.addEventListener('click', () => handleConfirmButtonClick(latlng, contentElement));

        manageCheckboxSelection(contentElement);

        contentElement.appendChild(confirmButton);
        return contentElement;
    }

    /**
     * Handle confirm button click.
     * @param {Object} latlng - Latitude and longitude object.
     * @param {HTMLElement} contentElement - Popup content element.
     */
    function handleConfirmButtonClick(latlng, contentElement) {
        var nameInput = document.getElementById('participantName').value;
        var checkboxes = document.querySelectorAll('input[type="checkbox"][name="type"]:checked');
        var type = checkboxes.length > 0 ? checkboxes[0].value : null;
        var errorMessageElement = manageErrorMessage(contentElement, '');

        if (checkboxes.length === 1 && nameInput.trim() !== "") {
            updateSelection(latlng.lat, latlng.lng, nameInput, type);
        } else {
            displayValidationErrors(checkboxes, nameInput, errorMessageElement);
        }
    }

    /**
     * Manage error message display.
     * @param {HTMLElement} contentElement - Popup content element.
     * @param {string} initialMessage - Initial error message.
     * @returns {HTMLElement} Error message element.
     */
    function manageErrorMessage(contentElement, initialMessage) {
        var errorMessageElement = document.getElementById('errorMessage');
        if (!errorMessageElement) {
            errorMessageElement = document.createElement('div');
            errorMessageElement.setAttribute('id', 'errorMessage');
            contentElement.appendChild(errorMessageElement);
        }
        errorMessageElement.textContent = initialMessage;
        return errorMessageElement;
    }

    /**
     * Display validation errors.
     * @param {NodeList} checkboxes - Checked checkboxes.
     * @param {string} nameInput - Participant name input.
     * @param {HTMLElement} errorMessageElement - Error message element.
     */
    function displayValidationErrors(checkboxes, nameInput, errorMessageElement) {
        var errors = [];
        if (checkboxes.length !== 1) {
            errors.push("Please select one option.");
        }
        if (nameInput.trim() === "") {
            errors.push("Please enter your name.");
        }
        errorMessageElement.textContent = errors.join(" ");
        errorMessageElement.style.color = 'red';
    }

    /**
     * Manage checkbox selection.
     * @param {HTMLElement} contentElement - Popup content element.
     */
    function manageCheckboxSelection(contentElement) {
        contentElement.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                contentElement.querySelectorAll('input[type="checkbox"]').forEach(function(box) {
                    if (box !== checkbox) box.checked = false;
                });
            });
        });
    }

    /**
     * Update selection.
     * @param {number} latitude - Latitude value.
     * @param {number} longitude - Longitude value.
     * @param {string} name - Participant name.
     * @param {string} type - Selection type.
     */
    async function updateSelection(latitude, longitude, name, type) {
        try {
            const response = await fetch('/explorer/update-selection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    latitude: parseFloat(latitude),
                    longitude: parseFloat(longitude), 
                    created_by: name, 
                    type: type,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error response:', errorData);
                alert(`Error: ${errorData.detail}`);
                return;
            }
            
            const data = await response.json();
            console.log(data.message);
            
            var popupContent = createMarkerPopupContent({
                type: type,
                latitude: latitude,
                longitude: longitude,
                created_by: name,
            });

            var icon = createMarkerIcon({ type: type });
            L.marker([latitude, longitude], { icon: icon })
                .bindPopup(popupContent)
                .addTo(map);

            map.closePopup();
        } catch (error) {
            console.error('Fetch error:', error);
            alert('An error occurred while updating the selection.');
        }
    }    
});
