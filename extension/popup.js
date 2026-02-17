const API_BASE = "http://127.0.0.1:8002";

const status = document.getElementById("status");

function showStatus(msg, type) {
  status.textContent = msg;
  status.className = type;
  setTimeout(() => { status.textContent = ""; status.className = ""; }, 3000);
}

function setAllButtons(disabled) {
  document.querySelectorAll("button").forEach(b => b.disabled = disabled);
}

async function deleteHistory(url, method = "DELETE") {
  setAllButtons(true);
  try {
    const res = await fetch(url, { method });
    const data = await res.json();
    if (res.ok) {
      showStatus(`Deleted ${data.deleted} chunk(s).`, "success");
    } else {
      showStatus(data.detail || "Failed", "error");
    }
  } catch (err) {
    showStatus("Connection error", "error");
  }
  setAllButtons(false);
}

document.getElementById("btn-delete-today").addEventListener("click", () => {
  const today = new Date().toISOString().slice(0, 10);
  deleteHistory(`${API_BASE}/history/${today}`);
});

document.getElementById("btn-delete-all").addEventListener("click", () => {
  if (confirm("Delete ALL indexed history? This cannot be undone.")) {
    deleteHistory(`${API_BASE}/history`);
  }
});

document.getElementById("btn-delete-date").addEventListener("click", () => {
  const date = document.getElementById("date-picker").value;
  if (!date) {
    showStatus("Please select a date.", "error");
    return;
  }
  deleteHistory(`${API_BASE}/history/${date}`);
});
