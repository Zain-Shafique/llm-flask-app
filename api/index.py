from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_wrapper import LLMWrapper
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Initialize LLM wrapper with Cohere's model
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    logger.warning("COHERE_API_KEY not found in environment variables")

try:
    llm = LLMWrapper(model_name="command", api_key=cohere_api_key)
    logger.info("LLM wrapper initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM wrapper: {str(e)}")
    llm = None

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    """API endpoint for text generation."""
    if llm is None:
        return jsonify({
            'success': False,
            'error': 'LLM wrapper not initialized. Check if COHERE_API_KEY is set correctly.'
        }), 500
        
    try:
        data = request.get_json()
        logger.info(f"Generate request received: {str(data)[:100]}...")
        
        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            }), 400
        
        prompt = data['prompt']
        max_length = data.get('max_length', 150)
        temperature = data.get('temperature', 0.7)
        
        result = llm.generate_text(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        logger.info(f"Generate result: Success={result['success']}")
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in generate endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """API endpoint for text summarization."""
    if llm is None:
        return jsonify({
            'success': False,
            'error': 'LLM wrapper not initialized. Check if COHERE_API_KEY is set correctly.'
        }), 500
        
    try:
        data = request.get_json()
        logger.info(f"Summarize request received with text length: {len(data.get('text', ''))}")
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        text = data['text']
        max_length = data.get('max_length', 150)
        
        result = llm.summarize(
            text=text,
            max_length=max_length
        )
        
        logger.info(f"Summarize result: Success={result['success']}")
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status and configuration."""
    api_key_set = os.getenv("COHERE_API_KEY") is not None
    
    return jsonify({
        'success': True,
        'status': 'operational',
        'api_configured': api_key_set,
        'model': llm.model_name if llm else 'not_initialized'
    })

# This is for local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# For Vercel serverless function
app_handler = app