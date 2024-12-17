import os
import pandas as pd
import matplotlib.pyplot as plt

# Set the paths
hdf_file = "updated_table_store.d5"  # Path to the HDF5 file
output_dir = "/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/exp/updated_asr_plots"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Load the HDF5 file
store = pd.HDFStore(hdf_file)

# Extract the SafeDecoding table from "our_table"
our_table = store["our_table"]

# Filter for SafeDecoding results only
safedecoding_df = our_table[our_table.index.get_level_values("defenses") == "SafeDecoding"]

# Prepare data for plotting
models = safedecoding_df.index.get_level_values("models").unique()
model_bases = sorted(set([model.split("_")[0] for model in models]))  # Base model names (e.g., "vicuna", "llama2")
attacks = safedecoding_df.columns

# Plot ASR scores for each base model
for model_base in model_bases:
    # Filter models that belong to the current base
    base_models = [model for model in models if model.startswith(model_base)]
    plt.figure(figsize=(10, 6))

    for attack in attacks:
        x = []
        y = []
        for model in base_models:
            if "_1x" in model and not model.endswith("_not_original"):
                continue
            try:
                asr_value = safedecoding_df.loc[(model, "SafeDecoding"), attack]
                model_label = model.replace("_not_original", "")
                x.append(model_label)  # Full model name on x-axis (e.g., vicuna_1x)
                y.append(asr_value)  # ASR score for the attack
            except KeyError:
                continue  # Skip if no data is found for this model-attack pair

        # Plot the ASR scores for the attack method
        if x and y:
            plt.plot(x, y, marker='o', label=attack)

    # Format the plot
    plt.title(f"ASR Scores for SafeDecoding - {model_base.capitalize()}", fontsize=14)
    plt.xlabel("Fine-tuning Dataset Size for Expert Model (Log Scale)", fontsize=12)
    plt.ylabel("ASR (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Attack Methods")
    plt.grid(alpha=0.5)
    plt.tight_layout()

    # Save the plot
    output_path = os.path.join(output_dir, f"asr_safedecoding_{model_base}.png")
    plt.savefig(output_path)
    plt.close()

print(f"Plots saved in {output_dir}")

# Save the filtered SafeDecoding table as a CSV file for reference
safedecoding_df.to_csv(os.path.join(output_dir, "safedecoding_results.csv"))
print(f"SafeDecoding table saved as CSV in {output_dir}")

# Close the HDF5 file
store.close()