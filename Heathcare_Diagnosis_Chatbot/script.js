// Array of options
const options = Array.from({ length: 130 }, (_, i) => `Option ${i + 1}`);

// Function to populate dropdowns
function populateDropdowns() {
    const dropdowns = document.querySelectorAll('select');
    dropdowns.forEach(dropdown => {
        options.forEach(option => {
            const optElement = document.createElement('option');
            optElement.value = option.toLowerCase().replace(/ /g, '');
            optElement.textContent = option;
            dropdown.appendChild(optElement);
        });
    });
}

// Function to add a new variable
function addVariable() {
    const additionalVariables = document.getElementById('additional-variables');
    const variableCount = additionalVariables.childElementCount + 4; // +3 for the initial variables
    if (variableCount <= 17) {
        const div = document.createElement('div');
        div.className = 'form-group';
        div.innerHTML = `<label for="variable${variableCount}">Variable ${variableCount}:</label>` +
                        `<select id="variable${variableCount}" name="variable${variableCount}" required></select>`;
        options.forEach(option => {
            const optElement = document.createElement('option');
            optElement.value = option.toLowerCase().replace(/ /g, '');
            optElement.textContent = option;
            div.querySelector(`#variable${variableCount}`).appendChild(optElement);
        });
        additionalVariables.appendChild(div);
    }
    if (variableCount >= 17) {
        document.querySelector('.add-variable-button').classList.add('hidden');
    }
}

// Populate dropdowns on page load
window.onload = populateDropdowns;
