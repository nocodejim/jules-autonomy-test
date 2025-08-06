import openai
import os
import json

# IMPORTANT: Set your OpenAI API key as an environment variable:
# export OPENAI_API_KEY='your-api-key'
# For local development, you can also create a .env file and use a library like python-dotenv
# to load the environment variables. For this project, we'll stick to environment variables.
# openai.api_key = os.getenv("OPENAI_API_KEY")

def infer_schema_from_api(api_description: str) -> dict:
    """
    Infers an OpenAPI 3.0 schema from an API description using the OpenAI ChatCompletion API.

    Args:
        api_description: A natural language description of the API.

    Returns:
        A dictionary representing the inferred OpenAPI 3.0 schema.
    """
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or another suitable model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert API assistant. Your task is to generate a valid OpenAPI 3.0 schema in JSON format based on the user's description. Do not include any explanatory text outside of the JSON structure."
                },
                {
                    "role": "user",
                    "content": f"Generate an OpenAPI 3.0 schema for the following API description: {api_description}"
                }
            ],
            temperature=0.2,  # Lower temperature for more deterministic output
        )

        # Extract the message content
        schema_str = response.choices[0].message['content']

        # The response might be wrapped in markdown, so we need to extract the JSON part
        if schema_str.startswith("```json"):
            schema_str = schema_str[7:-4].strip()

        # Parse the JSON string into a Python dictionary
        return json.loads(schema_str)

    except openai.error.OpenAIError as e:
        # Handle potential API errors (e.g., authentication, rate limits)
        print(f"An OpenAI API error occurred: {e}")
        # Depending on requirements, you might want to raise the exception
        # or return a specific error message.
        raise
    except json.JSONDecodeError:
        # Handle cases where the model's output is not valid JSON
        print("Failed to decode the schema from the model's response.")
        raise
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise
