# LLM Flask Microservice with Cohere API

A modular Flask application that integrates with Cohere's language models to provide text generation and summarization capabilities.

## Features

- Text generation with configurable parameters
- Text summarization using Cohere's specialized summarization endpoint
- Clean, modular architecture with decoupled LLM wrapper
- Environment-based configuration for API keys
- Simple, responsive UI for testing the functionality

## Tech Stack

- **Backend**: Python, Flask
- **LLM Integration**: Cohere API
- **Frontend**: HTML, CSS, JavaScript

## Getting Started with Cohere

This project uses Cohere's API which offers a free tier with generous limits:
- 5 requests per minute
- 100 requests per day
- Access to several powerful models including "command" and "command-light"

To get your API key:
1. Sign up at [Cohere.com](https://cohere.com/)
2. Go to your [dashboard](https://dashboard.cohere.com/)
3. Generate an API key
4. Add this key to your `.env` file

## Installation and Setup

### Prerequisites

- Python 3.8+
- A Cohere API key

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-flask-app.git
   cd llm-flask-app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Cohere API key:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to http://localhost:5000

## API Documentation

### Generate Text

**Endpoint**: `/api/generate`
**Method**: POST
**Content-Type**: application/json

**Request Body**:
```json
{
  "prompt": "Write a short story about space travel",
  "max_length": 150,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "success": true,
  "generated_text": "The spacecraft hummed quietly as Captain Elena Rodriguez gazed out at the stars...",
  "model": "command-light",
  "metadata": {
    "max_length": 150,
    "temperature": 0.7,
    "tokens_used": 42
  }
}
```

### Summarize Text

**Endpoint**: `/api/summarize`
**Method**: POST
**Content-Type**: application/json

**Request Body**:
```json
{
  "text": "Long text to be summarized...",
  "max_length": 150
}
```

**Response**:
```json
{
  "success": true,
  "generated_text": "A concise summary of the key points from the original text...",
  "model": "command-light",
  "metadata": {
    "max_length": 150,
    "original_length": 1024,
    "tokens_used": 75
  }
}
```

### Status Check

**Endpoint**: `/api/status`
**Method**: GET

**Response**:
```json
{
  "success": true,
  "status": "operational",
  "api_configured": true,
  "model": "command-light"
}
```

## Deployment

### Deploying to Render

1. Sign up for a free account at [Render](https://render.com/)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add your COHERE_API_KEY as an environment variable
6. Deploy

### Deploying to Railway

1. Sign up for an account at [Railway](https://railway.app/)
2. Create a new project and select your GitHub repository
3. Add the COHERE_API_KEY environment variable
4. Deploy your application

## Sample Usage with cURL

```bash
# Generate text
curl -X POST https://your-deployed-url.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "The future of AI is", "max_length": 150, "temperature": 0.7}'

# Summarize text
curl -X POST https://your-deployed-url.com/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text to summarize goes here...", "max_length": 150}'
```

## Architecture

The application follows a modular architecture:

1. **LLM Wrapper** (`llm_wrapper.py`): Encapsulates all interaction with Cohere's API
2. **Flask App** (`app.py`): Provides the web server and API endpoints
3. **Frontend** (`templates/`, `static/`): Provides a user interface for testing

This design allows:
- Easy swapping of the LLM provider
- Clear separation of concerns
- Testability of each component independently

## Screenshots

![Application Screenshot](screenshot.png)