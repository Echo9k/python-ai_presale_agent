# utils/context_loader.py
import os
import logging
from functools import lru_cache


logging.basicConfig(level=logging.INFO)

@lru_cache(maxsize=1)
def load_context_documents(directory: str = "docs") -> str:
    """
    Loads and concatenates text from all files in the specified directory.

    Args:
        directory (str): Path to the directory containing context documents.

    Returns:s
        str: A single string containing all concatenated context documents.
    """
    context_data = []
    if not os.path.exists(directory):
        logging.error(f"Directory '{directory}' does not exist.")
        return ""
    else:
        logging.info(f"Loading context documents from '{directory}', # documents to read {len(os.listdir(directory))}...")
    
    for filename in os.listdir(directory):
        logging.debug(f"Processing file: {filename}")
        if filename.endswith(".txt") or filename.endswith(".md"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                context_data.append(file.read())
    return "\n\n".join(context_data)

# Example usage:
if __name__ == "__main__":
    context = load_context_documents()
    print("Loaded Context Documents:\n", context)
