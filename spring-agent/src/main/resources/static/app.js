
const form = document.getElementById("predict-form");
const result = document.getElementById("result");
const button = document.getElementById("submit");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = document.getElementById("news").value.trim();
    const url = document.getElementById("url").value.trim();

    if (!text && !url) {
        result.hidden = false;
        result.textContent = "Please enter news text or an article URL.";
        return;
    }

    result.hidden = false;
    result.replaceChildren();

    const loading = document.createElement("p");
    loading.textContent = "Analyzing article...";
    result.appendChild(loading);

    button.disabled = true;

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                url: url,
                explain: false
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Prediction request failed."
            );
        }

        result.replaceChildren();

        const heading = document.createElement("h2");
        heading.textContent = data.prediction || "Unknown";
        result.appendChild(heading);

        const score = document.createElement("p");
        score.className = "score";

        const confidence = Number(data.confidencePercent);

        score.textContent = Number.isFinite(confidence)
            ? `${confidence.toFixed(2)}% model confidence`
            : "Confidence unavailable";

        result.appendChild(score);

        const disclaimer = document.createElement("p");
        disclaimer.textContent = data.disclaimer ||
            "This is a model prediction, not independent fact-checking.";

        result.appendChild(disclaimer);

    } catch (error) {
        result.replaceChildren();

        const message = document.createElement("p");
        message.className = "error";
        message.textContent =
            error.message || "An unexpected error occurred.";

        result.appendChild(message);

    } finally {
        button.disabled = false;
    }
});
