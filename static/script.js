function addSymptomInput() {
    const container = document.getElementById('symptoms-container');
    const currentInputs = container.getElementsByTagName('input');

    // Limit to 4 symptom inputs
    if (currentInputs.length >= 3) {
        alert("You can only add up to 4 symptoms.");
        return;
    }

    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Enter another symptom (optional)';
    input.className = 'symptom-input';
    container.appendChild(input);
}

function analyzeSymptoms() {
    const symptomInputs = document.getElementsByClassName('symptom-input');
    const selectedLanguage = document.getElementById('language').value;
    const output = document.getElementById('diagnosis-list');

    // Collect all symptom input values
    const symptoms = Array.from(symptomInputs)
        .map(input => input.value.trim())
        .filter(value => value); // Filters out any empty values

    if (symptoms.length === 0) {
        output.innerHTML = '<p>Please enter your symptoms.</p>';
        return;
    }

    // Display loading message
    output.innerHTML = `<p>Analyzing symptoms: <strong>${symptoms.join(', ')}</strong> in <strong>${selectedLanguage.toUpperCase()}</strong>...</p>`;

    // Send data to backend for initial analysis
    fetchData(symptoms, selectedLanguage);
}

function fetchData(symptoms, language) {
    const output = document.getElementById('diagnosis-list');

    // Send a request to the backend
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symptoms, language }),
    })
    .then(response => response.json())
    .then(data => {
        output.innerHTML = data.description
            ? `<p><strong>${data.disease}:</strong> ${data.description}</p>`
            : '<p>No possible diagnoses found.</p>';
    })
    .catch(error => {
        console.error('Error:', error);
        output.innerHTML = '<p>An error occurred while analyzing symptoms.</p>';
    });
}

// Trigger fetchData when language is changed after displaying results
function changeLanguage() {
    const selectedLanguage = document.getElementById('language').value;
    const symptomInputs = document.getElementsByClassName('symptom-input');

    // Collect all current symptom inputs
    const symptoms = Array.from(symptomInputs)
        .map(input => input.value.trim())
        .filter(value => value);

    // Only re-fetch if symptoms have been entered
    if (symptoms.length > 0) {
        fetchData(symptoms, selectedLanguage);
    }
}
