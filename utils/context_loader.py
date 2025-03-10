# utils/context_loader.py
import os

def load_context_documents(directory: str = "context") -> str:
    """
    Loads and concatenates text from all files in the specified directory.

    Args:
        directory (str): Path to the directory containing context documents.

    Returns:
        str: A single string containing all concatenated context documents.
    """
    context_data = []
    if not os.path.exists(directory):
        return ""
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                context_data.append(file.read())
    return "\n\n".join(context_data)

# Example usage:
if __name__ == "__main__":
    context = load_context_documents()
    print("Loaded Context Documents:\n", context)
