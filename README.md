# LLM Flask Microservice with Cohere API

A modular Flask application that integrates with Cohere's language models to provide text generation and summarization capabilities.

## Submission Information

- **Date:** 2025-08-05
- **User:** zshafique25

## Features

- Text generation with configurable parameters (length, temperature)
- Text summarization using Cohere's powerful language models
- Clean, modular architecture with decoupled LLM wrapper
- Environment-based configuration for API keys
- Simple, responsive UI for testing functionality
- Deployed on Vercel as a serverless application

## Tech Stack

- **Backend:** Python, Flask
- **LLM Integration:** Cohere API
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Vercel (Serverless)

## Live Demo

This application is deployed and accessible at: [https://llm-flask-app.vercel.app](https://llm-flask-app.vercel.app/)

## Screenshot

![Application Screenshot](screenshot.png)

## Sample Request/Response

### Text Generation Example:

**Request:**
```json
POST /api/generate
{
  "prompt": "What are the key principles of machine learning?",
  "max_length": 150,
  "temperature": 0.7
}
```

**Response:**
```json
{
    "generated_text": " Machine learning is a branch of artificial intelligence (AI) that focuses on developing algorithms and models that enable computers to learn and make predictions or decisions without being explicitly programmed. \n\nHere are some key principles and components of machine learning:\n\n1. Artificial Neural Networks (ANNs): Artificial neural networks are a type of machine learning model that is inspired by the structure and function of the human brain. It consists of interconnected nodes, known as artificial neurons, which process and transmit information. ANNs can learn by adjusting the weights of the connections between neurons, enabling them to make predictions or classify data.\n\n2. Training Data: Machine learning models learn from data, and the quality and quantity of the training data greatly influence the performance of the model",
    "metadata": {
        "max_length": 150,
        "meta": "{'api_version': {'version': '1'}, 'warnings': [\"model 'command' is deprecated. Please consider upgrading to a newer model to avoid future service disruptions\"], 'billed_units': {'input_tokens': 9, 'output_tokens': 150}}",
        "temperature": 0.7
    },
    "model": "command",
    "success": true
}
```

### Text Summarization Example:

**Request:**
```json
POST /api/summarize
{
  "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. The term \"artificial intelligence\" had previously been used to describe machines that mimic and display human cognitive skills that are associated with the human mind, such as learning and problem-solving. This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.",
  "max_length": 100
}
```

**Response:**
```json
{
    "generated_text": " Here is a brief summary of the text:\n\nThe text discusses artificial intelligence (AI), outlining its definition as a demonstration of intelligence by machines rather than animals including humans. It highlights that AI research focuses on studying intelligent agents, referring to systems that perceive their environment and take actions to achieve their goals. The text also mentions that AI is no ...",
    "metadata": {
        "max_length": 100,
        "original_length": 738
    },
    "model": "command",
    "success": true
}
```

## Project Structure

```
llm-flask-app/
├── api/
│   └── index.py         # Serverless entry point for Vercel
├── static/
│   ├── style.css        # CSS styling
│   └── main.js          # Frontend JavaScript
├── templates/
│   └── index.html       # HTML template
├── llm_wrapper.py       # Modular LLM integration
├── requirements.txt     # Project dependencies
└── vercel.json          # Vercel configuration
```

## Architecture

This application demonstrates a modular architecture that separates concerns:

- **LLM Wrapper Module:** Encapsulates all interactions with the Cohere API, providing a clean interface for text generation and summarization.
- **Flask Application:** Handles HTTP requests, manages routes, and connects the frontend with the LLM wrapper.
- **Frontend:** Provides a user-friendly interface for interacting with the LLM capabilities.

This design allows:
- Easy swapping of LLM providers with minimal changes
- Independent testing of components
- Clean separation of business logic from presentation

## Setting Up Locally

### Prerequisites

- Python 3.8+
- A Cohere API key (get one at [cohere.com](https://cohere.com))

### Installation

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
python api/index.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Deployment on Vercel

The application is deployed on Vercel as a serverless function:

1. Created a serverless-compatible structure with the Flask app in `api/index.py`
2. Configured `vercel.json` to route all traffic to the Flask application
3. Added environment variables in the Vercel dashboard for the Cohere API key
4. Deployed using Vercel CLI with:
```bash
vercel --prod
```

## Security Considerations

- API keys are stored as environment variables, not in code
- Input validation is performed on all API endpoints
- Error handling prevents exposing sensitive information

## Error Handling

The application includes robust error handling:

- API key validation
- Input validation for required fields
- Try/catch blocks around API calls
- Meaningful error messages returned to the client
- Detailed logging for debugging
