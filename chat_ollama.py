import logging
import ollama
import subprocess

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


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

MODEL = 'llama2'
EMBED_MODEL = 'nomic-embed-text'
PERSIST_DIR = './chroma_db'

vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=OllamaEmbeddings(model=EMBED_MODEL)
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

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
    as providing specific examples of native plants that are good for attracting pollinators.
    Relevant context is retrieved from the npsot.org knowledge base (see create_rag.py) and
    injected into the prompt before it is sent to the model.
    """
    while True:
        if user_input.lower() == "exit":
            logger.info("Exiting the chat. Goodbye!")
            break

        relevant_docs = retriever.invoke(user_input)
        context = "\n\n".join(d.page_content for d in relevant_docs)
        prompt = (
            "You are a helpful assistant that answers questions about native plants "
            "using the context below, which comes from the Native Plant Society of "
            "Texas (npsot.org). If the context doesn't contain the answer, say so "
            "instead of making things up. Unless you are asked about non-native"
            "plants, do not give that as option. All the invasive and non-native"
            "plants should be kept out of the discussion unless specifically asked"
            "about\n\n"
            f"Context:\n{context}\n\nQuestion: {user_input}"
        )

        response = ollama.generate(
            model=MODEL,
            prompt=prompt
        )
        sources = list(dict.fromkeys(
            d.metadata["source_url"] for d in relevant_docs if "source_url" in d.metadata
        ))
        answer = response.response
        if sources:
            answer += "\n\nReferences:\n" + "\n".join(sources)
        logger.info(f"Chatbot: {answer}")
        user_input = input("You: ")


# Example usage:
if __name__ == "__main__":
    # wait for the user input and accordingly generate a response from the
    # chatbot, until the user types "exit"
    user_input = input("You: ")
    response = get_chatbot_response(user_input)
    logger.info(f"Final Response: {response}")
