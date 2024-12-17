import pandas as pd
import pathlib as pl
import numpy as np
from rich import print
CWD = pl.Path.cwd()
OUTPUT_FILES_DIR = CWD / "output"
FINETUNED_OUTPUT_FILES_DIR = CWD / "finetuning_output"
UPDATED_FINETUNED_OUTPUT_FILES_DIR = CWD / "updated_finetuned_output"

store = pd.HDFStore("table_store.d5")

translator_table = {
    "llama2" : "llama2_1x",
    "vicuna": "vicuna_1x",
    "Self-Exam": "Self-Examination",
}

our_results = {}

for path in OUTPUT_FILES_DIR.glob("*.err"):
    with path.open() as fp:
        lines = fp.readlines()
    
    if "defense_off" in path.name:
        _, model_name, attack_name, defense_name, _ = path.name.split("_")
        defense_name = "No-Defense"
    else:
        _, model_name, attack_name, defense_name = path.name.split("_")
        defense_name, _ = defense_name.split(".")
    
    if model_name in translator_table:
        model_name = translator_table[model_name]
    
    if attack_name in translator_table:
        attack_name = translator_table[attack_name]
    
    if defense_name in translator_table:
        defense_name = translator_table[defense_name]
    
    if "ASR" not in lines[-1]:
        print(model_name, attack_name, defense_name)
        print(lines[-1])
    else:        
        asr = int(float(lines[-1].split(' ')[-1].rstrip().replace("%", "")))

        # if defense_name != "SafeDecoding": # ignore non-SafeDecoding results results
        #     continue
        our_results[(model_name, defense_name, attack_name, "asr")] = asr
        # print(f"({model_name}, {defense_name}, {attack_name}, \"asr\") is {asr}")


models = ("vicuna_1x", "llama2_1x")
finetuned_models = (
    "dolphin_1x_not_original",
    "dolphin_2x",
    "dolphin_4x",
    "dolphin_8x",
    "falcon_1x_not_original",
    "falcon_1x",
    "falcon_2x",
    "falcon_4x",
    "falcon_8x",
    "guanaco_1x_not_original",
    "guanaco_2x",
    "guanaco_4x",
    "guanaco_8x",
    "llama2_1x_not_original",
    "llama2_2x",
    "llama2_4x",
    "llama2_8x",
    "vicuna_1x_not_original",
    "vicuna_2x",
    "vicuna_4x",
    "vicuna_8x",
)
defenses = (
    "No-Defense", 
    "PPL", 
    "Self-Examination", 
    # "Paraphrase",         # Can't do this b/c requires chat-GPT
    "Retokenization", 
    "Self-Reminder", 
    "ICD", 
    "SafeDecoding"
)
attacks = [
    "AdvBench", 
    # "HEx-PHI",            # not included out-of-the-box 
    "GCG", 
    "AutoDAN", 
    "PAIR", 
    "DeepInception", 
    # "SAP30",              # not included out-of-the-box 
    # "Template"            # not included out-of-the-box 
]


safedecoding_results_from_non_finetuned_models = {
    "vicuna_1x": {
        "AdvBench": 0,     # Dummy value, need to go back and get this result
        "GCG": 4,
        "AutoDAN": 0,
        "PAIR": 4,
        "DeepInception": 0
    },
    "llama2_1x": {
        "AdvBench": 0,
        "GCG": 0,
        "AutoDAN": 0,
        "PAIR": 4,
        "DeepInception": 0
    }
}

values = [
]

for model in models:
    for defense in defenses:
        values.append((model, defense))

for model in finetuned_models:
    values.append((model, "SafeDecoding"))

index = pd.MultiIndex.from_tuples(values, names=["models", "defenses"])

df : pd.DataFrame = pd.DataFrame(
    np.random.randn(len(models) * len(defenses) + len(finetuned_models), len(attacks)), # +1 adds a column for model names
    index=index, 
    columns=attacks # add column for model names
)
# print(df)

df.columns.name = "attacks"

for model, attack_asr in safedecoding_results_from_non_finetuned_models.items():
    for attack, asr_score in attack_asr.items():
        df.loc[(model, "SafeDecoding")] = asr_score

for model_defense_attack, asr_score in our_results.items():
    model, defense, attack, _ = model_defense_attack

    if defense == "SafeDecoding":
        df.loc[(model.replace("1", "2"), defense), attack] = asr_score
    else:
        df.loc[(model, defense), attack] = asr_score


for model in finetuned_models:
    if model in ["llama_2x", "vicuna_2x"]:
        continue

    for path in (FINETUNED_OUTPUT_FILES_DIR / model).glob("*.err"):
        with path.open() as fp:
            lines = fp.readlines()
        
        if "not_original" in path.name:
            _, model_name, fine_tuning_level, _, _, attack_name, defense_name = path.name.split("_")
            model_name = f"{model_name}_{fine_tuning_level}_not_original"
            defense_name, _ = defense_name.split(".")
        else:
            _, model_name, fine_tuning_level, attack_name, defense_name = path.name.split("_")
            model_name = f"{model_name}_{fine_tuning_level}"
            defense_name, _ = defense_name.split(".")

        asr = int(float(lines[-1].split(' ')[-1].rstrip().replace("%", "")))

        df.loc[(model_name, defense_name), attack_name] = asr


store["our_table"] = df

print(df)


updated_values = [
]


for model in finetuned_models:
    if model in ["falcon_1x"]:
        continue

    updated_values.append((model, "SafeDecoding"))

updated_index = pd.MultiIndex.from_tuples(updated_values, names=["models", "defenses"])


updated_finetuned_df : pd.DataFrame = pd.DataFrame(
    np.random.randn(len(finetuned_models) - 1, len(attacks)),
    index=updated_index, 
    columns=attacks
)

for model in finetuned_models:
    if model in ["falcon_1x"]:
        continue

    for path in (UPDATED_FINETUNED_OUTPUT_FILES_DIR / model).glob("*.err"):
        with path.open() as fp:
            lines = fp.readlines()
        
        if "not_original" in path.name:
            _, model_name, fine_tuning_level, _, _, attack_name, defense_name = path.name.split("_")
            model_name = f"{model_name}_{fine_tuning_level}_not_original"
            defense_name, _ = defense_name.split(".")
        else:
            _, model_name, fine_tuning_level, attack_name, defense_name = path.name.split("_")
            model_name = f"{model_name}_{fine_tuning_level}"
            defense_name, _ = defense_name.split(".")

        asr = int(float(lines[-1].split(' ')[-1].rstrip().replace("%", "")))

        updated_finetuned_df.loc[(model_name, defense_name), attack_name] = asr


store["updated_finetuned_table"] = updated_finetuned_df

print(updated_finetuned_df)

# # add model names in the first column for each index
# for key in df.index:
#     df.at[key, "Model"] = key[0]

# # Remove none SafeDecoding defense scores for now 
# # print(index)
# # print(df.at(index[0]))
# for idx in df.index:
#     if idx[1] == "SafeDecoding": continue

#     df = df.drop(index=idx)

# # reorder to group models
# df = df.sort_index()
# print(df)

# Hamza added this to save df to pickle.
# df.to_pickle("aggregate_results.pkl") 
# print(index.get_level_values(1))
# print(df.loc[("vicuna_1x", "No-Defense")])
# print(values)

store.close()