function addSymptomInput() {
    const container = document.getElementById('symptoms-container');
    const currentInputs = container.getElementsByTagName('input');

    // Check if there are already 4 symptom inputs
    if (currentInputs.length >= 3) {
        alert("You can only add up to 4 symptoms.");
        return;
    }
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'symptoms';  // Keeps the name 'symptoms' for all inputs
    input.placeholder = 'Enter symptom leave if you are not having any';
    container.appendChild(input);
}

function analyzeSymptoms() {
    const symptomInputs = document.getElementsByName('symptoms'); // Collection of inputs
    const selectedLanguage = document.getElementById('language').value;
    const output = document.getElementById('diagnosis-list');

    // Collect all symptom input values
    const symptoms = Array.from(symptomInputs)
        .map(input => input.value.trim())
        .filter(value => value);  // Filters out any empty values

    if (symptoms.length === 0) {
        output.innerHTML = '<p>Please enter your symptoms.</p>';
        return;
    }

    output.innerHTML = `<p>Analyzing symptoms: <strong>${symptoms.join(', ')}</strong> in <strong>${selectedLanguage.toUpperCase()}</strong>...</p>`;

    // Send data to the backend
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symptoms, language: selectedLanguage }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
            output.innerHTML = '<p>No possible diagnoses found.</p>';
        } else {
            output.innerHTML = data.map(d => 
                `<p><strong>${d.disease}:</strong> ${d.description}</p>`
            ).join('');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        output.innerHTML = '<p>An error occurred while analyzing symptoms.</p>';
    });
}
