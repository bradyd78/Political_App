// map.js - Interactive Political Map

document.addEventListener("DOMContentLoaded", () => {
  // Initialize the map centered on the United States
  const map = L.map('map').setView([39.8283, -98.5795], 4);

  // Layer groups for different map styles
  const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  });

  const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri',
    maxZoom: 19
  });

  const terrainLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; OpenTopoMap contributors',
    maxZoom: 17
  });

  // Default to street map
  streetLayer.addTo(map);

  // State Capitals Data (sample of major state capitals)
  const stateCapitals = [
    { name: "Washington, D.C.", state: "Federal District", lat: 38.9072, lng: -77.0369, pop: "700,000", type: "capital", info: "U.S. Capital - Home to federal government" },
    { name: "Sacramento", state: "California", lat: 38.5816, lng: -121.4944, pop: "525,000", type: "capital", info: "Capital of California - Most populous state" },
    { name: "Austin", state: "Texas", lat: 30.2672, lng: -97.7431, pop: "978,000", type: "capital", info: "Capital of Texas - Tech hub and cultural center" },
    { name: "Albany", state: "New York", lat: 42.6526, lng: -73.7562, pop: "100,000", type: "capital", info: "Capital of New York - Historic Hudson River city" },
    { name: "Tallahassee", state: "Florida", lat: 30.4383, lng: -84.2807, pop: "196,000", type: "capital", info: "Capital of Florida - Home to FSU and FAMU" },
    { name: "Springfield", state: "Illinois", lat: 39.7817, lng: -89.6501, pop: "114,000", type: "capital", info: "Capital of Illinois - Lincoln's hometown" },
    { name: "Boston", state: "Massachusetts", lat: 42.3601, lng: -71.0589, pop: "695,000", type: "capital", info: "Capital of Massachusetts - Cradle of American Revolution" },
    { name: "Atlanta", state: "Georgia", lat: 33.7490, lng: -84.3880, pop: "498,000", type: "capital", info: "Capital of Georgia - Major Southern metropolis" },
    { name: "Denver", state: "Colorado", lat: 39.7392, lng: -104.9903, pop: "716,000", type: "capital", info: "Capital of Colorado - Mile High City" },
    { name: "Phoenix", state: "Arizona", lat: 33.4484, lng: -112.0740, pop: "1,660,000", type: "capital", info: "Capital of Arizona - Fastest growing major city" },
    { name: "Olympia", state: "Washington", lat: 47.0379, lng: -122.9007, pop: "55,000", type: "capital", info: "Capital of Washington - Pacific Northwest gem" },
    { name: "Salem", state: "Oregon", lat: 44.9429, lng: -123.0351, pop: "175,000", type: "capital", info: "Capital of Oregon - Willamette Valley location" }
  ];

  // Major Cities (non-capitals)
  const majorCities = [
    { name: "New York City", state: "New York", lat: 40.7128, lng: -74.0060, pop: "8,336,000", type: "city", info: "Largest U.S. city - Global financial center" },
    { name: "Los Angeles", state: "California", lat: 34.0522, lng: -118.2437, pop: "3,979,000", type: "city", info: "Second largest city - Entertainment capital" },
    { name: "Chicago", state: "Illinois", lat: 41.8781, lng: -87.6298, pop: "2,746,000", type: "city", info: "Third largest city - Midwest hub" },
    { name: "Houston", state: "Texas", lat: 29.7604, lng: -95.3698, pop: "2,304,000", type: "city", info: "Fourth largest city - Energy capital" },
    { name: "Philadelphia", state: "Pennsylvania", lat: 39.9526, lng: -75.1652, pop: "1,584,000", type: "city", info: "Birthplace of American democracy" },
    { name: "San Francisco", state: "California", lat: 37.7749, lng: -122.4194, pop: "874,000", type: "city", info: "Tech hub - Golden Gate Bridge" },
    { name: "Seattle", state: "Washington", lat: 47.6062, lng: -122.3321, pop: "753,000", type: "city", info: "Emerald City - Tech and coffee capital" },
    { name: "Miami", state: "Florida", lat: 25.7617, lng: -80.1918, pop: "467,000", type: "city", info: "Gateway to Latin America" }
  ];

  // Congressional District Examples
  const congressionalDistricts = [
    { name: "CA-12", state: "California", lat: 37.7749, lng: -122.4194, representative: "Rep. Nancy Pelosi (D)", type: "district", info: "San Francisco area district" },
    { name: "NY-14", state: "New York", lat: 40.7489, lng: -73.9680, representative: "Rep. Alexandria Ocasio-Cortez (D)", type: "district", info: "Parts of Bronx and Queens" },
    { name: "TX-21", state: "Texas", lat: 30.2672, lng: -98.7431, representative: "Rep. Chip Roy (R)", type: "district", info: "Central Texas district" },
    { name: "FL-27", state: "Florida", lat: 25.7617, lng: -80.3568, representative: "Rep. Maria Elvira Salazar (R)", type: "district", info: "Miami area district" }
  ];

  // Marker groups
  let capitalMarkers = L.layerGroup();
  let cityMarkers = L.layerGroup();
  let districtMarkers = L.layerGroup();

  // Create custom icons
  const capitalIcon = L.divIcon({
    className: 'custom-icon',
    html: '<div style="background: #667eea; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });

  const cityIcon = L.divIcon({
    className: 'custom-icon',
    html: '<div style="background: #28a745; width: 16px; height: 16px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  });

  const districtIcon = L.divIcon({
    className: 'custom-icon',
    html: '<div style="background: #dc3545; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });

  // Add state capitals
  stateCapitals.forEach(capital => {
    const marker = L.marker([capital.lat, capital.lng], { icon: capitalIcon })
      .bindPopup(`
        <div class="marker-popup">
          <h4>🏛️ ${capital.name}</h4>
          <p><strong>State:</strong> ${capital.state}</p>
          <p><strong>Population:</strong> ${capital.pop}</p>
          <p><strong>Info:</strong> ${capital.info}</p>
        </div>
      `);
    capitalMarkers.addLayer(marker);
  });

  // Add major cities
  majorCities.forEach(city => {
    const marker = L.marker([city.lat, city.lng], { icon: cityIcon })
      .bindPopup(`
        <div class="marker-popup">
          <h4>🏙️ ${city.name}</h4>
          <p><strong>State:</strong> ${city.state}</p>
          <p><strong>Population:</strong> ${city.pop}</p>
          <p><strong>Info:</strong> ${city.info}</p>
        </div>
      `);
    cityMarkers.addLayer(marker);
  });

  // Add congressional districts
  congressionalDistricts.forEach(district => {
    const marker = L.marker([district.lat, district.lng], { icon: districtIcon })
      .bindPopup(`
        <div class="marker-popup">
          <h4>📍 ${district.name}</h4>
          <p><strong>State:</strong> ${district.state}</p>
          <p><strong>Representative:</strong> ${district.representative}</p>
          <p><strong>Info:</strong> ${district.info}</p>
        </div>
      `);
    districtMarkers.addLayer(marker);
  });

  // Add default markers (capitals)
  capitalMarkers.addTo(map);

  // Handle marker type selection
  document.getElementById('markerType').addEventListener('change', function(e) {
    const value = e.target.value;
    
    // Remove all markers
    map.removeLayer(capitalMarkers);
    map.removeLayer(cityMarkers);
    map.removeLayer(districtMarkers);
    
    // Add selected markers
    switch(value) {
      case 'capitals':
        capitalMarkers.addTo(map);
        break;
      case 'major-cities':
        cityMarkers.addTo(map);
        break;
      case 'representatives':
        districtMarkers.addTo(map);
        break;
      case 'all':
        capitalMarkers.addTo(map);
        cityMarkers.addTo(map);
        districtMarkers.addTo(map);
        break;
    }
  });

  // Handle map style selection
  document.getElementById('mapStyle').addEventListener('change', function(e) {
    const value = e.target.value;
    
    // Remove all layers
    map.removeLayer(streetLayer);
    map.removeLayer(satelliteLayer);
    map.removeLayer(terrainLayer);
    
    // Add selected layer
    switch(value) {
      case 'street':
        streetLayer.addTo(map);
        break;
      case 'satellite':
        satelliteLayer.addTo(map);
        break;
      case 'terrain':
        terrainLayer.addTo(map);
        break;
    }
  });

  // Add zoom controls feedback
  map.on('zoomend', function() {
    const zoom = map.getZoom();
    if (zoom > 6) {
      // At higher zoom levels, could show more detailed markers
      console.log('Zoomed in to level:', zoom);
    }
  });

  console.log('Interactive map loaded successfully!');
});
