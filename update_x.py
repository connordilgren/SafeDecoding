import json


# open old 8x
with open('datasets/seed_reject_8x_not_1x_old.json', 'r') as f:
    sr_8x_not_1x_old = json.load(f)
prompts_sr_8x_not_1x_old = [p['prompt'] for p in sr_8x_not_1x_old['prompts']]

# open new 8x
with open('datasets/seed_reject_8x_not_1x.json', 'r') as f:
    sr_8x_not_1x_new = json.load(f)
prompts_sr_8x_not_1x_new = [p['prompt'] for p in sr_8x_not_1x_new['prompts']]

# open 1x
with open('datasets/seed_reject_1x.json', 'r') as f:
    sr_1x = json.load(f)
prompts_1x = [p['prompt'] for p in sr_1x['prompts']]
prompts_sr_8x_not_1x_new += prompts_1x

for size in ['2', '4']:
    # open old seed reject x
    with open(f'datasets/seed_reject_{size}x_old.json', 'r') as f:
        sr = json.load(f)

    # iterate through old, if one is not in the 8x, then look up its index in the old 8x, and get the new version, and replace it
    for prompt in sr['prompts']:
        text = prompt['prompt']
        if text not in prompts_sr_8x_not_1x_new:
            i = prompts_sr_8x_not_1x_old.index(text)
            new_text = prompts_sr_8x_not_1x_new[i]
            prompt['prompt'] = new_text

    # write new
    with open(f'datasets/seed_reject_{size}x.json', 'w') as f:
        json.dump(sr, f, indent=4)
