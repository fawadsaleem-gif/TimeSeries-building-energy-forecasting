// 1. Find the HTML elements
const readingsContainer = document.getElementById("readings-container");
const predictButton = document.getElementById("predict-button");
const timestampInput = document.getElementById("timestamp");
const resultContainer = document.getElementById("result");

// 2. Generate 48 input fields
for (let i = 1; i <= 48; i++) {
    const input = document.createElement("input");

    input.type = "number";
    input.step = "any";
    input.placeholder = `Reading ${i}`;
    input.id = `reading-${i}`;

    readingsContainer.appendChild(input);
    readingsContainer.appendChild(document.createElement("br"));
}

// 3. Listen for the Predict button click
predictButton.addEventListener("click", async function () {

    // Collect the 48 historical readings
    const readings = [];

    for (let i = 1; i <= 48; i++) {
        const value = document.getElementById(`reading-${i}`).value;

        if (value === "") {
            resultContainer.textContent = `Please enter Reading ${i}.`;
            return;
        }

        readings.push(Number(value));
    }

    // Collect the prediction timestamp
    const timestamp = timestampInput.value;

    if (!timestamp) {
        resultContainer.textContent = "Please select a prediction timestamp.";
        return;
    }

    if (!timestamp.endsWith(":00")) {
        resultContainer.textContent =
            "Please select a timestamp with minutes set to 00.";
        return;
    }

    // Prepare the data for FastAPI
    const requestData = {
        historical_readings: readings,
        next_timestamp: timestamp
    };

    // Send data to the backend
    try {
        resultContainer.textContent = "Generating prediction...";
        predictButton.disabled = true;

        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed.");
        }

        // Display the prediction
        resultContainer.innerHTML = `
            <h3>Prediction: ${data.predicted_reading}</h3>
            <p>Timestamp: ${data.prediction_timestamp}</p>
            <p>Model: ${data.model}</p>
        `;

    } catch (error) {
        resultContainer.textContent = "Error: " + error.message;

    } finally {
        predictButton.disabled = false;
    }
});