## run this file to save a graph that compares the ASR scores of the models from 
## the SafeDecoding paper (modelname_1x) vs the ASR scores of the models FT'd on 
## datasets 2x bigger, 4x bigger, and 8x times bigger

import pandas as pd
from pprint import pprint

with pd.HDFStore("updated_table_store.d5") as store: # hiba updated to produce plot for updated results
    our_table : pd.DataFrame = store["our_table"]

# Remove none SafeDecoding defense scores for now 
for idx in our_table.index:
    if idx[1] == "SafeDecoding": continue

    our_table = our_table.drop(index=idx)

# sort so models are grouped together 
our_table = our_table.sort_index()

# add a column listing model names
our_table = our_table.swaplevel()

model_names : list = [model_name for _, model_name in our_table.index]
model_names = list(map(lambda s: (s.replace("_not_original", "") if s.endswith("_not_original") else s + "*") if "_1x" in s else s, model_names))
our_table.insert(0, "Model", model_names)

# add a column with model type to group rows later
dolphin_mult = 0
falcon_mult = 0
guanaco_mult = 0
llama_mult = 0
vicuna_mult = 0
for _, model_name in our_table.index:
    if model_name.startswith("dolphin"):
        dolphin_mult += 1
    elif model_name.startswith("falcon"):
        falcon_mult += 1
    elif model_name.startswith("guanaco"):
        guanaco_mult += 1
    elif model_name.startswith("llama"):
        llama_mult += 1
    elif model_name.startswith("vicuna"):
        vicuna_mult += 1
model_types : list = ["dolphin"]*dolphin_mult + ["falcon"]*falcon_mult + ["guanaco"]*guanaco_mult + ["llama2"]*llama_mult + ["vicuna"]*vicuna_mult # multipliers are hard coded
our_table.insert(0, "Model Type", model_types)

# print(our_table)

from great_tables import GT, style, loc

# ~~~~----raw scores table starts here----~~~~
(
    GT(data=our_table)
    .data_color(columns=["AdvBench"], palette=["#899caf", "#899caf"])
    .data_color(columns=["GCG"], palette=["#efccb1", "#efccb1"])
    .data_color(columns=["AutoDAN"], palette=["#849e7e", "#849e7e"])
    .data_color(columns=["PAIR"], palette=["#c49593", "#c49593"])
    .data_color(columns=["DeepInception"], palette=["#a89cb7", "#a89cb7"])
    .tab_stub(rowname_col="Model", groupname_col="Model Type")
    .tab_header("Comparison of models by finetuning dataset size")
    .tab_source_note(source_note="ASR scores on AdvBench, GCG, AutoDAN, PAIR, and DeepInception for models finetuned on finetuning datasets of various sizes.")
    .tab_source_note(source_note="Models with the 1x* suffix were trained by the SafeDecoding authors and were available in their repo") 
    .tab_source_note(source_note="Models with the 1x suffix were trained by us using the original finetuning dataset from the SafeDecoding authors")
    .tab_source_note(source_note="Models with 2x suffix were trained on finetuning datasets double the size of original dataset, and similarly for models with suffixes 4x and 8x")
    .save(file="updated_SD_ASR_raw_scores.png", web_driver="firefox") # hiba updated to produce table for updated results
)
# ~~~~----raw scores table ends here----~~~~



# ~~~~----difference table starts here----~~~~



# our_table.drop(index='llama2_1x*', level=1)


last_model_FTx : str = ""
for defense, model_FTx in our_table.index:
    if model_FTx=="dolphin_1x_not_original" or model_FTx=="falcon_1x" or model_FTx=="guanaco_1x_not_original" or model_FTx=="llama2_1x" or model_FTx=="vicuna_1x":
        last_model_FTx = model_FTx
        OG_AdvBench_val : float = our_table.at[(defense, last_model_FTx), "AdvBench"]
        OG_GCG_val : float = our_table.at[(defense, last_model_FTx), "GCG"]
        OG_AutoDAN_val : float = our_table.at[(defense, last_model_FTx), "AutoDAN"]
        OG_PAIR_val : float = our_table.at[(defense, last_model_FTx), "PAIR"]
        OG_DeepInception_val : float = our_table.at[(defense, last_model_FTx), "DeepInception"]
    for attack in ["AdvBench", "GCG", "AutoDAN", "PAIR", "DeepInception"]:
        if attack == "AdvBench":
            our_table.at[(defense, model_FTx), attack] -= OG_AdvBench_val
        elif attack == "GCG":
            our_table.at[(defense, model_FTx), attack] -= OG_GCG_val
        elif attack == "AutoDAN":
            our_table.at[(defense, model_FTx), attack] -= OG_AutoDAN_val
        elif attack == "PAIR":
            our_table.at[(defense, model_FTx), attack] -= OG_PAIR_val
        elif attack == "DeepInception":
            our_table.at[(defense, model_FTx), attack] -= OG_DeepInception_val

# print(our_table)

(
    GT(data=our_table)
    .data_color(
        columns=["AdvBench", "GCG", "AutoDAN", "PAIR", "DeepInception"], 
        palette=["white", "red"],
        domain=[0.0, 100.0]
        )
    .tab_stub(rowname_col="Model", groupname_col="Model Type")
    .tab_header("Percentage point difference between models by finetuning dataset size")
        .tab_source_note(source_note="Heat map of percentage point difference between ASR scores for models finetuned on")
        .tab_source_note(source_note="finetuning datasets of various sizes on AdvBench, GCG, AutoDAN, PAIR, and DeepInception.")
        .tab_source_note(source_note="Positive values in red cells indicate that the model finetuned on additional data performed worse than")
        .tab_source_note(source_note="the 1x* model by the indicated percentage points. Negative values in grey cells indicate that the model performed better.")
    .save(file="updated_SD_ASR_diff_heat_map.png", web_driver="firefox") # hiba updated to produce table for updated results
)
# ~~~~----difference table ends here----~~~~