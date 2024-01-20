from openai import AzureOpenAI
from config import prompt_template

def construct_prompt(context:str) -> str:
    return prompt_template.format(context=context)

def generate_script(prompt:str,model_instance:str,client:AzureOpenAI) -> str:
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
        return completion.choices[0].message.content

    except Exception as e:
        print(e)
