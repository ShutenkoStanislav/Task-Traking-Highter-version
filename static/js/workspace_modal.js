document.addEventListener('show.bs.modal', function(event) {
    const trigger = event.relatedTarget;
    if ( !trigger || !trigger.dataset.workspaceId) {
        document.getElementById('folder-box-select-wrapper')?.classList.add('d-none');
        document.getElementById('task-workspace-fields')?.classList.add('d-none');
        return;
    }

    const boxes = window.WORKSPACE_BOXES || [];

    const folderBoxWrapper = document.getElementById('folder-box-select-wrapper');
    const folderBoxSelect = document.getElementById('folder-box-select');
    const folderBoxId = document.getElementById('folder-modal-box-id');

    if (folderBoxWrapper) {
        folderBoxWrapper.classList.remove('d-none');
        folderBoxSelect.innerHTML = '<option value="">Box</option>';
        boxes.forEach(box => {
            folderBoxSelect.innerHTML += `<option value="${box.id}">${box.name}</option>`;
        });
        folderBoxSelect.onchange = () => folderBoxId.value = folderBoxSelect.value;
    }

    const taskFields = document.getElementById('task-workspace-fields');
    const taskBoxSelector = document.getElementById('task-box-select');
    const taskFolderSelector = document.getElementById('task-folders-select');

    if (taskFields) {
        taskFields.classList.remove('d-none');
        taskBoxSelector.innerHTML = '<option value="">Box</option>';
        boxes.forEach(box => {
            taskBoxSelector.innerHTML += `<option value="${box.id}">${box.name}</option>`;
        });

        taskBoxSelector.onchange = function() {
            const selecetedBox = boxes.find(b => b.id == this.value);
            taskFolderSelector.innerHTML = '<option value="">Folder</option>';
            taskFolderSelector.disabled = !selecetedBox?.folders.length;
            selecetedBox?.folders.forEach(f => {
                taskFolderSelector.innerHTML += `<option value="${f.id}">${f.name}</option>`;
            });
        
        };
    }


});