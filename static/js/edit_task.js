function enableEditing(taskId) {
        console.log("Button clicked for task:", taskId); 
        const fieldset = document.getElementById('fieldset-' + taskId);
        if (!fieldset) {
            console.error("Fieldset not found for ID:", taskId);
            return;
        }

        fieldset.disabled = false; 

        const inputs = fieldset.querySelectorAll('input, textarea, select');
        inputs.forEach(el => {
            el.classList.remove('border-0', 'bg-transparent', 'p-0');
            el.classList.add('form-control', 'bg-white', 'border', 'p-2');
        });

        
        const editBtn = document.getElementById('edit-btn-' + taskId);
        const saveBtn = document.getElementById('save-btn-' + taskId);

        if(editBtn) editBtn.classList.add('d-none');
        if(saveBtn) saveBtn.classList.remove('d-none');
    }