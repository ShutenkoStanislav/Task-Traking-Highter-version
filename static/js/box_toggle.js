function toggleBox(boxId) {
    const folderList = document.getElementById('box-folder-' + boxId);
    const arrow = document.getElementById('box-arrow-' + boxId);
    if (!folderList || !arrow) return;

    const isOpen = localStorage.getItem('boxOpen-' + boxId) !== 'false';

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