function applyFilters() {
    const category = document.getElementById('filterCategory').value;
    const actor = document.getElementById('filterActor').value;
    const dateFrom = document.getElementById('filterDateFrom').value;
    const dateTo = document.getElementById('filterDateTo').value;

    const params = new URLSearchParams();
    params.set('tab', 'logs');
    if (category) params.set('category', category);
    if (actor) params.set('actor', actor);
    if (dateFrom) params.set('date_from', dateFrom);
    if (dateTo) params.set('date_to', dateTo);

    window.location.href = '?' + params.toString();
}

function setCategory(value, label) {
    document.getElementById('filterCategory').value = value;
    document.getElementById('categoryLabel').textContent = label;
    applyFilters();
}

function setActor(value, label) {
    document.getElementById('filterActor').value = value;
    document.getElementById('actorLabel').textContent = label;
    applyFilters();
}


const dateFrom = document.getElementById('filterDateFrom');
const dateTo   = document.getElementById('filterDateTo');

if (dateFrom) {
    flatpickr(dateFrom, {
        dateFormat: "Y-m-d",
        onChange: function() { applyFilters(); }
    });
}

if (dateTo) {
    flatpickr(dateTo, {
        dateFormat: "Y-m-d",
        onChange: function() { applyFilters(); }
    });
}
