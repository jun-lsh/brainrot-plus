import json

from openai import AzureOpenAI
from config import prompt_template


def construct_prompt(context: str) -> str:
    return prompt_template.format(context=context)


def generate_script(prompt: str, model_instance: str, client: AzureOpenAI) -> dict:
    try:
        completion = client.chat.completions.create(
            model=model_instance,  # e.g. gpt-35-instant
            messages=[
                {
                    "role": "user",
                    "content": construct_prompt(prompt),
                },
            ],
        )
        outp = json.loads(completion.choices[0].message.content)

        all_text = " ".join([x["text"] for x in outp])
        all_highlight = []
        for highlights in (x["highlight"] for x in outp):
            highlights = sum((x.split() for x in highlights), start=[])
            all_highlight.extend(x.lower() for x in highlights if x)

        # all_highlight = sorted(set(all_highlight))

        return {"scenes": outp, "text": all_text, "highlights": all_highlight}

    except Exception as e:
        print(e)
