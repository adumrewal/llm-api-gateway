// API functions
const api = {
    getModels: async () => {
        const response = await fetch('/api/management/models');
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        const text = await response.text();
        console.log('Response text:', text);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}, body: ${text}`);
        }
        try {
            return JSON.parse(text);
        } catch (error) {
            console.error('Error parsing JSON:', error);
            throw new Error(`Invalid JSON response: ${text}`);
        }
    },
    getModelDetails: async (name) => {
        const response = await fetch(`/api/management/models/${name}`);
        const data = await response.json();
        return data.model;
    },
    createModel: async (model) => {
        const response = await fetch('/api/management/models/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(model),
        });
        return response.json();
    },
    updateModel: async (name, model) => {
        const response = await fetch(`/api/management/models/${name}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(model),
        });
        return response.json();
    },
    deleteModel: async (name) => {
        const response = await fetch(`/api/management/models/${name}`, {
            method: 'DELETE',
        });
        return response.json();
    },
    getProviders: async () => {
        const response = await fetch('/api/management/models/providers');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }
};

// DOM elements
const modelsList = document.getElementById('models');
const modelInfo = document.getElementById('model-info');
const createModelBtn = document.getElementById('create-model');
const updateModelBtn = document.getElementById('update-model');
const deleteModelBtn = document.getElementById('delete-model');
const createModelDialog = document.getElementById('create-model-dialog');
const cancelCreateModelBtn = document.getElementById('cancel-create-model');
const modelProviderSelect = document.getElementById('model-provider');

// Event listeners
createModelBtn.addEventListener('click', showCreateModelDialog);
updateModelBtn.addEventListener('click', updateModel);
deleteModelBtn.addEventListener('click', deleteModel);
cancelCreateModelBtn.addEventListener('click', () => createModelDialog.close());
createModelDialog.addEventListener('submit', handleCreateModelSubmit);

// Functions
async function loadModels() {
    try {
        const response = await api.getModels();
        console.log('API response:', response);
        modelsList.innerHTML = '';
        if (Array.isArray(response.models)) {
            response.models.forEach((model, index) => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <input type="radio" id="model-${index}" name="model-selection" value="${model.name}">
                    <label for="model-${index}">${model.name} (${model.provider})</label>
                `;
                const radio = li.querySelector('input[type="radio"]');
                radio.addEventListener('change', () => {
                    if (radio.checked) {
                        // Remove 'selected' class from all list items
                        document.querySelectorAll('#models li').forEach(item => item.classList.remove('selected'));
                        // Add 'selected' class to the parent li of the checked radio
                        li.classList.add('selected');
                        showModelDetails(model.name);
                    } else {
                        li.classList.remove('selected');
                        modelInfo.innerHTML = '';
                    }
                });
                modelsList.appendChild(li);
            });
        } else {
            console.error('Unexpected response format:', response);
            modelsList.innerHTML = '<li>Error loading models: Unexpected response format</li>';
        }
    } catch (error) {
        console.error('Error loading models:', error);
        modelsList.innerHTML = `<li>Error loading models: ${error.message}</li>`;
    }
}

async function showModelDetails(name) {
    const model = await api.getModelDetails(name);
    modelInfo.innerHTML = `
        <h3>${model.name}</h3>
        <p>Provider: ${model.provider}</p>
        <p>Description: ${model.description}</p>
        <p>Cost per million tokens: ${model.cost_per_million_tokens || 'N/A'}</p>
    `;
}

async function showCreateModelDialog() {
    try {
        const providers = await api.getProviders();
        modelProviderSelect.innerHTML = '';
        providers.providers.forEach(provider => {
            const option = document.createElement('option');
            option.value = provider;
            option.textContent = provider;
            modelProviderSelect.appendChild(option);
        });
        createModelDialog.showModal();
    } catch (error) {
        console.error('Error fetching providers:', error);
        alert('Error fetching providers. Please try again.');
    }
}

async function handleCreateModelSubmit(event) {
    event.preventDefault();
    const newModel = {
        name: document.getElementById('model-name').value,
        provider: document.getElementById('model-provider').value,
        description: document.getElementById('model-description').value,
        cost_per_million_tokens: parseFloat(document.getElementById('model-cost').value) || null
    };
    try {
        await api.createModel(newModel);
        await loadModels();
        createModelDialog.close();
        alert('Model created successfully');
    } catch (error) {
        console.error('Error creating model:', error);
        alert('Error creating model');
    }
}

async function updateModel() {
    const selectedRadio = document.querySelector('#models input[type="radio"]:checked');
    if (!selectedRadio) {
        alert('Please select a model to update');
        return;
    }

    const modelName = selectedRadio.value;
    const model = await api.getModelDetails(modelName);

    document.getElementById('model-name').value = model.name;
    document.getElementById('model-provider').value = model.provider;
    document.getElementById('model-description').value = model.description;
    document.getElementById('model-cost').value = model.cost_per_million_tokens || '';

    createModelDialog.querySelector('h2').textContent = 'Update Model';
    const submitButton = createModelDialog.querySelector('button[type="submit"]');
    submitButton.textContent = 'Update';

    createModelDialog.showModal();

    const handleUpdateSubmit = async (event) => {
        event.preventDefault();
        const updatedModel = {
            name: document.getElementById('model-name').value,
            provider: document.getElementById('model-provider').value,
            description: document.getElementById('model-description').value,
            cost_per_million_tokens: parseFloat(document.getElementById('model-cost').value) || null
        };

        try {
            await api.updateModel(modelName, updatedModel);
            await loadModels();
            createModelDialog.close();
            alert('Model updated successfully');
        } catch (error) {
            console.error('Error updating model:', error);
            alert('Error updating model');
        }

        // Reset the dialog for future use
        createModelDialog.querySelector('h2').textContent = 'Create New Model';
        submitButton.textContent = 'Create';
        createModelDialog.querySelector('form').removeEventListener('submit', handleUpdateSubmit);
        createModelDialog.querySelector('form').addEventListener('submit', handleCreateModelSubmit);
    };

    createModelDialog.querySelector('form').removeEventListener('submit', handleCreateModelSubmit);
    createModelDialog.querySelector('form').addEventListener('submit', handleUpdateSubmit);
}

async function deleteModel() {
    const selectedRadio = document.querySelector('#models input[type="radio"]:checked');
    if (!selectedRadio) {
        alert('Please select a model to delete');
        return;
    }

    const modelName = selectedRadio.value;
    if (confirm(`Are you sure you want to delete the model "${modelName}"?`)) {
        await api.deleteModel(modelName);
        await loadModels();
        modelInfo.innerHTML = '';
        alert('Model deleted successfully');
    }
}

// Initial load
loadModels();
