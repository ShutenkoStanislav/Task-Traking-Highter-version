(function () {
    const memberModal = document.getElementById("MemberDetailModal");
    if (!memberModal) return;

    const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] ?? "";
    const WORKSPACE_PK = window.location.pathname.split("/")[2];
    const promoteBtn = document.getElementById("promoteBtn");
    const kickBtn = document.getElementById("kickBtn");
    const confirmModal = document.getElementById("ConfirmActionModal");
    const confirmTitle = document.getElementById("confirmTitle");
    const confirmText = document.getElementById("confirmText");
    const confirmActionBtn = document.getElementById("confirmActionBtn");

    let currentMemberPk = null;
    let pendingAction = null;

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

    function showConfirm(title, text, action) {
        

        confirmTitle.textContent = title;
        confirmText.textContent = text;
        pendingAction = action;

        confirmActionBtn.className = action === 'kick'
            ? 'btn btn-danger'
            : 'btn btn-primary';

        const memberModalInstance = bootstrap.Modal.getInstance(memberModal);

        if (memberModalInstance) {
            memberModal.addEventListener('hidden.bs.modal', () => {
                new bootstrap.Modal(confirmModal).show();
            }, {once: true });
            memberModalInstance.hide();
        } else {
            new bootstrap.Modal(confirmModal).show();
        }
    }

    promoteBtn?.addEventListener("click", () => {
        const isPromote = promoteBtn.textContent.trim() === "Promote to Admin";
        showConfirm(
            isPromote ? "Promote to Admin?": "Demote to Member?",
            isPromote
                ? `Are you sure you want to promote ${document.getElementById("memberUsername").textContent} to Admin?`
                : `Are you sure you want to demote ${document.getElementById("memberUsername").textContent} to Member?`,
            'promote'
        );
    });

    kickBtn?.addEventListener("click", () => {
        showConfirm(
            "Kick member?",
            `Are you sure you want kick ${document.getElementById("memberUsername").textContent} from workspace?`,
            'kick'
        );

    });

    confirmActionBtn?.addEventListener("click", async () => {
        confirmActionBtn.disabled = true;

        const url = pendingAction === 'kick'
            ? `/workspace/${WORKSPACE_PK}/kick/${currentMemberPk}/`
            : `/workspace/${WORKSPACE_PK}/promote/${currentMemberPk}/`;

        try {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
            });

            const data = await res.json();

            if (data.success) {
                bootstrap.Modal.getInstance(confirmModal).hide();
                location.reload();
            } else {
                alert(data.error);
                confirmActionBtn.disabled = false;
            }
        } catch (err) {
            alert("Connection error, try again");
            confirmActionBtn.disabled = false;

        }
    });
  

})();

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('workspace-search');
    if (!searchInput) return;

    const membersContainer = document.getElementById('members-container');
    if (!membersContainer) return;

    function highlightText(element, query) {
        if (!element) return;
        if (!element.dataset.originalHtml) {
            element.dataset.originalHtml = element.innerHTML;
        }
        const originalHtml = element.dataset.originalHtml;
        if (!query) {
            element.innerHTML = originalHtml;
            return;
        }
        const regex = new RegExp(`(${query.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')})`, 'gi');
        element.innerHTML = originalHtml;
        const walk = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
        let node;
        const nodesToReplace = [];
        while (node = walk.nextNode()) {
            if (node.nodeValue.toLowerCase().includes(query)) {
                nodesToReplace.push(node);
            }
        }
        nodesToReplace.forEach(textNode => {
            const span = document.createElement('span');
            span.innerHTML = textNode.nodeValue.replace(regex, '<mark class="p-0 text-dark" style="background-color: rgba(255, 193, 7, 0.4); border-radius: 3px;">$1</mark>');
            textNode.parentNode.replaceChild(span, textNode);
        });
    }

    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        const entries = membersContainer.querySelectorAll('[data-member-entry]');

        entries.forEach(function(entry) {
            const textEl = entry.querySelector('.ms-3');

            if (query === '') {
                entry.style.removeProperty('display');
                highlightText(textEl, '');
                return;
            }

            const text = entry.dataset.searchText.toLowerCase();
            if (text.includes(query)) {
                entry.style.removeProperty('display');
                highlightText(textEl, query);
            } else {
                entry.style.setProperty('display', 'none', 'important');
                highlightText(textEl, '');
            }
        });

        membersContainer.querySelectorAll('hr').forEach(function(hr) {
            const prev = hr.previousElementSibling;
            if (prev && prev.style.display === 'none') {
                hr.style.setProperty('display', 'none', 'important');
            } else {
                hr.style.removeProperty('display');
            }
        });
    });
});