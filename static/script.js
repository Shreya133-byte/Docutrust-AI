const uploadBtn = document.getElementById("uploadBtn");
const pdfFile = document.getElementById("pdfFile");
const chatInput = document.querySelector(".chat-input input");
const sendBtn = document.querySelector(".chat-input button");
const chatBox = document.querySelector(".chat-box");
const documentList = document.querySelector("aside ul");

uploadBtn.addEventListener("click", () => pdfFile.click());

pdfFile.addEventListener("change", async () => {
    if (pdfFile.files.length === 0) return;

    const file = pdfFile.files[0];
    uploadBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Uploading...`;
    addSystemMessage(`Uploading ${file.name}...`);

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || data.error || "Upload failed");
        }

        uploadBtn.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${file.name}`;
        addSystemMessage(`Uploaded ${data.filename}. ${data.characters} characters extracted.`);
        refreshDocuments();
    } catch (error) {
        addSystemMessage(`Upload failed: ${error.message}`);
        uploadBtn.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> Choose PDF`;
    }
});

sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {
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

        const data = await response.json();
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
    const div = document.createElement("div");
    div.className = "user-message";
    div.innerHTML = text;
    chatBox.appendChild(div);
    scrollBottom();
}

function addSystemMessage(text) {
    const div = document.createElement("div");
    div.className = "ai-message";
    div.innerHTML = text;
    chatBox.appendChild(div);
    scrollBottom();
}

function scrollBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function refreshDocuments() {
    try {
        const response = await fetch("/documents");
        const data = await response.json();
        if (!response.ok) return;

        documentList.innerHTML = "";
        data.documents.forEach((name) => {
            const item = document.createElement("li");
            item.innerHTML = `<i class="fa-solid fa-file-pdf"></i> ${name}`;
            documentList.appendChild(item);
        });
    } catch (error) {
        console.error("Could not refresh documents", error);
    }
}

refreshDocuments();