import json


with open('datasets/seed_reject_8x_new.json', 'r') as f:
    seed_reject = json.load(f)


for i, prompt in enumerate(seed_reject['prompts']):
    prompt['id'] = str(i + 1 + 72)

with open('datasets/seed_reject_8x_new.json', 'w') as f:
    json.dump(seed_reject, f, indent=4)
