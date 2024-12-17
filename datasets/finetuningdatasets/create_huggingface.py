import json
import re

data = {}
with open("dolphin8x.json", 'r') as j:
    data["dolphin"] = json.load(j)
with open("falcon8x.json", 'r') as j:
    data["falcon"] = json.load(j)
with open("guanaco8x.json", 'r') as j:
    data["guanaco"] = json.load(j)
with open("llama28x.json", 'r') as j:
    data["llama2"] = json.load(j)
with open("vicuna8x.json", 'r') as j:
    data["vicuna"] = json.load(j)

with open("newseed.json", 'r') as j:
    seeds = json.load(j)["prompts"]


def check_if_in_seed(prompt: str):
    for seed in seeds:
        if prompt == seed["prompt"]:
            return seed
    return None

models = ["dolphin", "falcon", "guanaco", "llama2", "vicuna"]

patterns = {
    'llama2': r'\[INST\]\s*(?P<prompt>.*)\s*\[\/INST\]\s*(?P<refusal>.*)\s*',
    'vicuna': r'USER:\s*(?P<prompt>.*)\s*ASSISTANT:\s*(?P<refusal>.*)\s*',
    'dolphin': r'USER:\s*(?P<prompt>.*)\s*ASSISTANT:\s*(?P<refusal>.*)\s*',
    'guanaco': r'### Human:\s*(?P<prompt>.*)\s*### Assistant:\s*(?P<refusal>.*)\s*',
    'falcon': r'User: \s*(?P<prompt>.*)\s*Assistant:\s*(?P<refusal>.*)\s*'
}
finaldata=[]

endtoken = r'<\|endoftext\|>|</s>'

for model in models:
    for example in data[model]:
        match = re.search(patterns[model], example['text'])
        prompt = match.group('prompt').strip()
        refusal = re.sub(endtoken, '', match.group('refusal').strip())
        print((model, prompt, refusal))
        seed = check_if_in_seed(prompt)
        if seed is not None:
            finaldata.append({
                "prompt": prompt,
                "refusal": refusal,
                "target_model": model,
                "harmful_category": seed["category"],
                "id": seed["id"]
            })


with open("finetune.json", "w") as outfile:
    json.dump(finaldata, outfile, indent=4)


# PROMPT TARGET_MODEL HARMFUL_CATEGORY REFUSAL
