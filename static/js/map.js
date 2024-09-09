let map;
let markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 54.093409, lng: -2.89479 },
        zoom: 6
    });

    fetchTrustData();
}

function fetchTrustData() {
    fetch('/api/trusts')
        .then(response => response.json())
        .then(data => {
            data.forEach(trust => {
                addMarker(trust);
            });
        })
        .catch(error => console.error('Error fetching trust data:', error));
}

function addMarker(trust) {
    const marker = new google.maps.Marker({
        position: { lat: trust.lat, lng: trust.lng },
        map: map,
        title: trust.name
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <h3>${trust.name}</h3>
            <p>Total PAs and AAs: ${trust.total}</p>
        `
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });

    markers.push(marker);
}

window.onload = initMap;
