// Auto-refresh portfolio data every 30 seconds
function refreshPortfolio() {
    location.reload();
}

// Auto-refresh every 30 seconds (optional)
// setInterval(refreshPortfolio, 30000);

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
    });
}