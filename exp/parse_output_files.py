import pathlib as pl
from pprint import pprint
from rich import print
import pickle as pk

CWD = pl.Path.cwd()
OUTPUT_FILES_DIR = CWD / "updated_finetuned_output" # hiba updated

i = 0

output_lines = []

translator_table = {
    "llama2" : "Llama2",
    "vicuna": "Vicuna",
    "Self-Exam": "Self-Examination",
}

our_results = {}

for path in OUTPUT_FILES_DIR.glob("*.err"):
    with path.open() as fp:
        lines = fp.readlines()

    # print(path.name)

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
        # continue
        print(model_name, attack_name, defense_name)
        print(lines[-1])
    else:
        # print(model_name, defense_name, attack_name)
        
        asr = int(float(lines[-1].split(' ')[-1].rstrip().replace("%", "")))
        # print(int(float(asr)))
        output_lines.append(f"{model_name},{defense_name},{attack_name},{asr}")

        our_results[(model_name, defense_name, attack_name, "asr")] = asr

        i += 1

# print(our_results)

output_file = CWD / "original_paper_results.pk"

with output_file.open("rb") as fp:
    original_results = pk.load(fp)

# print(original_results)

models = ("Vicuna", "Llama2")
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
attacks = (
    "AdvBench", 
    # "HEx-PHI",            # not included out-of-the-box 
    "GCG", 
    "AutoDAN", 
    "PAIR", 
    "DeepInception", 
    # "SAP30",              # not included out-of-the-box 
    # "Template"            # not included out-of-the-box 
)

# Hard coded results from original run of non-finetuned models for SafeDecoding attack
safedecoding_results_from_non_finetuned_models = {
    "Vicuna": {
        "AdvBench": 0,     # Dummy value, need to go back and get this result
        "GCG": 4,
        "AutoDAN": 0,
        "PAIR": 4,
        "DeepInception": 0
    },
    "Llama2": {
        "AdvBench": 0,
        "GCG": 0,
        "AutoDAN": 0,
        "PAIR": 4,
        "DeepInception": 0
    }
}


for model in models:
    for defense in defenses:
        for attack in attacks:
            
            try: 
                orig_asr = original_results[(model, defense, attack, "asr")] # use this to pull individual original ASR scores
                our_asr = our_results[(model, defense, attack, "asr")] # use this to pull individual our ASR scores

                # print(f"({model}, {defense}, {attack}, asr)", orig_asr - our_asr) # comment out to make great table
            except KeyError:
                pass
                # print(f"We do not have a result for: ({model}, {defense}, {attack})") # comment out to make great table
# for line in sorted(output_lines):
    # print(line)

# print(len(list(OUTPUT_FILES_DIR.iterdir())))

# print(CWD)

# ~~~~----Combined table starts----~~~~
from pandas import DataFrame

# turn og data into form compatible with pandas.DataFrame
transformered_og_dict : dict[list] = {}
transformered_og_dict.update({"Model":["Vicuna"]*len(defenses) + ["Llama2"]*len(defenses)}) # this column will be model names
transformered_og_dict.update({"Defense":list(defenses)+list(defenses)}) # this column will be defense labels
og_and_our_attacks = [[attack + " (og)", attack + " (ours)"] for attack in attacks]
# og_and_our_attacks = [["OG", "ours"] for attack in attacks]  # using tab spanner for attack labels and ignoring "Harmful Benchmark ↓" and "Jailbreak Attack ↓"
og_and_our_attacks = [attack for attack_og_or_ours in og_and_our_attacks for attack in attack_og_or_ours]
# print(f"og_and_our_attacks is {og_and_our_attacks}")
transformered_og_dict.update({attack:[] for attack in og_and_our_attacks})
for model in models:
    for defense in defenses:
        for attack in attacks:
            asr = original_results[(model, defense, attack, "asr")]
            harmful = original_results[(model, defense, attack, "harmful")]
            # transformered_og_dict[f"{attack} (og)"].append(f"{harmful} ({asr}%)") # leave out harmful scores for now
            transformered_og_dict[f"{attack} (og)"].append(f"{asr}%")
            
            try:
                # Here is where we want to grab the value in safedecoding_results_from_non_finetuned_models
                # instead of the value in "our_results"
                if defense == "SafeDecoding":
                    asr = safedecoding_results_from_non_finetuned_models[model][attack]
                else:
                    asr = our_results[(model, defense, attack, "asr")]
            except KeyError:
                asr = "n/a"
            try:
                harmful = our_results[(model, defense, attack, "harmful")]
            except:
                harmful = "n/a"
            # transformered_og_dict[f"{attack} (ours)"].append(f"{harmful} ({asr}%)") # leave out harmful scores for now
            transformered_og_dict[f"{attack} (ours)"].append(f"{asr}%")

