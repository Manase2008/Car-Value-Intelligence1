document.getElementById('lets-get-started-btn').addEventListener('click', () => {
    const introScene = document.getElementById('intro-scene');
    const evaluatorScene = document.getElementById('evaluator-scene');

    introScene.classList.remove('active');
    introScene.classList.add('hidden');

    setTimeout(() => {
        evaluatorScene.classList.remove('hidden');
        evaluatorScene.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 350);
});

async function makePrediction() {
    const resultCard = document.getElementById('result');
    const priceOutput = document.getElementById('priceOutput');
    
    resultCard.classList.remove('hidden');
    priceOutput.innerText = "Calculating...";

    const payload = {
        brand: document.getElementById('brand').value,
        year: parseInt(document.getElementById('year').value),
        mileage: parseInt(document.getElementById('mileage').value),
        engine_size_l: parseFloat(document.getElementById('engine_size_l').value),
        cylinders: parseInt(document.getElementById('cylinders').value),
        horsepower: parseInt(document.getElementById('horsepower').value),
        transmission: document.getElementById('transmission').value,
        drivetrain: document.getElementById('drivetrain').value,
        fuel_type: document.getElementById('fuel_type').value,
        body_style: document.getElementById('body_style').value,
        num_doors: parseInt(document.getElementById('num_doors').value),
        seating_capacity: parseInt(document.getElementById('seating_capacity').value),
        fuel_economy_mpg: parseFloat(document.getElementById('fuel_economy_mpg').value),
        num_owners: parseInt(document.getElementById('num_owners').value),
        accidents_reported: parseInt(document.getElementById('accidents_reported').value),
        service_history: document.getElementById('service_history').value,
        condition: document.getElementById('condition').value,
        warranty_months: parseInt(document.getElementById('warranty_months').value),
        seller_type: document.getElementById('seller_type').value
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok && data.predicted_price !== undefined) {
            priceOutput.innerText = `$${data.predicted_price.toLocaleString()}`;
        } else {
            priceOutput.innerText = data.error || "Error calculating price.";
        }
    } catch (error) {
        priceOutput.innerText = "Backend connection error. Make sure uvicorn is running!";
    }
}