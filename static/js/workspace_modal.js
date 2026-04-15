document.addEventListener('show.bs.modal', function(event) {
    const trigger = event.relatedTarget;
    

    
    const taskFields = document.getElementById('task-workspace-fields');
    const folderBoxWrapper = document.getElementById('folder-box-select-wrapper');
    const titleDiv = document.getElementById('task-title-wrap');
    const contDiv = document.getElementById('task-cont-wrap');


    if ( !trigger || !trigger.dataset.workspaceId) {
        folderBoxWrapper?.classList.add('d-none');
        taskFields?.classList.add('d-none');
        if (titleDiv) titleDiv.style.width = '100%';
        if (contDiv) contDiv.style.width = '100%';
        return;

    }

    const boxes = window.WORKSPACE_BOXES || [];

    if (titleDiv) titleDiv.style.width = '50%';
    if (contDiv) contDiv.style.width = '50%';



    if (folderBoxWrapper) {
        folderBoxWrapper.classList.remove('d-none');
        const folderBoxSelect = document.getElementById('folder-box-select')
        const folderBoxId = document.getElementById('folder-modal-box-id');
        folderBoxSelect.innerHTML = '<option value="">Box</option>';
        boxes.forEach(box => {
            folderBoxSelect.innerHTML += `<option value="${box.id}">${box.name}</option>`;
        });
        folderBoxSelect.onchange = () => folderBoxId.value = folderBoxSelect.value;
    }

    

    if (taskFields) {
        taskFields.classList.remove('d-none');
        taskFields.classList.add('d-flex');

        const boxDropdown = document.getElementById('task-box-dropdown');
        const folderDropdown = document.getElementById('task-folder-dropdown');
        const folderBtn = document.getElementById('task-folder-btn');
        const folderLabel = document.getElementById('task-folder-label');

        boxDropdown.innerHTML = '';
        boxes.forEach(box => {
            boxDropdown.innerHTML += `
            <li>
                    <a class="dropdown-item rounded-3" href="#" 
                       onclick="selectTaskBox(${box.id}, '${box.name}')">
                        ${box.name}
                    </a>
                </li>`;
        });

        window._taskBoxes = boxes;      
    }

});

function selectTaskBox(boxId, boxName) {
    document.getElementById('task-box-label').textContent = boxName;
    document.getElementById('task-box-hidden').value = boxId;

    const boxes = window._taskBoxes || [];
    const selectedBox = boxes.find(b => b.id == boxId);
    const folderDropdown = document.getElementById('task-folder-dropdown');
    const folderBtn = document.getElementById('task-folder-btn');
    const folderLabel = document.getElementById('task-folder-label');

    folderDropdown.innerHTML = '';
    folderLabel.textContent = 'Folder';
    document.getElementById('task-folder-hidden').value = '';

    if (selectedBox && selectedBox.folders.length > 0) {
        folderBtn.disabled = false;
        selectedBox.folders.forEach(f => {
            folderDropdown.innerHTML += `
                <li>
                    <a class="dropdown-item rounded-3" href="#"
                       onclick="selectTaskFolder(${f.id}, '${f.name}')">
                        ${f.name}
                    </a>
                </li>
            `;
        });
    } else {
        folderBtn.disabled = true;
    }

}

function selectTaskFolder(folderId, folderName) {
    document.getElementById('task-folder-label').textContent = folderName;
    document.getElementById('task-folder-hidden').value = folderId;
}