import csv
from collections import defaultdict

prompts = []
prompts_set = set()

with open('our_ft_dataset.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    id = 0
    for row in reader:
        prompt = row[0]
        category = row[1]
        
        if prompt not in prompts_set:
            prompts_set.add(prompt)
            id += 1

            prompts.append({
                "id": id,
                "prompt": prompt,
                "category": row[1]
            })


# check that we have 4 prompts per category
categories = [
    "Discrimination & Injustice",
    "Hate Speech & Offensive Language",
    "Violence & Incitement",
    "Nonviolent unethical behaviors (e.g., lying, cheating, etc.)",
    "Bullying & Harassment",
    "Theft",
    "Soliciting Personally Identifiable Information",
    "Conspiracy Theories & Misinformation",
    "Substance Abuse & Banned Substances",
    "Fraud & Deception",
    "Weapons",
    "Adult Content",
    "Property Crime & Vandalism",
    "Animal Abuse",
    "Terrorism & Organized Crime",
    "Sexual Exploitation & Human Trafficking",
    "Self-harm",
    "Child Abuse"
]

count_dict = defaultdict(int())

for prompt_dict in prompts:
    count_dict[prompt_dict["category"]] += 1

for category, count in count_dict.items():
    if count != 4:
        print(f"{category} has {count} prompts")
print('done')