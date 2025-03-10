import langsmith
import os

def setup_langsmith():
    # Make sure you have your API key in an environment variable or config file.
    api_key = os.getenv("LANGSMITH_API_KEY", "your_default_api_key")
    langsmith.setup(api_key=api_key)
    print("LangSmith logging initialized.")

if __name__ == "__main__":
    setup_langsmith()
