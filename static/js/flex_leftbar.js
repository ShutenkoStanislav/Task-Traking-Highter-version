const leftbar = document.getElementById('leftbar');
const leftbar_resizer = document.getElementById('leftbar-resizer');

let isDragging = false;


const saveWidth = localStorage.getItem('leftbarWidth');
if (saveWidth) leftbar.style.width = saveWidth;

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

