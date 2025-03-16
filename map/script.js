// Initialize the map
var map = L.map('map').setView([17.3850, 78.4867], 7); // Centered in Andhra Pradesh

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Function to determine marker color based on water quality
function getColor(bod) {
    return bod > 50 ? "red" :
           bod > 20 ? "orange" :
           bod > 10 ? "yellow" :
                      "green";
}

// Load JSON data
fetch("waterquality_map.json")
    .then(response => response.json())
    .then(data => {
        data.forEach(station => {
            let lat = station.lat;
            let lng = station.lon;

            // Only plot markers if latitude and longitude are available
            if (lat !== null && lng !== null) {
                let bod = parseFloat(station["B.O.D. (mg/l)"]); // Convert BOD to a float

                L.circleMarker([lat, lng], {
                    radius: 8,
                    color: getColor(bod),
                    fillColor: getColor(bod),
                    fillOpacity: 0.7
                }).addTo(map)
                  .bindPopup(`
                    <b>Location:</b> ${station.LOCATIONS}<br>
                    <b>State:</b> ${station.STATE}<br>
                    <b>B.O.D.:</b> ${bod} mg/l
                  `);
            }
        });
    })
    .catch(error => console.error("Error loading data:", error));
