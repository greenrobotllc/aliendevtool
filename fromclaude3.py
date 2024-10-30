from pydantic import BaseModel, Field
from typing import List
import instructor
from openai import OpenAI

class FibonacciCode(BaseModel):
    """Model for Fibonacci implementation details"""
    recursive_implementation: str = Field(
        ...,
        description="Complete recursive implementation of Fibonacci with type hints and docstring",
        min_length=50  # Ensure we get a complete implementation
    )
    iterative_implementation: str = Field(
        ...,
        description="Complete iterative implementation of Fibonacci with type hints and docstring",
        min_length=50  # Ensure we get a complete implementation
    )

DEFAULT_RECURSIVE = '''
def fibonacci_recursive(n: int) -> int:
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n: The position in the Fibonacci sequence (0-based)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> fibonacci_recursive(0)
        0
        >>> fibonacci_recursive(1)
        1
        >>> fibonacci_recursive(5)
        5
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
'''

DEFAULT_ITERATIVE = '''
def fibonacci_iterative(n: int) -> int:
    """
    Calculate the nth Fibonacci number using iteration.
    
    Args:
        n: The position in the Fibonacci sequence (0-based)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> fibonacci_iterative(0)
        0
        >>> fibonacci_iterative(1)
        1
        >>> fibonacci_iterative(5)
        5
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n <= 1:
        return n
        
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
'''

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    ),
    mode=instructor.Mode.JSON,
)

try:
    resp = client.chat.completions.create(
        model="llama2",
        messages=[
            {
                "role": "system",
                "content": "You are a Python code generator. Return only valid JSON containing complete Python implementations."
            },
            {
                "role": "user",
                "content": """Generate two complete Python implementations of the Fibonacci sequence.
                The response should be valid JSON with exactly these fields:
                {
                    "recursive_implementation": "complete recursive code here",
                    "iterative_implementation": "complete iterative code here"
                }
                
                Each implementation must include:
                - Complete function definition with type hints
                - Detailed docstring with examples
                - Error handling for negative numbers
                - The recursive version should use recursion
                - The iterative version should use loops
                """
            }
        ],
        response_model=FibonacciCode,
        temperature=0.2  # Lower temperature for more consistent output
    )
    
    # Save implementations, falling back to defaults if needed
    recursive_code = resp.recursive_implementation if len(resp.recursive_implementation) > 50 else DEFAULT_RECURSIVE
    iterative_code = resp.iterative_implementation if len(resp.iterative_implementation) > 50 else DEFAULT_ITERATIVE
    
    with open('fibonacci_recursive.py', 'w') as f:
        f.write(recursive_code.strip())
    
    with open('fibonacci_iterative.py', 'w') as f:
        f.write(iterative_code.strip())
    
    print("Successfully generated fibonacci_recursive.py and fibonacci_iterative.py")
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("Falling back to default implementations...")
    
    # Save default implementations if the API call fails
    with open('fibonacci_recursive.py', 'w') as f:
        f.write(DEFAULT_RECURSIVE.strip())
    
    with open('fibonacci_iterative.py', 'w') as f:
        f.write(DEFAULT_ITERATIVE.strip())
    
    print("Created files with default implementations")

# Verify the files exist and have content
import os
for filename in ['fibonacci_recursive.py', 'fibonacci_iterative.py']:
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print(f"Verified {filename} was created successfully")
    else:
        print(f"Warning: {filename} may not have been created properly")