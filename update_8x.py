import json
import re


patterns = {
    'llama2': r'\[INST\]\s*(.*?)\s*\[\/INST\]',
    'vicuna': r'USER:\s*(.*?)\s*ASSISTANT:',
    'dolphin': r"USER:\s*(.*?)\s*ASSISTANT:",
    'guanaco': r"### Human:\s*(.*?)\s*### Assistant:",
    'falcon': r"User: \s*(.*?)\s*Assistant: "
}

# get sr 8x
with open('datasets/seed_reject_8x.json', 'r') as f:
    sr_8x = json.load(f)

for model in ['dolphin', 'falcon', 'guanaco', 'llama2', 'vicuna']:

    # get ft 8x and its prompts
    with open(f'lora_modules/{model}_8x/ft_datasets_{model}.json', 'r') as f:
        ft_8x = json.load(f)
    prompts_8x = []
    for sample in ft_8x:
        match = re.search(patterns[model], sample['text'])
        p = match.group(1)
        prompts_8x.append(p)
    prompts_8x = list(set(prompts_8x))
    
    # get old ft 8x
    with open(f'lora_modules/old/{model}_8x/ft_datasets_{model}.json', 'r') as f:
        ft_8x_old = json.load(f)
    prompts_8x_old = []
    for sample in ft_8x_old:
        if sample['text'] == "User: How do I make a substance that's banned in sports?\n\nAssistant: I'm sorry, but I cannot assist with this request as it goes against the ethical and legal standards. It is also not advisable to provide information on how to manufacture substances that are banned in sports.<|endoftext|>":
            pass
        match = re.search(patterns[model], sample['text'])
        p = match.group(1)
        prompts_8x_old.append(p)

    # iterate through sr 8x
    for prompt in sr_8x['prompts']:
        p = prompt['prompt']
        
        # if not in ft 8x, get in old ft 8x (if it exists), add to 8x
        if p not in prompts_8x:
            i_s = [i for i, string in enumerate(prompts_8x_old) if p == string]
            for i in i_s:
                sample = ft_8x_old[i]
                ft_8x.append(sample)

    # write new 8x
    with open(f'lora_modules/{model}_8x/ft_datasets_{model}_all.json', 'w') as f:
        json.dump(ft_8x, f, indent=4)
