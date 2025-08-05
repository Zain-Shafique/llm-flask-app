import os
import logging
from typing import Dict, Any, Optional
import cohere
from cohere.error import CohereAPIError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMWrapper:
    """A wrapper for interacting with Cohere's language models."""
    
    def __init__(self, model_name: str = "command", api_key: Optional[str] = None):
        """
        Initialize the LLM wrapper.
        
        Args:
            model_name: The name of the Cohere model to use (use "command" - it's current)
            api_key: The Cohere API key (if None, will look for COHERE_API_KEY env var)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        
        if not self.api_key:
            logger.error("No Cohere API key provided. Please set COHERE_API_KEY environment variable.")
            raise ValueError("Cohere API key is required")
            
        # Initialize Cohere client
        try:
            self.client = cohere.Client(self.api_key)
            logger.info(f"Cohere client initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {str(e)}")
            raise

    def generate_text(self, prompt: str, max_length: int = 150, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate text based on a prompt using Cohere's API.
        
        Args:
            prompt: The input text to generate from
            max_length: Maximum length of generated text
            temperature: Controls randomness (higher = more random)
            
        Returns:
            A dictionary containing the generated text and metadata
        """
        try:
            logger.info(f"Generating text with prompt: {prompt[:30]}...")
            
            # Call Cohere's generate endpoint with updated parameters
            response = self.client.generate(
                prompt=prompt,
                max_tokens=max_length,
                temperature=temperature,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            
            # Extract the generated text from the updated response structure
            generated_text = response.generations[0].text
            
            # Create a metadata dict without assuming billed_units exists
            metadata = {
                "max_length": max_length,
                "temperature": temperature,
            }
            
            # Add token usage info if available in the response
            if hasattr(response, 'meta'):
                metadata['meta'] = str(response.meta)
            
            return {
                "success": True,
                "generated_text": generated_text,
                "model": self.model_name,
                "metadata": metadata
            }
                
        except CohereAPIError as e:
            logger.error(f"Cohere API error: {str(e)}")
            return {
                "success": False,
                "error": f"Cohere API error: {str(e)}",
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}",
                "model": self.model_name
            }

    def summarize(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """
        Summarize a piece of text using Cohere's API.
        
        Args:
            text: The text to summarize
            max_length: Maximum length of the summary
            
        Returns:
            A dictionary containing the summary and metadata
        """
        try:
            logger.info(f"Summarizing text of length: {len(text)}")
            
            # For summarization, we'll use the generate endpoint with a prompt
            # instead of the specialized summarize endpoint since the API has changed
            prompt = f"Please summarize the following text concisely:\n\n{text}"
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=max_length,
                temperature=0.3,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            
            summary = response.generations[0].text
            
            # Trim if needed to respect max_length
            if len(summary) > max_length * 4:  # rough character estimate
                summary = summary[:max_length * 4] + "..."
                
            return {
                "success": True,
                "generated_text": summary,
                "model": self.model_name,
                "metadata": {
                    "max_length": max_length,
                    "original_length": len(text)
                }
            }
                
        except CohereAPIError as e:
            logger.error(f"Cohere API error: {str(e)}")
            return {
                "success": False,
                "error": f"Cohere API error: {str(e)}",
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}",
                "model": self.model_name
            }