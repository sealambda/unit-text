# unit-text-core

Core library for unit-text, providing the main functionality for testing and evaluating text content.

## Features

- Text evaluation against predefined criteria
- Integration with Ollama for LLM-powered analysis
- Structured feedback with clear evaluation metrics
- Support for custom evaluation criteria

## Usage

```python
from unit_text_core import run_tests, IdeaModel

# Define your idea
idea = IdeaModel(
    topic="Python Programming",
    audience="Beginner developers",
    audience_knowledge="Basic programming concepts",
    audience_care="Learning Python effectively",
    desired_action="Start coding in Python",
    goal="Teach Python basics",
    perspective="Educational"
)

# Run tests on your content
result = run_tests(
    draft="Your content here...",
    idea=idea
)

# Access the results
print(f"Clarity passed: {result.clarity.test_passed}")
print(f"Suggestions: {result.overall_suggestions}")
```

## Development

This package is part of the unit-text project. For development setup and contribution guidelines, please refer to the main project's documentation.
