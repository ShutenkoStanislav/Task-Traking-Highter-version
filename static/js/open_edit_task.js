document.getElementById('universalTaskModal')
    .addEventListener('show.bs.modal', function(event){
        const btn = event.relatedTarget;
        const pk = btn.dataset.taskId;

        document.getElementById('modal-title').value = btn.dataset.title;
        document.getElementById('modal-description').value = btn.dataset.description;

        const priorityLabel = {low: '🟩 Low', medium: '🟨 Medium', high: '🟥 High' }
        document.getElementById('modal-priority').value = btn.dataset.priority;
        document.getElementById('priority-label').textContent = priorityLabel[btn.dataset.priority];

        document.getElementById('modal-edit-form').action = `/${pk}/update/`;
        document.getElementById('modal-comment-form').action = `/${pk}/`;
        document.getElementById('modal-delete-form').action  = `/${pk}/delete/`;

        document.getElementById('modal-fieldset').disabled = true;
        document.getElementById('modal-edit-btn').classList.remove('d-none');
        document.getElementById('modal-save-btn').classList.add('d-none');

        

        document.querySelectorAll('.comment[data-comment-task]').forEach(function(el) {
            el.style.display = el.dataset.commentTask == pk ? '' : 'none';
        });

});

document.getElementById('comment-media').addEventListener('change', function() {
    const filename = this.files[0] ? this.files[0].name : 'No media';
    document.getElementById('media-fileman').textContent = filename;
});

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const openPk = urlParams.get('open');
    if (openPk) {
        const btn = document.querySelector(`[data-task-id="${openPk}"]`);
        if (btn) btn.click();
    }
});

function enableModalEditing() {
    document.getElementById('modal-fieldset').disabled = false;
    document.getElementById('modal-edit-btn').classList.add('d-none');
    document.getElementById('modal-save-btn').classList.remove('d-none');
}

function openDeleteModal() {
    bootstrap.Modal.getInstance(
        document.getElementById('universalTaskModal')
    ).hide();
    new bootstrap.Modal(
        document.getElementById("universalDeleteModal")
    ).show();
}

function setPriority(value, label) {
    document.getElementById('modal-priority').value = value;
    document.getElementById('priority-label').textContent = label;

}

function createPriority(value, label) {
    document.getElementById('create-priority').value = value;
    document.getElementById('create-priority-label').textContent = label;

}

function createColor(value, label) {
    document.getElementById('create-color').value = value;
    document.getElementById('create-color-label').textContent = label;

}

function createColorBox(value, label) {
    document.getElementById('create-color-box').value = value;
    document.getElementById('create-color-box-label').textContent = label;

}