let pollInterval;

async function startPolling() {
    pollInterval = setInterval(async () => {
        const statusDiv = document.getElementById("status");
        
        try {
            const res = await fetch("/progress");
            const data = await res.json();
            
            if (data.status === "downloading") {
                // feedback during download
                statusDiv.innerHTML = `
                    <div style="margin-top:8px; padding: 15px; border-radius: 8px;">
                        <h4 style="margin-top: 0;">⏳ Downloading...</h4>
                        <div style="margin-bottom: 5px; font-weight: bold;">Progress: ${data.percent}</div>
                        
                        <div style="height: 15px; background-color: #ccc; border-radius: 5px; overflow: hidden; margin-bottom: 10px;">
                            <div style="height: 100%; width: ${data.percent}; background-color: #d8061bff;"></div>
                        </div>

                        <p style="margin: 5px 0;">Speed: <strong>${data.speed}</strong></p>
                        <p style="margin: 5px 0;">ETA: <strong>${data.eta}</strong></p>
                        <p style="margin: 5px 0;">Downloaded: ${data.downloaded_bytes} of ${data.total_size}</p>
                    </div>
                `;
            } else if (data.status === "starting") {
                 statusDiv.innerText = "🔍 Fetching video info and preparing download...";
            } else if (data.status === "error") {
                clearInterval(pollInterval);
                statusDiv.innerText = "Download failed during processing.";
            }

        } catch (err) {
            console.error("Polling error (network or JSON issue):", err);
            // Don't stop polling on minor error
        }
    }, 2000); // Poll every 2 seconds
}


document.getElementById("downloadBtn").addEventListener("click", async () => {
    // Clear any previous interval
    if (pollInterval) clearInterval(pollInterval);
    
    const url = document.getElementById("videoUrl").value.trim();
    const statusDiv = document.getElementById("status");

    if (!url) {
        statusDiv.innerText = "Please enter a valid URL.";
        return;
    }

    statusDiv.innerText = "Requesting download...";
    
    // Start polling - show status updates immediately
    startPolling(); 

    try {
        // This will block until the download is *complete* or *fails*
        const res = await fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });
        const data = await res.json();
        
        // Stop polling on final response
        clearInterval(pollInterval); 

        if (data.status === "success") {
            // Final success feedback
            statusDiv.innerHTML = `
                <div style="padding: 15px; border: 1px solid #28a745; background-color: #d4edda; color: #155724; border-radius: 8px;">
                    <strong>Download Complete!</strong><br>
                    <strong>Title:</strong> <b>${data.title}</b><br>
                    <strong>Platform:</strong> ${data.platform}<br>
                    <strong>File Saved as:</strong> <code>${data.file}</code>
                </div>
            `;
        } else {
            // Final error feedback
            statusDiv.innerHTML = `
                <div style="padding: 15px; border: 1px solid #dc3545; background-color: #f8d7da; color: #721c24; border-radius: 8px;">
                    <strong>Error during Download!</strong><br>
                    <strong>Message:</strong> ${data.message}
                </div>
            `;
        }
    } catch (err) {
        clearInterval(pollInterval);
        statusDiv.innerText = "Server connection lost. Please try refreshing.";
    }
});