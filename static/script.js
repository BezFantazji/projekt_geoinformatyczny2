const map = L.map('map').setView([52.1, 19.4], 6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18
}).addTo(map);

let selectedCity = null;

function onMapClick(e) {
  if (!selectedCity) return;
  document.getElementById("selected_city").value = selectedCity;
}

function addCityMarkers(cities) {
  cities.forEach(city => {
    const marker = L.marker([city.lat, city.lon]).addTo(map);
    marker.bindPopup(city.name);
    marker.on("click", () => {
      document.getElementById("selected_city").value = city.name;
    });
  });
}

fetch("/api/cities_coords")
  .then(res => res.json())
  .then(data => {
    addCityMarkers(data);
  });
