const API_ENDPOINT = "http://127.0.0.1:8002/index-page";

async function scrapeAndSend(tab) {
  try {
    const [{ result: htmlContent }] = await browser.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.documentElement.outerHTML,
    });

    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: tab.url,
        title: tab.title,
        html: htmlContent,
      }),
    });

    const data = await response.json();
    console.log("Success:", data);
    return { success: true };
  } catch (err) {
    console.error("Scraping failed:", err);
    return { success: false, error: err.message };
  }
}

async function indexPage(data) {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: data.url,
        title: data.title,
        html: data.html,
      }),
    });

    const result = await response.json();
    console.log("Success:", result);
    return { success: true };
  } catch (err) {
    console.error("Indexing failed:", err);
    return { success: false, error: err.message };
  }
}

// Handle messages from content script
browser.runtime.onMessage.addListener((message, sender) => {
  if (message.action === "indexPage") {
    return indexPage(message);
  }
});
