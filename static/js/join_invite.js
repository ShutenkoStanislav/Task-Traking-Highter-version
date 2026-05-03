(function () {
    const joinModal = document.getElementById("JoinWorkspaceModal");
    if (!joinModal) return;

    const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] ?? "";

    const codeInput = document.getElementById("joinCode")
    const joinBtn = document.getElementById("joinBtn")
    const alertBox = document.getElementById("joinAlert")

    function showAlert(message, type = "danger") {
        alertBox.className = `alert alert-${type} mb-3`;
        alertBox.textContent = message;
        alertBox.classList.remove("d-none");
    }

    codeInput.addEventListener("input", () => {
        let val = codeInput.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
        if (val.length > 4) val = val.slice(0, 4) + "-" + val.slice(4, 8);
        codeInput.value = val;
    });

    joinModal.addEventListener("hidden.bs.modal", () => {
        codeInput.value = "";
        alertBox.classList.add("d-none");
    });

    joinBtn.addEventListener("click", async () => {
        console.log("joinBtn clicked, code:", codeInput.value);
        const code = codeInput.value.trim();

        if (code.length < 9){
            showAlert("Enter a valid code (A3F8-C2D1)", "warning");
            return;
        }

        joinBtn.disabled = true;

        try {
            const res = await fetch("/workspace/invite/accept/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
                body: JSON.stringify({ code }),
            });
            const data = await res.json();

            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                showAlert(data.error);
                joinBtn.disabled = false;
            }

        } catch (err) {
            showAlert("Connection error, try again");
            joinBtn.disabled = false;
        }

    });
})();