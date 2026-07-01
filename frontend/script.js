const uploadBtn = document.getElementById("uploadBtn");
const heroUploadBtn = document.getElementById("heroUploadBtn");
const pdfFile = document.getElementById("pdfFile");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("chatBox");
const documentList = document.getElementById("documentList");
const clearChatBtn = document.getElementById("clearChatBtn");

function bindEvents() {
    if (uploadBtn && pdfFile) {
        uploadBtn.addEventListener("click", () => pdfFile.click());
        heroUploadBtn?.addEventListener("click", () => pdfFile.click());
    }

    if (pdfFile) {
        pdfFile.addEventListener("change", async () => {
            if (pdfFile.files.length === 0) return;

            const file = pdfFile.files[0];
            uploadBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
            addSystemMessage(`Uploading ${file.name}...`);

            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("/upload", { method: "POST", body: formData });
                const text = await response.text();
                let data = {};
                try {
                    data = text ? JSON.parse(text) : {};
                } catch (error) {
                    throw new Error("The server returned an invalid response.");
                }

                if (!response.ok) {
                    throw new Error(data.detail || data.error || "Upload failed");
                }

                uploadBtn.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${file.name}`;
                addSystemMessage(`Uploaded ${data.filename}. ${data.characters} characters extracted.`);
                refreshDocuments();
            } catch (error) {
                addSystemMessage(`Upload failed: ${error.message}`);
                uploadBtn.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> Choose PDF';
            }
        });
    }

    if (sendBtn && chatInput) {
        sendBtn.addEventListener("click", sendMessage);
        chatInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
    }

    if (clearChatBtn && chatBox) {
        clearChatBtn.addEventListener("click", () => {
            chatBox.innerHTML = '<div class="ai-message">Hello! Upload a PDF and I’ll help you ask questions about it.</div>';
        });
    }
}

async function sendMessage() {
    if (!chatInput || !chatBox) return;

    const message = chatInput.value.trim();
    if (message === "") return;

    addUserMessage(message);
    chatInput.value = "";
    addSystemMessage("Thinking...");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: message }),
        });

        const text = await response.text();
        let data = {};
        try {
            data = text ? JSON.parse(text) : {};
        } catch (error) {
            throw new Error("The server returned an invalid response.");
        }

        if (!response.ok) {
            throw new Error(data.detail || "Unable to answer right now");
        }

        const aiMessage = document.createElement("div");
        aiMessage.className = "ai-message";
        aiMessage.innerHTML = `${data.answer}<br><br><strong>Source:</strong> ${data.source || "Uploaded PDF"}`;
        chatBox.appendChild(aiMessage);
        scrollBottom();
    } catch (error) {
        addSystemMessage(`Sorry: ${error.message}`);
    }
}

function addUserMessage(text) {
    if (!chatBox) return;
    const div = document.createElement("div");
    div.className = "user-message";
    div.innerHTML = text;
    chatBox.appendChild(div);
    scrollBottom();
}

function addSystemMessage(text) {
    if (!chatBox) return;
    const div = document.createElement("div");
    div.className = "ai-message";
    div.innerHTML = text;
    chatBox.appendChild(div);
    scrollBottom();
}

function scrollBottom() {
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

async function refreshDocuments() {
    if (!documentList) return;

    try {
        const response = await fetch("/documents");
        const text = await response.text();
        let data = {};
        try {
            data = text ? JSON.parse(text) : {};
        } catch (error) {
            console.error("Could not parse document list", error);
            return;
        }

        if (!response.ok) return;

        documentList.innerHTML = "";
        const documents = Array.isArray(data.documents) ? data.documents : [];
        if (documents.length === 0) {
            documentList.innerHTML = '<li class="empty-state">No documents uploaded yet.</li>';
            return;
        }

        documents.forEach((name) => {
            const item = document.createElement("li");
            item.innerHTML = `<i class="fa-solid fa-file-pdf"></i> ${name}`;
            documentList.appendChild(item);
        });
    } catch (error) {
        console.error("Could not refresh documents", error);
    }
}

bindEvents();
refreshDocuments();