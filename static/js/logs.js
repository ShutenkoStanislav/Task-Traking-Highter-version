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


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('workspace-search');
    if (!searchInput) return;

    const logsContainer = document.getElementById('logs-container');
    if (!logsContainer) return;

    function highlightText(element, query) {
        if (!element) return;

        if (!element.dataset.originalHtml) {
            element.dataset.originalHtml = element.innerHTML;
        }

        const originalHtml = element.dataset.originalHtml;

        if (!query) {
            element.innerHTML = originalHtml;
            return;
        }

        const regex = new RegExp(`(${query.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')})`, 'gi'); 
        element.innerHTML = originalHtml;

        const walk = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
        let node;
        const nodesToReplace = [];

        while (node = walk.nextNode()) {
            if (node.nodeValue.toLowerCase().includes(query)) {
                nodesToReplace.push(node);
            }
        }
        nodesToReplace.forEach(textNode => {
            const span = document.createElement('span');
            span.innerHTML = textNode.nodeValue.replace(regex, '<mark class="p-0 text-dark" style="background-color: rgba(255, 193, 7, 0.4); border-radius: 3px; ">$1</mark>');
            textNode.parentNode.replaceChild(span, textNode);
        });
    }

    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        const entries = logsContainer.querySelectorAll('[data-log-entry]');

        entries.forEach(function(entry) {
            const textEl = entry.querySelector('.flex-grow-1');

            if (query === '') {
                entry.style.removeProperty('display');
                highlightText(textEl, '');
                return;
            }

            const text = entry.dataset.logText.toLowerCase();
            if (text.includes(query)) {
                entry.style.removeProperty('display');
                highlightText(textEl, query);
            } else {
                entry.style.setProperty('display', 'none', 'important');
                highlightText(textEl, '');
            }
        });

        logsContainer.querySelectorAll('hr').forEach(function(hr) {
            const prev = hr.previousElementSibling;
            if (prev && prev.style.display === 'none') {
                hr.style.setProperty('display', 'none', 'important');
            } else {
                hr.style.removeProperty('display');
            }
        });
    });
});
