const leftbar = document.getElementById('leftbar');
const leftbar_resizer = document.getElementById('leftbar-resizer');

const folder_list = document.getElementById('folder_list');
const folders_toggle = document.getElementById('folders-toggle');
const folder_Arrow = document.getElementById('folders-arrow')

let isDragging = false;

let isOpen = true;

const saveWidth = localStorage.getItem('leftbarWidth');
if (saveWidth) leftbar.style.width = saveWidth;

folders_toggle.addEventListener('click', function() {
    if (isOpen) {
        folder_list.style.opacity = '0';
        setTimeout(function() {
            folder_list.style.display = 'none';
        }, 150);
        folder_Arrow.className = 'bi bi-caret-down-fill';
    } else {
        folder_list.style.display = '';
        setTimeout(function() {
            folder_list.style.opacity = '1';
        }, 15);
        folder_Arrow.className = 'bi bi-caret-up-fill';
    }
    isOpen = !isOpen;
});

leftbar_resizer.addEventListener('mousedown', function(e) {
    isDragging = true;
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
});

document.addEventListener('mousemove', function(e) {
    if (!isDragging) return;
    const perc = (e.clientX / window.innerWidth) * 100;
    if (perc >= 12 && perc <= 31) {
        leftbar.style.width = perc + '%';
    }
});

document.addEventListener('mouseup', function() {
    if (isDragging) {
        localStorage.setItem('leftbarWidth', leftbar.style.width);
    }
    isDragging = false;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';



});

