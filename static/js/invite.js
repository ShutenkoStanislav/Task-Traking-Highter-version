function setInviteRole(value, label) {
    document.getElementById("inviteRole").value = value;
    document.getElementById("inviteRoleLabel").textContent = label;
}

(function () {
    const inviteModal = document.getElementById("InviteModal");

    if (!inviteModal) return;

    const WORKSPACE_PK = inviteModal.dataset.workspacePk;
    const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] ?? "";

    const roleInput = document.getElementById("inviteRole");
    const sendBtn = document.getElementById("sendInviteBtn");
    const alertBox = document.getElementById("inviteAlert");
    const codeBlock = document.getElementById("inviteCodeBlock");
    const codeText = document.getElementById("inviteCodeText");
    const copyBtn = document.getElementById("copyLinkBtn");

    function showAlert(message, type = "danger") {
        alertBox.className = `alert alert-${type} mb-3`;
        alertBox.textContent = message;
        alertBox.classList.remove("d-none");
    }

    function hideAlert() {
        alertBox.classList.add("d-none");
    }

    inviteModal.addEventListener("hidden.bs.modal", () => {
        alertBox.classList.add("d-none");
        codeBlock.classList.add("d-none");
        codeText.value = "";
        document.getElementById("inviteRole").value = "member";
        const roleLabel = document.getElementById("inviteRoleLabel");
        if (roleLabel) roleLabel.textContent = "Member";
    });


    sendBtn.addEventListener("click", async () => {
        const role = roleInput.value;

        alertBox.classList.add("d-none");
        sendBtn.disabled = true;

        try {
            const res = await fetch("/workspace/invite/accept/", {
                method: "POST",
                headers : {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
                body: JSON.stringify({ role }),
            });

            const data = await res.json();

            if (data.success) {
               
                codeText.value = data.code;
                codeBlock.classList.remove("d-none");
            } else {
                showAlert(data.error, "danger");
            }
        } catch (err) {
            showAlert("Conection error, try again", "danger");
        } finally {
            sendBtn.disabled = false;
        }
    });

    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(codeText.value).then(() => {
            copyBtn.innerHTML = '<i class="bi bi-clipboard-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
            }, 2000);
        });
    })
})();