(function () {
    const inviteModal = document.getElementById("InviteModal");

    if (!inviteModal) return;

    const WORKSPACE_PK = inviteModal.dataset.workspacePk;
    const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] ?? "";

    const emailInput = document.getElementById("inviteEmail");
    const roleInput = document.getElementById("inviteRole");
    const sendBtn = document.getElementById("sendInviteBtn");
    const alertBox = document.getElementById("inviteAlert");
    const linkBlock = document.getElementById("inviteLinkBlock");
    const linkText = document.getElementById("inviteLinkText");
    const copyBtn = document.getElementById("copyLinkBtn");

    function showAlert(message, type = "danger") {
        alertBox.className = `alert alert-${type} mb-3`;
        alertBox.textContent = message;
        alertBox.classList.remove("d-none");
    }

    function hideAlert() {
        alertBox.classList.add("d-none");
    }

    function setLoading(isLoading) {
        sendBtn.disabled = isLoading;
        sendBtn.innerHTML = isLoading
            ? '<span class="spinner-border spinner-border-sm me-1"></span> Відправка...'
            : '<i class="bi bi-send"></i> Відправити запрошення';
    }

    inviteModal.addEventListener("hidden.bs.modal", () => {
        emailInput.value = "";
        hideAlert();
        linkBlock.classList.add("d-none");
        linkText.value = "";
    });

    sendBtn.addEventListener("click", async () => {
        const email = emailInput.value.trim();
        const role = roleInput.value;

        hideAlert();

        if (!email) {
            showAlert("Type email addres", "warning");
            return;
        }

        setLoading(true);

        try {
            const res = await fetch(`/workspace/${WORKSPACE_PK}/invite/`, {
                method: "POST",
                headers : {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
                body: JSON.stringify({ email, role }),
            });

            const data = await res.json();

            if (data.success) {
                showAlert(data.message, "success")
                emailInput.value = "";
                linkText.value = data.invite_link;
                linkBlock.classList.remove("d-none");
            } else {
                showAlert(data.error, "danger");
            }
        } catch (err) {
            showAlert("Conection error, try again", "danger");
        } finally {
            setLoading(false);
        }
    });

    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(linkText.value).then(() => {
            copyBtn.innerHTML = '<i class="bi bi-clipboard-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
            }, 2000);
        });
    })
})();