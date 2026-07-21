const universalTaskModal = document.getElementById('universalTaskModal');
if (universalTaskModal) {
    universalTaskModal.addEventListener('show.bs.modal', function(event){
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

        const userRole = btn.dataset.userRole;
        const isWorkspace = btn.dataset.workspace !== '';
        const taskCreator = btn.dataset.taskCreator;
        const currentUserId = window.CURRENT_USER_ID ? String(window.CURRENT_USER_ID) : '';

        const editBtn = document.getElementById('modal-edit-btn');
        const deleteBtn = document.querySelector('#universalTaskModal .btn-danger');

        if (isWorkspace && userRole) {
            if (userRole === 'member') {
                if (taskCreator === currentUserId) {
                    editBtn.classList.remove('d-none');
                    deleteBtn.classList.remove('d-none');
                } else {
                    editBtn.classList.add('d-none');
                    deleteBtn.classList.add('d-none');
                }
            } else if (userRole === 'admin') {
                editBtn.classList.remove('d-none');
                deleteBtn.classList.add('d-none');
            } else {
                editBtn.classList.remove('d-none');
                deleteBtn.classList.remove('d-none');
            }
        } else {
            editBtn.classList.remove('d-none');
            deleteBtn.classList.remove('d-none');
        }
    });
}

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

function createColorBox(value, label) {
    document.getElementById('create-color-box').value = value;
    document.getElementById('create-color-box-label').textContent = label;
}

function createColor(value, label, element) {
    const modal = element.closest('.modal-content');
    const input = modal.querySelector('input[name="color"]');
    const labelSpan = modal.querySelector('.dropdown-toggle span');

    if (input) input.value = value;
    if (labelSpan) labelSpan.textContent = label;
}

const commentMedia = document.getElementById('comment-media');
if (commentMedia) {
    commentMedia.addEventListener('change', function() {
        const filename = this.files[0] ? this.files[0].name : 'No media';
        document.getElementById('media-fileman').textContent = filename;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const openPk = urlParams.get('open');
    if (openPk) {
        const btn = document.querySelector(`[data-task-id="${openPk}"]`);
        if (btn) btn.click();
    }
});