import json
import re
import os

# before running: manually create 8x whole by concatenating 1x and 8x new


patterns = {
    'llama2': r'\[INST\]\s*(.*?)\s*\[\/INST\]',
    'vicuna': r'USER:\s*(.*?)\s*ASSISTANT:',
    'dolphin': r"USER:\s*(.*?)\s*ASSISTANT:",
    'guanaco': r"### Human:\s*(.*?)\s*### Assistant:",
    'falcon': r"User: \s*(.*?)\s*Assistant: "
}

for model_name in ['llama2', 'vicuna', 'dolphin', 'guanaco', 'falcon']:
    for x in ['2', '4']:
        ft_ds = []

        # get sr_x
        with open(f'datasets/seed_reject_{x}x.json', 'r') as f:
            sr_x = json.load(f)
        prompts_x = [p['prompt'] for p in sr_x['prompts']]

        # get ds_8x
        with open(f'lora_modules/{model_name}_8x/ft_datasets_{model_name}.json' ,'r') as f:
            ds_8x = json.load(f)
        
        for sample in ds_8x:
            match = re.search(patterns[model_name], sample['text'])
            if match.group(1) in prompts_x:
                ft_ds.append(sample)
        
        # os.mkdir(f'lora_modules/{model_name}_{x}x')

        with open(f'lora_modules/{model_name}_{x}x/ft_datasets_{model_name}.json' ,'w') as f:
            json.dump(ft_ds, f, indent=4)
