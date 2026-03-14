document.getElementById('universalTaskModal')
    .addEventListener('show.bs.modal', function(event){
        const btn = event.relatedTarget;
        const pk = btn.dataset.taskId;

        document.getElementById('modal-title').value = btn.dataset.title;
        document.getElementById('modal-description').value = btn.dataset.description;
        document.getElementById('modal-priority').value = btn.dataset.priority;

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



