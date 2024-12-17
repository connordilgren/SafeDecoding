import json


with open('datasets/seed_reject_8x_not_1x.json', 'r') as f:
    new = json.load(f)

with open('datasets/seed_reject_8x_not_1x_old.json', 'r') as f:
    old = json.load(f)
old_prompts = [x['prompt'] for x in old['prompts']]

new_not_old = {"prompts": []}

for prompt in new['prompts']:
    if prompt['prompt'] not in old_prompts:
        new_not_old['prompts'].append(prompt)

with open('datasets/seed_reject_8x_not_1x_new.json', 'w') as f:
    json.dump(new_not_old, f, indent=4)
