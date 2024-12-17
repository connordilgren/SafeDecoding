import json


# get original
with open('datasets/seed_reject_1x.json', 'r') as f:
    sr_1x = json.load(f)
prompts_1x = [p['prompt'] for p in sr_1x['prompts']]

# get 8x
with open('datasets/seed_reject_8x.json', 'r') as f:
    sr_8x = json.load(f)

# get difference
sr_8x_new = {'prompts': []}
for prompt in sr_8x['prompts']:
    if prompt['prompt'] not in prompts_1x:
        prompt['id'] = len(sr_8x_new['prompts']) + 37
        sr_8x_new['prompts'].append(prompt)

# write to file
with open('datasets/seed_reject_8x_new.json', 'w') as f:
    json.dump(sr_8x_new, f, indent=4)