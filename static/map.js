let map;
let markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 54.5, lng: -3.5 },
        zoom: 6,
    });
    fetch('/api/trusts')
        .then(response => response.json())
        .then(data => {
            populateTableAndMap(data);
        });
}

function populateTableAndMap(data) {
    const tableBody = document.getElementById('trusts-table').getElementsByTagName('tbody')[0];
    data.forEach((trust, index) => {
        addMarker(trust, index);
        addTableRow(tableBody, trust, index);
    });
}

function addMarker(trust, index) {
    const marker = new google.maps.Marker({
        position: { lat: trust.lat, lng: trust.lng },
        map: map,
        title: trust.name,
    });
    markers.push(marker);

    marker.addListener('click', () => {
        highlightRow(index);
        scrollToRow(index);
        highlightMarker(index);
    });
}

function addTableRow(tableBody, trust, index) {
    const row = tableBody.insertRow();
    const nameCell = row.insertCell(0);
    const totalCell = row.insertCell(1);
    nameCell.innerHTML = trust.name + ` <a href="/trusts/${index}/policy" target="_blank">(1)</a>`;
    totalCell.textContent = trust.total;
    row.dataset.index = index;

    // Add event listener for row click
    row.addEventListener('click', () => {
        highlightRow(index);
        scrollToRow(index);
        highlightMarker(index);
    });
}

function highlightRow(index) {
    const rows = document.getElementById('trusts-table').getElementsByTagName('tr');
    for (let row of rows) {
        row.classList.remove('highlight');
    }
    rows[index + 1].classList.add('highlight');
}

function scrollToRow(index) {
    const tableSection = document.getElementById('table-section');
    const rows = document.getElementById('trusts-table').getElementsByTagName('tr');
    const targetRow = rows[index + 1];
    tableSection.scrollTop = targetRow.offsetTop - tableSection.offsetTop;
}

function highlightMarker(index) {
    markers.forEach((marker, i) => {
        marker.setIcon(null);
        marker.setZIndex(1);
    });

    markers[index].setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
    markers[index].setZIndex(100);
}

window.onload = initMap;