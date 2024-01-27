const share = async () => {
    try {
        const location = window.location.href.slice(7); // Get the URL without the protocol
        // Remove the '?page' parameter if it exists
        const url = location.split('?')[0];
        await navigator.clipboard.writeText(url);
        const copyPopup = document.getElementById("copyPopup");
        copyPopup.classList.toggle("show");
    } catch (err) {
        alert("Failed to copy link");
    }
}