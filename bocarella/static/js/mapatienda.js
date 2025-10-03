// Crear mapa centrado en la primera tienda
const map = L.map('map').setView([tiendas[0].lat, tiendas[0].lng], 13);

// Cargar tiles de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Grupo de marcadores para ajustar zoom automáticamente
const markers = L.featureGroup();

// Agregar marcadores de todas las tiendas
tiendas.forEach(tienda => {
    const marker = L.marker([tienda.lat, tienda.lng])
        .bindPopup(`<b>${tienda.nombre}</b>`);
    marker.addTo(markers);
});

// Agregar al mapa y ajustar zoom para que se vean todos
markers.addTo(map);
map.fitBounds(markers.getBounds());
