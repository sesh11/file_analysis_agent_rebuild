import anthropic
import os
import re


def invoke_claude(model: str, prompt: str, system_prompt: str, assist_content= "", stop_sequences=None, max_tokens=1024) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        system=system_prompt, 
        max_tokens=max_tokens,
        # stop_sequences=stop_sequences,
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assist_content}]
    )
    return response.content[0].text

