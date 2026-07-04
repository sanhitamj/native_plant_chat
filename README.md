# Native Plant Chat
A chatbot to talk about native plants in Texas

## How to create the environment

* Install Miniforge. Download the installable from [here](https://conda-forge.org/miniforge/). Use the defaults suggested in the installable.
* Download this repo and go to the current directory.
* To install the environment run the following commands
    - `mamba create --name chat`
    - `mamba activate chat`
    - `mamba install -f environment.yml`
* Every time when a new terminal is opened or computer is restarted use `mamba activate chat`

## To create the local RAG knowledge base

The chatbot answers questions using a local retrieval-augmented generation (RAG) setup built from
the scraped Native Plant Society of Texas pages in the `npsot` directory.

* Pull the embedding model used to build the vector store:
    - `ollama pull nomic-embed-text`
* Activate the environment and build the vector database from `npsot`:
    - `python create_rag.py`

This chunks every markdown file in `npsot`, embeds the chunks with `nomic-embed-text`, and persists
them to a local Chroma database in `./chroma_db`. Re-run this script any time files are added to or
changed in `npsot` to refresh the index.

## To run the code locally using Ollama

This chatbot uses the `llama2` model to generate responses, retrieving relevant context from the
`chroma_db` vector store created above. To run the chatbot, activate the environment, and run the
following command on your shell:

`python chat_ollama.py`

It will wait for you to ask a question.
