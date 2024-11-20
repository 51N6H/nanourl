async function shortenUrl() {
    const originalUrl = document.getElementById("originalUrl").value;
    const shortenedUrlElement = document.getElementById("shortenedUrl");

    // Clear the previous result or show a loading state
    shortenedUrlElement.innerText = "Shortening URL...";

    try {
        const response = await fetch('http://127.0.0.1:5000/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: originalUrl })
        });

        // Debugging to check if the response is ok
        console.log('Response status:', response.status); // This should log a 200 status if successful

        // Check if the response is OK (200 status)
        if (response.ok) {
            const data = await response.json();

            // Debugging to check what data is returned
            console.log('Data received:', data); // This should log the shortened URL
            
            // Update the DOM with the shortened URL
            shortenedUrlElement.innerText = `Shortened URL: ${data.shortened_url}`;
        } else {
            shortenedUrlElement.innerText = "Error: Unable to shorten URL.";
        }
    } catch (error) {
        // Handle fetch errors (network issues, server issues)
        shortenedUrlElement.innerText = "Error: Unable to shorten URL.";
        console.error('Fetch error:', error); // Log the error to console for debugging
    }
}
