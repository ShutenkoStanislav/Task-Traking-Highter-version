document.addEventListener('show.bs.modal', function(event) {
    const trigger = event.relatedTarget;
    const modal = event.target;
    const modalId = modal.id;
    const isWorkspace = trigger && trigger.dataset.workspaceId;
    const boxes = window.WORKSPACE_BOXES || [];

    
    if (modalId === 'FolderModal') {
        const folderBoxWrapper = document.getElementById('folder-box-select-wrapper');
        const folderNameWrap = document.getElementById('folder-name-wrap');
        const colorBtn = document.getElementById('folder-color-btn');
        const brSeparator = document.getElementById('folder-br-separator');
        const modalBody = modal.querySelector('.modal-body');

        if (!isWorkspace) {
            folderBoxWrapper?.classList.add('d-none');

            if (folderNameWrap) folderNameWrap.style.width = '100%';
            if (brSeparator) brSeparator.style.display = 'block';
            colorBtn?.classList.replace('custom_color_select_btn_lg', 'custom_workspace_btn_style');
            modalBody?.classList.remove('compact-workspace-mode');
        } else {
            folderBoxWrapper?.classList.remove('d-none');
            if (folderNameWrap) folderNameWrap.style.width = '50%';
            if (brSeparator) brSeparator.style.display = 'none';
            colorBtn?.classList.replace('custom_workspace_btn_style', 'custom_color_select_btn_lg');
            modalBody?.classList.add('compact-workspace-mode');

          
            const folderBoxDropdown = document.getElementById('folder-box-dropdown');
    
            if (folderBoxDropdown) {
                folderBoxDropdown.innerHTML = boxes.map(box => `
                    <li>
                        <a class="dropdown-item rounded-3" href="#"
                            onclick="selectFolderBox(${box.id}, '${box.name}')">
                            ${box.name}
                        </a>
                    </li>
                    `).join('');
                
            }
        }
        return; 
    }

    
    const taskFields = document.getElementById('task-workspace-fields');
    const titleDiv = document.getElementById('task-title-wrap');
    const contDiv = document.getElementById('task-cont-wrap');

    if (!isWorkspace) {
        taskFields?.classList.add('d-none');
        if (titleDiv) titleDiv.style.width = '100%';
        if (contDiv) contDiv.style.width = '100%';
    } else {
        if (titleDiv) titleDiv.style.width = '50%';
        if (contDiv) contDiv.style.width = '50%';

        if (taskFields) {
            taskFields.classList.remove('d-none');
            taskFields.classList.add('d-flex');

            const boxDropdown = document.getElementById('task-box-dropdown');
            if (boxDropdown) {
                boxDropdown.innerHTML = boxes.map(box => `
                    <li>
                        <a class="dropdown-item rounded-3" href="#" onclick="selectTaskBox(${box.id}, '${box.name}')">
                            ${box.name}
                        </a>
                    </li>
                `).join('');
            }
            window._taskBoxes = boxes;
        }
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
        folderDropdown.innerHTML = selectedBox.folders.map(f => `
            <li>
                <a class="dropdown-item rounded-3" href="#" onclick="selectTaskFolder(${f.id}, '${f.name}')">
                    ${f.name}
                </a>
            </li>
        `).join('');
    } else {
        folderBtn.disabled = true;
    }
}

function selectTaskFolder(folderId, folderName) {
    document.getElementById('task-folder-label').textContent = folderName;
    document.getElementById('task-folder-hidden').value = folderId;
}

function selectFolderBox(boxId, boxName) {
    document.getElementById('folder-box-label').textContent = boxName;
    document.getElementById('folder-modal-box-id').value = boxId;
}