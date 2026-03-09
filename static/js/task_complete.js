document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.task-complete-input');

    inputs.forEach(input => {
        
        input.addEventListener('change', function() {
            if (this.checked) {
               
                const url = this.dataset.url;
                const taskItem = this.closest('.list-group-item');

                
                if (taskItem) {
                    taskItem.style.transition = "all 3s ease";
                    taskItem.style.opacity = "0.2";
                    taskItem.style.textDecoration = "line-through";
                    taskItem.style.pointerEvents = "none";
                }

                
                setTimeout(() => {
                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie("csrftoken"),
                            'X-Requested-With': "XMLHttpRequest",
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json()) 
                    .then(data => {
                        if (data.status === 'success') {
                            taskItem.style.opacity = '0';
                            setTimeout(() => taskItem.remove(), 300);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        
                        if (taskItem) {
                            taskItem.style.opacity = '1';
                            taskItem.style.textDecoration = 'none';
                            taskItem.style.pointerEvents = 'auto';
                            input.checked = false;
                        }
                    });
                }, 3000);
            }
        });
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') { 
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}