chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "getComments") {
    const noeuds = document.querySelectorAll("ytd-comment-thread-renderer #content-text");
    const comments = [...new Set([...noeuds].map(n => n.innerText.trim()).filter(Boolean))];
    sendResponse({ comments });
  }
});