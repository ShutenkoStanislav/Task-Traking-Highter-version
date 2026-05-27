let originalBoxeOrder = null;

function initBoxOrder() {
    const container = document.getElementById('boxes-container');
    if (!container || originalBoxeOrder) return;

    originalBoxeOrder = [];
    const children = Array.from(container.children);

    let i = 0;

    while (i < children.length) {
        const el = children[i];
        if (el.dataset && el.dataset.name) {
            const group = [el];
            i++;
            while (i < children.length && !(children[i].dataset && children[i].dataset.name)) {
                group.push(children[i]);
                i++;
            }

            const folderContainer = group.find(e => e.id && e.id.startsWith('box-folder-'));
            const originalFolders = folderContainer
                ? Array.from(folderContainer.querySelectorAll('.folder-row')).map(f => f.cloneNode(true))
                : [];

            originalBoxeOrder.push({
                name: el.dataset.name,
                group,
                originalFolders,
                folderContainer
            });
        } else {
            i++;
        }

    }
}


function sortBoxes(direction) {
    const container = document.getElementById('boxes-container');
    if (!container) return;


    initBoxOrder();

    const sorted = [...originalBoxeOrder].sort((a, b) => {
        return direction === 'asc'
            ? a.name.localeCompare(b.name, undefined, { sensitivity: 'base'})
            : b.name.localeCompare(a.name, undefined, { sensitivity: 'base'});
    });

    sorted.forEach(box => {
        if (box.folderContainer) {
            const folders = Array.from(box.folderContainer.querySelectorAll('.folder-row'));
            folders.sort((a, b) => {
                const nameA = a.querySelector('a').textContent.trim();
                const nameB = b.querySelector('a').textContent.trim();
                return direction === 'asc'
                    ? nameA.localeCompare(nameB, undefined, { sensitivity: 'base' })
                    : nameB.localeCompare(nameA, undefined, { sensitivity: 'base' });
            });                              
            folders.forEach(f => box.folderContainer.appendChild(f));
        }                                   
        box.group.forEach(el => container.appendChild(el));
    });                                      
}                                            

document.addEventListener('DOMContentLoaded', initBoxOrder);