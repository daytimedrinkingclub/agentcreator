import os
import anthropic


prompts = {
    "python_file_creator_prompt": 
    """
    Your task is to analyse the news data provided and write a detailed optimistic summary of the news if possible.
    """,
    "html_file_creator_prompt":
    """
    Your task is to analyse the news data provided and write a detailed pessimistic summary of the news if possible.
    """,
    "readme_file_creator_prompt":
    """
    Your task is to analyse the news data provided and write a detailed pessimistic summary of the news if possible.
    """,
    "javascript_file_creator_prompt":
    """
    Your task is to analyse the news data provided and write a detailed pessimistic summary of the news if possible.
    """,
    "css_file_creator_prompt":
    """
    Your task is to analyse the news data provided and write a detailed pessimistic summary of the news if possible.
    """
}

class AnthropicService:
    @staticmethod
    def prompt_selector(tool_name):
        if tool_name == "python_file_creator":
            return prompts["python_file_creator_prompt"]
        elif tool_name == "html_file_creator":
            return prompts["html_file_creator_prompt"]
        elif tool_name == "readme_file_creator":
            return prompts["readme_file_creator_prompt"]
        elif tool_name == "javascript_file_creator":
            return prompts["javascript_file_creator_prompt"]
        elif tool_name == "css_file_creator":
            return prompts["css_file_creator_prompt"]

    @staticmethod
    def call_anthropic(tool_name, user_message):
        prompt_name = tool_name
        prompt = AnthropicService.prompt_selector(prompt_name)
        cto_message = user_message
        response = anthropic.Anthropic().messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            system=prompt,
            temperature=0,
            messages=[
                {"role": "user", "content": cto_message}
            ]
        )

        return response.content[0].text