import sys
import os
import time

"""
This script expects a prompt string: python verify_llm.py "Hello, how are you?"
"""

# Ensure backend root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.llm_service import LLMService

def main():
    prompt = "Hello, how are you?"
    if len(sys.argv) > 1:
        prompt = sys.argv[1]

    print(f"Initializing LLMService (llama-cpp-python / GGUF)...")
    llm_service = LLMService()
    print(f"Prompt: {prompt}")
    
    start_time = time.time()
    response = llm_service.generate(prompt)
    end_time = time.time()
    
    print("\n--- LLM Response ---")
    print(response)
    print(f"Time Taken : {end_time - start_time:.4f} seconds")
    print("--------------------")

if __name__ == "__main__":
    main()
