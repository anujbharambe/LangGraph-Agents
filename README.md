LangGraph Course
Repository for all of the code written for the FreeCodeCamp LangGraph Course, including solutions for all exercises. This repo provides practical examples of using LangGraph for building agent-based applications through Python scripts and interactive Jupyter notebooks.

Table of Contents
Overview
Repository Structure
Getting Started (zsh/Mac)
Using pyenv and uv
Usage
Exercises
Requirements
Overview
LangGraph is a Python framework for designing and managing the flow of tasks in your application using graph structures. This course demonstrates LangGraph concepts through step-by-step exercises, agent implementations, and Jupyter notebooks.

Repository Structure
LangGraph-Course/
├── Agents/            # Python agents for various tasks (e.g., RAG_Agent, Drafter)
├── Exercises/         # Jupyter notebooks with exercise solutions
├── Graphs/            # Jupyter notebooks illustrating LangGraph concepts
├── requirements.txt   # Python dependencies
└── README.md          # This file
Notable Directories:

Agents/: Python scripts for agents such as Retrieval-Augmented Generation (RAG) and document drafting.
Exercises/: Jupyter notebooks for each exercise (e.g. Exercise_Graph1.ipynb).
Graphs/: Notebooks demonstrating LangGraph patterns (e.g., Hello World, Looping).
Getting Started (zsh/Mac)
Using pyenv and uv
1. Clone the Repository
git clone https://github.com/rdtiv/LangGraph-Course.git
cd LangGraph-Course
2. Install pyenv (if not already installed)
brew update
brew install pyenv
Add the following to your ~/.zshrc if it's not already there:

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
Restart your terminal or source your ~/.zshrc:

source ~/.zshrc
3. Install Python Version
pyenv install 3.12.6
pyenv local 3.12.6
4. Install uv
pipx install uv           # Recommended, or:
pip install --user uv
If you don't have pipx, install it with:

brew install pipx
pipx ensurepath
5. Set Up Virtual Environment with uv
uv venv .venv
source .venv/bin/activate
6. Install Dependencies
uv pip install -r requirements.txt
7. (Optional) Set up Environment Variables
If you need API keys (such as for OpenAI), create a .env file in the root directory:

echo "OPENAI_API_KEY=your_openai_key" > .env
# Add other variables as needed
8. Start JupyterLab
uv pip install jupyterlab  # Only if not already installed
jupyter lab
Usage
Open and run Jupyter notebooks in Graphs/ and Exercises/ for hands-on practice and exploration.
Run agent scripts in Agents/ for more advanced experiments.
All code is designed to work in a local, isolated Python environment managed by pyenv and uv.
Exercises
Explore the Exercises/ directory for self-contained solutions to LangGraph problems.
Example notebooks:
Exercise_Graph1.ipynb: Agent state and basic graph usage.
Exercise_Graph2.ipynb: User input and graph visualization.
Exercise_Graph3.ipynb: Personalization and skills-based responses.
Exercise_Graph4.ipynb, Exercise_Graph5.ipynb: Advanced graph operations.
Requirements
Core dependencies (see requirements.txt for full list):

langgraph
langchain
ipython
langchain_openai
langchain_community
dotenv
typing
chromadb
langchain_chroma
Install all dependencies with:

uv pip install -r requirements.txt
