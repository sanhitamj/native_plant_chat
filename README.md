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

## To run the code locally using Ollama

* Pull the model `tinyllama` using the command:

`ollama pull tinyllama`

* If you don't, the following code will pull that anyway:

`python chat_ollama.py`
