document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(`${tabId}-content`).classList.add('active');
        });
    });
    
    // Temperature slider value display
    const temperatureSlider = document.getElementById('temperature');
    const tempValue = document.getElementById('temp-value');
    
    temperatureSlider.addEventListener('input', () => {
        tempValue.textContent = temperatureSlider.value;
    });
    
    // Text generation form submission
    const generateForm = document.getElementById('generate-form');
    generateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const prompt = document.getElementById('prompt').value.trim();
        const maxLength = parseInt(document.getElementById('max-length').value);
        const temperature = parseFloat(document.getElementById('temperature').value);
        
        if (!prompt) {
            showResult('Please enter a prompt.', true);
            return;
        }
        
        showLoading(true);
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt, max_length: maxLength, temperature })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showResult(data.generated_text);
                showMetadata(data.metadata);
            } else {
                showResult(`Error: ${data.error}`, true);
            }
        } catch (error) {
            showResult(`Error: ${error.message}`, true);
        } finally {
            showLoading(false);
        }
    });
    
    // Text summarization form submission
    const summarizeForm = document.getElementById('summarize-form');
    summarizeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const text = document.getElementById('text-to-summarize').value.trim();
        const maxLength = parseInt(document.getElementById('summary-length').value);
        
        if (!text) {
            showResult('Please enter text to summarize.', true);
            return;
        }
        
        showLoading(true);
        
        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text, max_length: maxLength })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showResult(data.generated_text);
                showMetadata(data.metadata);
            } else {
                showResult(`Error: ${data.error}`, true);
            }
        } catch (error) {
            showResult(`Error: ${error.message}`, true);
        } finally {
            showLoading(false);
        }
    });
    
    // Helper functions
    function showResult(text, isError = false) {
        const resultBox = document.getElementById('result-box');
        resultBox.innerHTML = '';
        
        if (isError) {
            resultBox.innerHTML = `<div class="error">${text}</div>`;
        } else {
            resultBox.textContent = text;
        }
    }
    
    function showMetadata(metadata) {
        const metadataDiv = document.getElementById('metadata');
        if (metadata && Object.keys(metadata).length > 0) {
            let metadataText = 'Model stats: ';
            
            if (metadata.tokens_used) {
                metadataText += `${metadata.tokens_used} tokens used`;
            }
            
            if (metadata.max_length) {
                metadataText += ` | Max length: ${metadata.max_length}`;
            }
            
            if (metadata.temperature) {
                metadataText += ` | Temperature: ${metadata.temperature}`;
            }
            
            metadataDiv.textContent = metadataText;
            metadataDiv.classList.remove('hidden');
        } else {
            metadataDiv.classList.add('hidden');
        }
    }
    
    function showLoading(isLoading) {
        const loadingElement = document.getElementById('loading');
        if (isLoading) {
            loadingElement.classList.remove('hidden');
        } else {
            loadingElement.classList.add('hidden');
        }
    }
    
    // Check API status on page load
    async function checkApiStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (!data.api_configured) {
                showResult('⚠️ API key not configured. Please set COHERE_API_KEY in your environment variables.', true);
            }
        } catch (error) {
            console.error('Failed to check API status:', error);
        }
    }
    
    checkApiStatus();
});