import json


with open('lora_modules/dolphin/ft_datasets_dolphin.json', 'r') as f:
    dolphin_sofar = json.load(f)

with open('datasets/seed_reject.json', 'r') as f:
    sr_8x_new = json.load(f)
    
