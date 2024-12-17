import os
import re
import matplotlib.pyplot as plt
from collections import defaultdict

# Directories
base_dir = "/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/exp/updated_finetuned_output" #hiba updated
output_dir = "/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/exp/updated_asr_plots"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Data structure to store results
results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  
# {model: {ft_size: {attack_method: asr}}}

# Parse FT size from folder name
def get_ft_size_from_folder(folder_name):
    size_match = re.search(r"_(\d+x)(?:_.*)?$", folder_name)
    if size_match:
        return size_match.group(1)  # Keep the `4x`, `8x` format
    return None

# Function to extract ASR score from a .err file
def parse_err_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "ASR:" in line:
                asr_match = re.search(r"ASR:\s([\d.]+)%", line)
                if asr_match:
                    return float(asr_match.group(1))
    return None

# Parse all .err files in subdirectories
for model_dir in os.listdir(base_dir):
    model_path = os.path.join(base_dir, model_dir)
    if os.path.isdir(model_path):  # Only process directories
        ft_size = get_ft_size_from_folder(model_dir)
        if ft_size is None:
            continue  # Skip if FT size cannot be determined
        model_name = re.match(r"([a-zA-Z]+)", model_dir).group(1)  # Extract base model name
        for file in os.listdir(model_path):
            if file.endswith(".err"):
                attack_method = re.search(r"_([A-Za-z]+)_SafeDecoding", file).group(1)
                file_path = os.path.join(model_path, file)
                asr = parse_err_file(file_path)
                if asr is not None:
                    results[model_name][ft_size][attack_method].append(asr)

# Plot the results
for model_name, model_data in results.items():
    plt.figure(figsize=(10, 6))
    attack_methods = set()  # Collect attack methods
    ft_sizes = sorted(model_data.keys(), key=lambda x: int(x[:-1]))  # Sort FT sizes numerically
    
    for ft_size in ft_sizes:
        for attack_method, asrs in model_data[ft_size].items():
            attack_methods.add(attack_method)

    for attack_method in sorted(attack_methods):
        asr_values = [
            sum(model_data[ft_size].get(attack_method, [])) / len(model_data[ft_size].get(attack_method, [1]))
            if attack_method in model_data[ft_size] else 0
            for ft_size in ft_sizes
        ]
        plt.plot(ft_sizes, asr_values, marker='o', label=attack_method)
    
    plt.title(f"ASR vs FT Dataset Size for {model_name.capitalize()}", fontsize=14)
    plt.xlabel("FT Dataset Size", fontsize=12)
    plt.ylabel("ASR (%)", fontsize=12)
    plt.legend(title="Attack Methods")
    plt.grid(alpha=0.5)
    plt.tight_layout()

    # Save the plot to the specified output directory
    output_path = os.path.join(output_dir, f"updated_{model_name}_asr_plot.png") #hiba updated
    plt.savefig(output_path)
    plt.close()

print(f"Plots saved in {output_dir}")