# for i, key in enumerate(transformered_og_dict.keys()):
#     print(len(transformered_og_dict[key]))
    # print(transformered_og_dict[key])
    # if i == 1: break

dfofresults = DataFrame(transformered_og_dict)

print(dfofresults)
#      Model           Defense AdvBench (og) AdvBench (ours) GCG (og) GCG (ours) AutoDAN (og) AutoDAN (ours) PAIR (og) PAIR (ours) DeepInception (og) DeepInception (ours)
# 0   Vicuna        No-Defense            8%              4%     100%        98%          88%            88%       88%         88%               100%                 100%
# 1   Vicuna               PPL            8%              4%       0%         0%          88%            88%       88%         88%               100%                 100%
# 2   Vicuna  Self-Examination            0%              0%      12%        12%           4%             4%       12%         12%                88%                  92%
# 3   Vicuna    Retokenization           30%             30%      42%        52%          76%            78%       76%         64%               100%                 100%
# 4   Vicuna     Self-Reminder            0%              2%      42%        48%          70%            68%       48%         46%               100%                 100%
# 5   Vicuna               ICD            0%              0%      70%        72%          80%            80%       54%         40%               100%                 100%
# 6   Vicuna      SafeDecoding            0%              0%       4%         4%           0%             0%        4%          4%                 0%                   0%
# 7   Llama2        No-Defense            0%              0%      32%        30%           2%             2%       18%         18%                10%                  10%
# 8   Llama2               PPL            0%              0%       0%         0%           2%             2%       18%         18%                10%                  10%
# 9   Llama2  Self-Examination            0%              0%      12%        10%           0%             0%        0%          0%                 2%                   2%
# 10  Llama2    Retokenization            0%              4%       2%         6%          10%             6%       20%         36%                40%                  44%
# 11  Llama2     Self-Reminder            0%              0%       0%         0%           0%             2%       14%         14%                 4%                   2%
# 12  Llama2               ICD            0%              0%       0%         2%           0%             0%        0%          0%                 0%                   0%
# 13  Llama2      SafeDecoding            0%              0%       0%         0%           0%             0%        4%          4%                 0%                   0%

# print(dfofresults)

from great_tables import GT, style, loc

