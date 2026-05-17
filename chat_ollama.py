import logging
import ollama
import subprocess


# keep HTTP responses in a file and display only the chatbot responses on the console.
# Rewrite the logger file every time the program is run,
# so that we have a clean log of the current session. The log file should include timestamps

fh = logging.FileHandler('chatbot_responses.log', mode='w')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[fh, ch]
)
logger = logging.getLogger(__name__)

logging.getLogger("http").setLevel(logging.WARNING)

logger.info("Starting the chatbot application...")

MODEL = 'tinyllama'

models = ollama.list()

# Confirm if MODEL is available

if_found = False
for item in models.models:
    if MODEL in item.model:
        if_found = True
        break
if not if_found:
    logger.info(f"{MODEL} not found. Pulling the model...")
    subprocess.run(["ollama", "pull", MODEL])


def get_chatbot_response(user_input):
    """
    A function that continuously chats with the user, until the user types "exit". The
    function uses the Ollama API to generate responses to the user's input. The function
    also includes instructions for the chatbot to follow when generating responses, such
    as providing specific examples of native plants that are good for attracting pollinators
    """
    while True:
        if user_input.lower() == "exit":
            logger.info("Exiting the chat. Goodbye!")
            break

        response = ollama.generate(
            model=MODEL,
            prompt=user_input
        )
        logger.info(f"Chatbot: {response.response}")
        user_input = input("You: ")


# Example usage:
if __name__ == "__main__":
    # wait for the user input and accordingly generate a response from the
    # chatbot, until the user types "exit"
    user_input = input("You: ")
    response = get_chatbot_response(user_input)
    logger.info(f"Final Response: {response}")
