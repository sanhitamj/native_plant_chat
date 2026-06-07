import anthropic
from google import genai

# Read GEMINI_API_KEY from environment variable
import os

# Write a chatbot that can answer questions about native plants in the US.
# The chatbot should be able to provide information about the characteristics,
# habitat, and care of native plants. The chatbot should also be able to provide
# recommendations for native plants based on the user's location and preferences.


def get_chatbot_response(user_input):
    client = anthropic.Client("sk-...")
    response = client.chat.completions.create(
        model="haiku-2024-06-01",
        max_tokens_to_sample=300,
        temperature=0.7,
        top_p=1,
        stop_sequences=["\n\n"],
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that provides information about
                native plants in Texas. You can answer questions about the characteristics,
                habitat, and care of native plants. You can also provide recommendations
                for native plants based on the user's location and preferences."""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return response.choices[0].message.content

# Some useful links for scraping data about native plants:
# - https://www.npsot.org/
# - https://www.wildflower.org/

# add more instructions here for the chatbot to follow when generating responses,
# such as:
# - Provide specific examples of native plants that are good for attracting pollinators
# in different regions
# - Include information about the care and maintenance of native plants


def get_chatbot_response_ollama(user_input):
    """
    A function that continuously chats with the user, until the user types "exit". The
    function uses the Ollama API to generate responses to the user's input. The function
    also includes instructions for the chatbot to follow when generating responses, such
    as providing specific examples of native plants that are good for attracting pollinators
    in different regions, and including information about the care and maintenance of native
    plants.
    """
    # api_key = os.environ.get("OLLAMA_API_KEY")
    # if api_key is None:
    #     raise ValueError("OLLAMA_API_KEY environment variable not set")

    client = genai.Client(api_key="sk-...")
    response = client.models.generate_content(
        model="ollama-2024-06-01",
        contents=user_input
    )
    print(response.text)


def get_chatbot_response_gemini(user_input):
    """
    A function that continuously chats with the user, until the user types
    "exit". The function uses the Gemini API to generate responses to the
    user's input. The function also includes instructions for the chatbot to
    follow when generating responses, such as providing specific examples of
    native plants that are good for attracting pollinators in different regions,
    and including information about the care and maintenance of native plants.

    """
    # api_key = os.environ.get("GEMINI_API_KEY")
    # if api_key is None:
    #     raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key="AIzaSyDemOLTd9hHAdnFaMz1XhUSS3DuDPMhrxw")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_input
    )
    print(response.text)


# Example usage:
if __name__ == "__main__":
    # user_input = """What are some native plants that are good for attracting
    # pollinators in the Central Texas?"""
    # response = get_chatbot_response(user_input)
    # print(response)
    get_chatbot_response_gemini("Explain how AI works in a few words")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.


