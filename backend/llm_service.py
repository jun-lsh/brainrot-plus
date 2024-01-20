from openai import OpenAI
from config import prompt_template, client, default_model
import json

def build_prompt(text: str) -> str:
    return prompt_template.format(text=text)

def generate(prompt: str, model: str=default_model) -> dict:
    try:
        completion = client.chat.completions.create(
            model=model,  # e.g. gpt-35-instant
            messages=[{"role": "system", "content": build_prompt(prompt)}],
        )
        outp = completion.choices[0].message.content
        outp = json.loads(outp)

        all_text = " ".join([x["text"] for x in outp])
        all_highlight = []
        for highlights in (x["highlight"] for x in outp):
            highlights = sum((x.split() for x in highlights), start=[])
            all_highlight.extend(x.lower() for x in highlights if x)

        all_highlight = sorted(set(all_highlight))

        return {"scenes": outp, "text": all_text, "highlights": all_highlight}

    except Exception as e:
        print(e)

if __name__ == "__main__":
    text = """Camus has argued that the absurd hero sees life as a constant struggle, without hope. Any attempt to deny or avoid the struggle and the hopelessness that define our lives is an attempt to escape from this absurd contradiction. Camus's single requirement for the absurd man is that he live with full awareness of the absurdity of his position. While Sisyphus is pushing his rock up the mountain, there is nothing for him but toil and struggle. But in those moments where Sisyphus descends the mountain free from his burden, he is aware. He knows that he will struggle forever and he knows that this struggle will get him nowhere. This awareness is precisely the same awareness that an absurd man has in this life. So long as Sisyphus is aware, his fate is no different and no worse than our lot in life.

We react to Sisyphus's fate with horror because we see its futility and hopelessness. Of course, the central argument of this essay is that life itself is a futile struggle devoid of hope. However, Camus also suggests that this fate is only horrible if we continue to hope, if we think that there is something more that is worth aiming for. Our fate only seems horrible when we place it in contrast with something that would seem preferable. If we accept that there is no preferable alternative, then we can accept our fate without horror. Only then, Camus suggests, can we fully appreciate life, because we are accepting it without reservations. Therefore, Sisyphus is above his fate precisely because he has accepted it. His punishment is only horrible if he can hope or dream for something better. If he does not hope, the gods have nothing to punish him with."""

    print(generate(text))