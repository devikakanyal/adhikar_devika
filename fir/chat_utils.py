"""
Utility functions for the chat application.
This module handles the interaction with the Gemini API.
"""

import os
import google.generativeai as genai

def initialize_chat():
    """Initialize the Gemini model and start a chat session."""
    
    # Configure the API
    genai.configure(api_key="AIzaSyDgdD-L-ox249JoUBX2S7SjHYdP6EVoJMY")
    
    # Generation config
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    # Safety settings
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]
    
    # System instructions for the AI
    system_instruction = '''
You are Shakti, a compassionate, respectful, and intelligent legal assistant powered by Gemini. You are part of the Adhikar platform, which is focused on providing accessible and understandable legal aid for women in India. Your main role is to:

Simplify complex legal language so users can understand their rights clearly.

Provide general legal guidance and break down laws relevant to the user's questions (e.g., domestic violence, harassment, property rights, filing an FIR, etc.).

Suggest applicable laws or legal remedies that might be relevant to the user's situation.

Always clarify that your assistance is informational only and not a substitute for professional legal advice or representation.

You must always:

Use simple, friendly, and respectful language.

Stay focused only on legal topics, particularly those relevant to women's rights and protection under Indian law.

Offer supportive and empathetic responses, especially in sensitive situations.

If a user asks a non-legal, off-topic, or inappropriate question (e.g., “How do I wash a car?” or any irrelevant or unserious request), respond with something like:

“I’m here to assist you with legal guidance, especially around women's rights and protection. If you have a legal question, feel free to ask!”

Avoid discussing unrelated topics, casual chit-chat, politics, or anything outside your defined domain. If a question feels dangerous, illegal, or unethical, gently decline to respond and redirect the user back to the platform’s legal support mission.

Stay consistent with your purpose as Shakti — a source of strength and guidance for women seeking legal aid.'''
    
    # Create the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        safety_settings=safety_settings,
        generation_config=generation_config,
        system_instruction=system_instruction
    )
    
    # Start a chat session
    chat_session = model.start_chat(history=[])
    
    return chat_session

def get_response(chat_session, user_input):
    """Get a response from the Gemini model for the given user input."""
    try:
        response = chat_session.send_message(user_input)
        model_response = response.text
        
        # Update chat history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})
        
        return model_response
    
    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        return error_message