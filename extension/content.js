(() => {
  const btn = document.createElement("button");
  btn.textContent = "Index Page";
  btn.id = "chs-index-btn";

  Object.assign(btn.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    zIndex: "2147483647",
    padding: "10px 18px",
    backgroundColor: "#4F46E5",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "14px",
    fontFamily: "system-ui, sans-serif",
    cursor: "pointer",
    boxShadow: "0 2px 8px rgba(0,0,0,0.3)",
    transition: "background-color 0.2s, transform 0.1s",
  });

  btn.addEventListener("mouseenter", () => {
    btn.style.backgroundColor = "#4338CA";
    btn.style.transform = "scale(1.05)";
  });
  btn.addEventListener("mouseleave", () => {
    btn.style.backgroundColor = "#4F46E5";
    btn.style.transform = "scale(1)";
  });

  function showToast(message, color) {
    const toast = document.createElement("div");
    toast.textContent = message;
    Object.assign(toast.style, {
      position: "fixed",
      bottom: "70px",
      right: "20px",
      zIndex: "2147483647",
      padding: "8px 16px",
      backgroundColor: color,
      color: "#fff",
      borderRadius: "6px",
      fontSize: "13px",
      fontFamily: "system-ui, sans-serif",
      boxShadow: "0 2px 8px rgba(0,0,0,0.3)",
      opacity: "0",
      transition: "opacity 0.2s",
    });
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.style.opacity = "1");
    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 200);
    }, 2000);
  }

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.style.opacity = "0.5";

    try {
      const response = await browser.runtime.sendMessage({
        action: "indexPage",
        url: window.location.href,
        title: document.title,
        html: document.documentElement.outerHTML,
      });
      showToast(response.success ? "Page indexed" : "Indexing failed", response.success ? "#16A34A" : "#DC2626");
    } catch (err) {
      showToast("Connection error", "#DC2626");
    }

    btn.disabled = false;
    btn.style.opacity = "1";
  });

  document.body.appendChild(btn);
})();
