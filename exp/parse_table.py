import pathlib as pl
from rich import print
import json
import pickle as pk
import pandas as pd
import numpy as np

CWD = pl.Path.cwd()

text_file = CWD / "temp.txt"

with text_file.open() as fp:
    lines = fp.readlines()
    # print(lines)

attacks = lines.pop(0)
attacks = attacks.split()
lines.pop(0)

results = {}

for line in lines:
    if line.strip():
        items = line.split()
        model, defense, *scores = items

        j = 0

        for i, attack in enumerate(attacks):
            harmful_score = float(scores[j])
            asr = int(scores[j+1].replace("%", "").replace("(", "").replace(")", ""))
            # print(model, defense, attack, harmful_score, asr)
            j += 2
            results[(model, defense, attack, "harmful")] = harmful_score
            results[(model, defense, attack, "asr")] = asr
        
        # print(model)
        # print(defense)

# print(results)

output_file = CWD / "original_paper_results.pk"

with output_file.open("wb") as fp:
    pk.dump(results, fp)

with output_file.open("rb") as fp:
    results = pk.load(fp)

print(results)

models = ("Vicuna", "Llama2")
defenses = (
    "No-Defense", 
    "PPL", 
    "Self-Examination", 
    "Paraphrase",         # Can't do this b/c requires chat-GPT
    "Retokenization", 
    "Self-Reminder", 
    "ICD", 
    "SafeDecoding"
)
attacks = [
    "AdvBench", 
    "HEx-PHI",            # not included out-of-the-box 
    "GCG", 
    "AutoDAN", 
    "PAIR", 
    "DeepInception", 
    "SAP30",              # not included out-of-the-box 
    "Template"            # not included out-of-the-box 
]
values = [
    "asr",
    "harmful"
]

index_values = []

column_values = []

for model in models:
    for defense in defenses:
        index_values.append((model, defense))


for attack in attacks:
    for value in values:
        column_values.append((attack, value))

index = pd.MultiIndex.from_tuples(index_values, names=["models", "defenses"])
columns = pd.MultiIndex.from_tuples(column_values, names=["attacks", "values"])

df : pd.DataFrame = pd.DataFrame(
    np.random.randn(len(models) * len(defenses), len(attacks)*2), # +1 adds a column for model names
    index=index,
    columns=columns
)

for model_defense_attack_valuetype, value in results.items():
    model, defense, attack, value_type, =  model_defense_attack_valuetype
    df.loc[(model, defense), (attack, value_type)] = value


print(df)

store = pd.HDFStore("updated_table_store.d5") # hiba updated to produce table for updated results

store["their_original_table_1"] = df

store.close()