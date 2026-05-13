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

const filterCategory = document.getElementById('filterCategory')
const filterActor = document.getElementById('filterActor')
const filterDateFrom = document.getElementById('filterDateFrom')
const filterDateTo = document.getElementById('filterDateTo')

if (filterCategory) filterCategory.addEventListener('change', applyFilters);
if (filterActor) filterActor.addEventListener('change', applyFilters);
if (filterDateFrom) filterDateFrom.addEventListener('change', applyFilters);
if (filterDateTo) filterDateTo.addEventListener('change', applyFilters);