(function () {
    const memberModal = document.getElementById("MemberDetailModal");
    if (!memberModal) return;

    const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] ?? "";
    const WORKSPACE_PK = window.location.pathname.split("/")[2];

    let currentMemberPk = null;

    const promoteBtn = document.getElementById("promoteBtn");
    const kickBtn = document.getElementById("kickBtn");

    document.querySelectorAll("[data-member-pk]").forEach(card => {
        card.addEventListener("click", () => {
            currentMemberPk = card.dataset.memberPk;
            const role = card.dataset.memberRole;

            document.getElementById("memberUsername").textContent = card.dataset.memberUsername;
            document.getElementById("memberEmail").textContent = card.dataset.memberEmail;
            document.getElementById("memberJoined").textContent = card.dataset.memberJoined;

            const roleLabels = {
                owner:  "Owner",
                admin:  "Admin",
                member: "Member"
            };
            document.getElementById("memberRole").textContent = roleLabels[role] ?? role;

            if (promoteBtn) {
                if (role === "owner") {
                    promoteBtn.classList.add("d-none");
                } else {
                    promoteBtn.classList.remove("d-none");
                    promoteBtn.textContent = role === "member"
                        ? "Promote to Admin"
                        : "Demote to Member";
                }
            }

            if (kickBtn) {
                kickBtn.classList.toggle("d-none", role === "owner");
            }

           
            new bootstrap.Modal(memberModal).show();
        });
    });

    promoteBtn?.addEventListener("click", async () => {
        promoteBtn.disabled = true;

        try {
            const res = await fetch(`/workspace/${WORKSPACE_PK}/promote/${currentMemberPk}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
            });
            const data = await res.json();

            if (data.success) {
                bootstrap.Modal.getInstance(memberModal).hide();
                location.reload();
            } else {
                alert(data.error);
                promoteBtn.disabled = false;
            }

        } catch (err) {
            alert("Connection error, try again");
            promoteBtn.disabled = false;
        }
    });

    kickBtn?.addEventListener("click", async () => {
        kickBtn.disabled = true;

        try {
            const res = await fetch(`/workspace/${WORKSPACE_PK}/kick/${currentMemberPk}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
            });
            const data = await res.json();

            if (data.success) {
                bootstrap.Modal.getInstance(memberModal).hide();
                location.reload();
            } else {
                alert(data.error);
                kickBtn.disabled = false;
            }

        } catch (err) {
            alert("Connection error, try again");
            kickBtn.disabled = false;
        }
    });

    

    

})();