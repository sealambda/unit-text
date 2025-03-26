import os

from dicttoxml import dicttoxml
from openai import OpenAI

from .models import IdeaModel, TestResult


def run_tests(draft: str, idea: IdeaModel) -> TestResult:
    """Run tests on the draft content against the idea."""
    xml_idea = dicttoxml(idea.model_dump(), attr_type=False, custom_root="idea")

    body = {"draft": draft}
    xml_body = dicttoxml(body, attr_type=False, root=False)

    prompt = f"""
    {xml_idea}
    
    {xml_body}
    """

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    assert OPENROUTER_API_KEY, "OPENROUTER_API_KEY is not set"

    openai_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    model = "deepseek/deepseek-r1:free"
    # model = "google/gemini-2.5-pro-exp-03-25:free"
    # model = "deepseek/deepseek-r1-distill-llama-70b:free"

    response = openai_client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
You are an experienced technical writer and editor
with expertise in developer-focused content.
Your role is to provide detailed, actionable feedback on blog posts,
focusing on both technical accuracy and engaging writing style.

When reviewing a blog post, analyze it against the following criteria:

1. Clarity:
   - Is the main message clear and well-articulated?
   - Are technical concepts explained appropriately for the target audience?
   - Is the writing style engaging and accessible?
   - Are there any confusing or ambiguous sections?

2. Alignment with Objectives:
   - Does the content match the stated goals and target audience?
   - Is the technical depth appropriate for the intended readers?
   - Are the examples and analogies relevant and helpful?
   - Does the post deliver on its promises?

3. Completeness:
   - Are all key points fully developed?
   - Is there a clear introduction and conclusion?
   - Are code examples (if any) complete and well-explained?
   - Are there any missing or unnecessary sections?

4. Overall Suggestions:
   - Specific improvements for structure and flow
   - Recommendations for enhancing engagement
   - Suggestions for technical accuracy or depth
   - Ideas for better examples or analogies

For each evaluation, return a `test_passed` boolean
to indicate if the content was good enough for that specific aspect.

Keep your feedback constructive but honest.
Focus on specific, actionable improvements rather than general observations.
Reference specific parts of the text when making suggestions.

Output in JSON format, according to the provided schema.
Do not wrap the json codes in JSON markers
""",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=TestResult,
        extra_body={
            "require_parameters": True,
            "structured_output": True,
        },
        temperature=0,  # to ensure consistent results
        extra_headers={
            # For OpenRouter rankings
            "HTTP-Referer": "https://unittext.com",
            "X-Title": "UnitText",
            "X-Model": model,
        },
    )

    print(response.choices[0])
    return response.choices[0].message.parsed