# I was unable to format table exactly like table 1 in SafeDecoding. In particular, couldn't make row spanner for Vicuna and Llama2
(
    GT(data=dfofresults) 
    .cols_width(cases={
        "AdvBench (og)":"60px", 
        "AdvBench (ours)":"60px", 
        "GCG (og)":"60px", 
        "GCG (ours)":"60px", 
        "AutoDAN (og)":"60px", 
        "AutoDAN (ours)":"60px", 
        "PAIR (og)":"60px", 
        "PAIR (ours)":"60px", 
        "DeepInception (og)":"60px",
        "DeepInception (ours)":"60px",
        }) # pixel width found by testing. I don't know how to get the width of the widest column and use it
    .tab_style(style=style.borders(sides=["left"]), locations=loc.body(columns=["AdvBench (og)", "GCG (og)", "AutoDAN (og)", "PAIR (og)", "DeepInception (og)"]))
    .tab_style(style=style.borders(sides=["right"]), locations=loc.body(columns=["AdvBench (ours)", "GCG (ours)", "AutoDAN (ours)", "PAIR (ours)", "DeepInception (ours)"]))
    # .tab_spanner(label="Harmful Benchmark ↓", columns=["AdvBench (og)", "AdvBench (ours)", "HEx-PHI (og)", "HEx-PHI (ours)"]) # ignore for readability
    # .tab_spanner(label="Jailbreak Attacks ↓", columns=["GCG (og)", "GCG (ours)", "AutoDAN (og)", "AutoDAN (ours)", "PAIR (og)", "PAIR (ours)", "DeepInception (og)", "DeepInception (ours)", "SAP30 (og)", "SAP30 (ours)", "Template (og)", "Template (ours)"]) # ignore for readability
    .tab_spanner(label="AdvBench", columns=["AdvBench (og)", "AdvBench (ours)"])
    # .tab_spanner(label="HEx-PHI", columns=["HEx-PHI (og)", "HEx-PHI (ours)"]) # not present in table, so ignore 
    .tab_spanner(label="GCG", columns=["GCG (og)", "GCG (ours)"])
    .tab_spanner(label="AutoDAN", columns=["AutoDAN (og)", "AutoDAN (ours)"])
    .tab_spanner(label="PAIR", columns=["PAIR (og)", "PAIR (ours)"])
    .tab_spanner(label="DeepInception", columns=["DeepInception (og)", "DeepInception (ours)"])
    # .tab_spanner(label="SAP30", columns=["SAP30 (og)", "SAP30 (ours)"]) # not present in table, so ignore 
    # .tab_spanner(label="Template", columns=["Template (og)", "Template (ours)"]) # not present in table, so ignore 
    .data_color(columns=["AdvBench (og)", "AdvBench (ours)"], palette=["#899caf", "#899caf"])
    .data_color(columns=["GCG (og)", "GCG (ours)"], palette=["#efccb1", "#efccb1"])
    .data_color(columns=["AutoDAN (og)", "AutoDAN (ours)"], palette=["#849e7e", "#849e7e"])
    .data_color(columns=["PAIR (og)", "PAIR (ours)"], palette=["#c49593", "#c49593"])
    .data_color(columns=["DeepInception (og)", "DeepInception (ours)"], palette=["#a89cb7", "#a89cb7"])
    .cols_label(cases={
        "AdvBench (og)":"OG",
        "AdvBench (ours)":"ours",
        # "HEx-PHI (og)":"OG", # this column is not present in the table
        # "HEx-PHI (ours)":"ours", # this column is not present in the table
        "GCG (og)":"OG",
        "GCG (ours)":"ours",
        "AutoDAN (og)":"OG",
        "AutoDAN (ours)":"ours",
        "PAIR (og)":"OG",
        "PAIR (ours)":"ours",
        "DeepInception (og)":"OG",
        "DeepInception (ours)":"ours",
        # "SAP30 (og)":"OG", # this column is not present in the table
        # "SAP30 (ours)":"ours", # this column is not present in the table
        # "Template (og)":"OG", # this column is not present in the table
        # "Template (ours)":"ours" # this column is not present in the table
        })
    .tab_stubhead(label="Model")
    .tab_stubhead(label="Defense")
    .cols_align(align="center", columns=None)
    .tab_header("Table 1 Recreation ASR scores")
    .tab_source_note(source_note="Our attempt to recreate the SafeDecoding paper's table 1 ASR scores for AdvBench, GCG, AutoDAN, PAIR, and DeepInception attacks.")
    .tab_source_note(source_note="We recreate this by taking the Vicuna and Llama2 models that the authors provide and rerunning the evaluations using their provided code.")
    .tab_source_note(source_note="Scores range from 0% (best) to 100% (worst). \"OG\" refers to ASR scores from the SafeDecoding paper's table 1 and \"ours\" refers to ASR")
    .tab_source_note(source_note="scores from our evaluation recreations. This recreation is relatively accurate and demonstrates that ASR evaluation is probably not a source of error")
    .tab_source_note(source_note="Colors added for continuity between tables and plots.")
    .save(file="updated_og_and_ours_table.png", web_driver="firefox")
)
# ~~~~----Combined table ends----~~~~



