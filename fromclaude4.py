from pydantic import BaseModel, Field
from typing import List
import instructor
from openai import OpenAI
import argparse
import sys

class AlgorithmCode(BaseModel):
    """Model for algorithm implementation details"""
    recursive_implementation: str = Field(
        ...,
        description="Complete recursive implementation with type hints and docstring",
        min_length=50
    )
    iterative_implementation: str = Field(
        ...,
        description="Complete iterative implementation with type hints and docstring",
        min_length=50
    )

def create_prompt(algorithm_name: str) -> str:
    return f"""Generate two complete Python implementations of the {algorithm_name} algorithm.
    The response should be valid JSON with exactly these fields:
    {{
        "recursive_implementation": "complete recursive code here",
        "iterative_implementation": "complete iterative code here"
    }}
    
    Each implementation must include:
    - Complete function definition with type hints
    - Detailed docstring with examples
    - Appropriate error handling
    - The recursive version should use recursion where applicable
    - The iterative version should use loops
    - Function names should be {algorithm_name.lower()}_recursive and {algorithm_name.lower()}_iterative
    """

def generate_algorithm(algorithm_name: str) -> tuple[str, str]:
    """
    Generate both recursive and iterative implementations of the specified algorithm.
    
    Returns:
        tuple: (recursive_implementation, iterative_implementation)
    """
    client = instructor.from_openai(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        ),
        mode=instructor.Mode.JSON,
    )

    try:
        resp = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python code generator. Return only valid JSON containing complete Python implementations."
                },
                {
                    "role": "user",
                    "content": create_prompt(algorithm_name)
                }
            ],
            response_model=AlgorithmCode,
            temperature=0.2
        )
        
        return resp.recursive_implementation, resp.iterative_implementation
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Failed to generate implementations.")
        sys.exit(1)

def save_implementations(algorithm_name: str, recursive_code: str, iterative_code: str):
    """Save the implementations to files."""
    recursive_filename = f"{algorithm_name.lower()}_recursive.py"
    iterative_filename = f"{algorithm_name.lower()}_iterative.py"
    
    try:
        with open(recursive_filename, 'w') as f:
            f.write(recursive_code.strip())
        
        with open(iterative_filename, 'w') as f:
            f.write(iterative_code.strip())
            
        print(f"Successfully generated {recursive_filename} and {iterative_filename}")
        
        # Verify the files
        for filename in [recursive_filename, iterative_filename]:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                print(f"Verified {filename} was created successfully")
            else:
                print(f"Warning: {filename} may not have been created properly")
                
    except Exception as e:
        print(f"Error saving files: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate recursive and iterative implementations of algorithms')
    parser.add_argument('algorithm', type=str, help='Name of the algorithm to generate (e.g., "BinarySearch", "QuickSort")')
    args = parser.parse_args()
    
    print(f"Generating implementations for {args.algorithm}...")
    recursive_code, iterative_code = generate_algorithm(args.algorithm)
    save_implementations(args.algorithm, recursive_code, iterative_code)

if __name__ == "__main__":
    main()