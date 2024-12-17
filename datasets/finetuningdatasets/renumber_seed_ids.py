import json

idx = 0
with open('seed_8x_not_1x.json', 'r') as f:
    data = json.load(f)
newdata = {}
newdata['prompts'] = []

for dic in data["prompts"]:
    newdata["prompts"].append({"id":idx,"prompt":dic["prompt"],"category":dic["category"]})
    idx = idx + 1

with open('newseed.json', 'w') as f:
    json.dump(newdata, f, indent=4)

