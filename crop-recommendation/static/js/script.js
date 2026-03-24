document.getElementById("predictionForm").addEventListener("submit", async function(e) {

    e.preventDefault(); // prevent page reload

    // collect input values
    const data = {
        nitrogen: parseFloat(document.getElementById("nitrogen").value),
        phosphorous: parseFloat(document.getElementById("phosphorous").value),
        potassium: parseFloat(document.getElementById("potassium").value),
        temperature: parseFloat(document.getElementById("temperature").value),
        humidity: parseFloat(document.getElementById("humidity").value),
        ph: parseFloat(document.getElementById("ph").value),
        rainfall: parseFloat(document.getElementById("rainfall").value)
    };

    try {

        // send data to Flask backend
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // display result
        if(result.success){

            document.getElementById("results").style.display = "block";

            document.getElementById("cropName").textContent = result.prediction;

            document.getElementById("confidence").textContent =
                "Confidence: " + result.confidence.toFixed(2) + "%";

            let alternativesHTML = "";

            result.top_3_crops.slice(1).forEach(crop => {
                alternativesHTML += `
                    <div>
                        ${crop.name} - ${crop.confidence.toFixed(2)}%
                    </div>
                `;
            });

            document.getElementById("alternatives").innerHTML = alternativesHTML;

        }

    } catch(error){

        alert("Server Error: " + error.message);

    }

});


// reset form
function resetForm(){

    document.getElementById("predictionForm").reset();
    document.getElementById("results").style.display = "none";

}