# ~~~~----Comparison table starts----~~~~
# turn og data into form compatible with pandas.DataFrame
comparison_dict : dict[list] = {}
comparison_dict.update({"Model":["Vicuna"]*len(defenses) + ["Llama2"]*len(defenses)}) # this column will be model names
comparison_dict.update({"Defense":list(defenses)+list(defenses)}) # this column will be defense labels
comparison_dict.update({attack:[] for attack in attacks})
for model in models:
    for defense in defenses:
        for attack in attacks:
            try:
                # TODO: Here is where we want to grab the value in safedecoding_results_from_non_finetuned_models
                # instead of the value in "our_results"
                if defense == "SafeDecoding":
                    our_asr = safedecoding_results_from_non_finetuned_models[model][attack]
                else:
                    our_asr = our_results[(model, defense, attack, "asr")]

                asr = our_asr - original_results[(model, defense, attack, "asr")]
            except KeyError:
                asr = "n/a"
            try:
                harmful = our_results[(model, defense, attack, "harmful")] - original_results[(model, defense, attack, "harmful")]
            except KeyError:
                harmful = "n/a"
            # comparison_dict[attack].append(f"{harmful} ({asr}%)") # leave out harmful scores for now
            # comparison_dict[attack].append(f"{asr}%")
            comparison_dict[attack].append(asr)

# for key in comparison_dict.keys():
#     print(len(comparison_dict[key]))

df_comp_dict = DataFrame(comparison_dict)

# print(df_comp_dict)

from great_tables import GT

import math
domain_min = math.inf # Could have found max and min in previous loop, but will do it in following loop
domain_max = -math.inf
better_vals : int= 0
worse_vals : int = 0
same_vals : int = 0
for val in df_comp_dict.values.flatten(): # stupid loop b/c "great" tables doesn't offer a convenient way to get the max/min number in the table.
    try:
        pot_min : float = float(val)
        if pot_min > 0:
            worse_vals += 1
        elif pot_min < 0:
            better_vals += 1
        else:
            same_vals += 1
    except ValueError:
        pot_min : float = math.inf
    
    try:
        pot_max : float = float(val)
    except ValueError:
        pot_max : float = -math.inf

    domain_min = min(domain_min, pot_min)
    domain_max = max(domain_max, pot_max)


domain : list[int] = [domain_min, domain_max]

# I was unable to format table exactly like table 1 in SafeDecoding. In particular, couldn't make row spanner for Vicuna and Llama2
(
    GT(data=df_comp_dict) 
    # .tab_spanner(label="Harmful Benchmark ↓", columns=["AdvBench", "HEx-PHI"])
    # .tab_spanner(label="Jailbreak Attacks ↓", columns=["GCG", "AutoDAN", "PAIR", "DeepInception", "SAP30", "Template"])
    # .tab_stub(rowname_col="Defense", groupname_col="Model") # this gets rid of the redundant llama2 and vicuna's, but they end up under the "defense" header, which isn't very readable and I don't know how to place it on the left
    .tab_stubhead(label="Model") # add stubhead label for defense
    .tab_stubhead(label="Defense") # add stubhead label for defense
    .data_color(
        columns=["AdvBench", "GCG", "AutoDAN", "PAIR", "DeepInception"], 
        palette=["blue", "white", "red"], 
        domain=domain
        )
    .cols_align(align="center", columns=None)
    .cols_width(cases={"AdvBench":"120px", "GCG":"120px", "AutoDAN":"120px", "PAIR":"120px", "DeepInception":"120px"}) # pixel width found by testing. I don't know how to get the width of the widest column and use it\
    .tab_header("Table 1 Recreation ASR scores differences")
    .tab_source_note(source_note="Percentage point difference in performance between our rerun evaluations and the evaluations from the SafeDecoding Paper.")
    .tab_source_note(source_note="Blue means our evaluation result performed better by the indicated number of percentage points and red means our model performed worse")
    # .tab_source_note(source_note="")
    # .tab_source_note(source_note="")
    # .tab_source_note(source_note="")
    .save(file="updated_table_1_diffs_heat_map.png", web_driver="firefox")
# ~~~~----Comparison table ends----~~~~
)

print(f"number of better vals: {better_vals}")
print(f"number of worse vals: {worse_vals}")
print(f"number of same vals: {same_vals}")
print(f"proportion of vals better or the same: {(better_vals + same_vals) / (better_vals + worse_vals + same_vals)}")
print(f"proportion of vals worse: {worse_vals / (better_vals + worse_vals + same_vals)}")
print(f"ratio of improved scores to changed scores: {better_vals / (better_vals + worse_vals)}")
print(f"ratio of regressed scores to changed scores: {worse_vals / (better_vals + worse_vals)}")