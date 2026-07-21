function toggleBox(boxId) {
    const folderList = document.getElementById('box-folder-' + boxId);
    const arrow = document.getElementById('box-arrow-' + boxId);
    if (!folderList || !arrow) return;

    const isOpen = arrow.classList.contains('bi-caret-up-fill');

    if (isOpen) {
        folderList.style.opacity = '0';
        setTimeout(() => { folderList.style.display = 'none'; }, 300);
        arrow.className = 'bi bi-caret-down-fill ms-2';
        localStorage.setItem('boxOpen-' + boxId, 'false');
    } else {
        folderList.style.display = '';
        setTimeout(() => { folderList.style.opacity = '1'; }, 10);
        arrow.className = 'bi bi-caret-up-fill ms-2';
        localStorage.setItem('boxOpen-' + boxId, 'true');
    }
}

function editBoxColor(boxId, color, label) {
    document.getElementById('edit-box-color-' + boxId).value = color;
    document.getElementById('edit-box-color-label-' + boxId).innerHTML = 
        `<i class="bi bi-box2-fill" style="color: ${color};"></i> ${label}`;
}



document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[id^="box-folder-"]').forEach(function (el) {
        const boxId = el.id.replace('box-folder-', '');
        const arrow = document.getElementById('box-arrow-' + boxId)
        if (!arrow) return;

        const isOpen = localStorage.getItem('boxOpen-' + boxId) !== 'false';

        if (!isOpen) {
            el.style.display = 'none';
            el.style.opacity = '0';
            arrow.className = 'bi bi-caret-down-fill ms-2';
        } else {
            el.style.opacity = '1';
            arrow.className = 'bi bi-caret-up-fill ms-2';
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('workspace-search');
    if (!searchInput) return;

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
        const container = document.getElementById('boxes-container');
        if (!container) return;

        const boxes = container.querySelectorAll('[data-box-id]');

        let hasGlobalMatch = false;
        if (query !== '') {
            boxes.forEach(function(boxEl) {
                const boxTitleEl = boxEl.querySelector('.box-title') || boxEl.querySelector('a') || boxEl;
                const fallbackName = boxTitleEl.textContent ? boxTitleEl.textContent.toLowerCase() : '';
                const boxName = boxEl.dataset.name ? boxEl.dataset.name.toLowerCase() : fallbackName;

                if (boxName.includes(query)) hasGlobalMatch = true;

                const folderContainer = document.getElementById('box-folder-' + boxEl.dataset.boxId);
                if (folderContainer) {
                    const folders = folderContainer.querySelectorAll('.folder-row a');
                    folders.forEach(link => {
                        if (link.textContent.toLowerCase().includes(query)) hasGlobalMatch = true;
                    });
                }
            });
        }

        const isSearching = query !== '' && hasGlobalMatch;
        const activeQuery = isSearching ? query : '';

        boxes.forEach(function(boxEl) {
            const boxId = boxEl.dataset.boxId;
            const boxTitleEl = boxEl.querySelector('.box-title') || boxEl.querySelector('a') || boxEl;
            
            const fallbackName = boxTitleEl.textContent ? boxTitleEl.textContent.toLowerCase() : '';
            const boxName = boxEl.dataset.name ? boxEl.dataset.name.toLowerCase() : fallbackName;
            
            const arrow = document.getElementById('box-arrow-' + boxId);
            const folderContainer = document.getElementById('box-folder-' + boxId);
            const folders = folderContainer ? Array.from(folderContainer.querySelectorAll('.folder-row')) : [];

            if (!isSearching) {
                boxEl.style.removeProperty('display'); 
                highlightText(boxTitleEl, '');
                
                folders.forEach(f => {
                    f.style.removeProperty('display');
                    const folderLink = f.querySelector('a');
                    highlightText(folderLink, ''); 
                });
                
                if (folderContainer) {
                    const isOpen = localStorage.getItem('boxOpen-' + boxId) !== 'false';
                    if (isOpen) {
                        folderContainer.style.removeProperty('display');
                        folderContainer.style.opacity = '1';
                    } else {
                        folderContainer.style.setProperty('display', 'none', 'important');
                        folderContainer.style.opacity = '0';
                    }
                    if (arrow) arrow.className = isOpen ? 'bi bi-caret-up-fill ms-2' : 'bi bi-caret-down-fill ms-2';
                }
            } else {
                const boxMatch = boxName.includes(activeQuery);
                let anyFolderMatch = false;

                highlightText(boxTitleEl, boxMatch ? activeQuery : '');

                folders.forEach(f => {
                    const folderLink = f.querySelector('a');
                    const folderName = folderLink ? folderLink.textContent.toLowerCase().trim() : '';
                    const folderMatch = folderName.includes(activeQuery);

                    if (folderMatch) {
                        anyFolderMatch = true;
                    }

                    if (boxMatch || folderMatch) {
                        f.style.removeProperty('display');
                        highlightText(folderLink, folderMatch ? activeQuery : ''); 
                    } else {
                        f.style.setProperty('display', 'none', 'important');
                        highlightText(folderLink, '');
                    }
                });

                if (boxMatch || anyFolderMatch) {
                    boxEl.style.removeProperty('display');
                    if (folderContainer) {
                        folderContainer.style.removeProperty('display');
                        folderContainer.style.opacity = '1';
                        if (arrow) arrow.className = 'bi bi-caret-up-fill ms-2';
                    }
                } else {
                    boxEl.style.setProperty('display', 'none', 'important');
                    if (folderContainer) {
                        folderContainer.style.setProperty('display', 'none', 'important');
                    }
                }
            }
        });
    });
});