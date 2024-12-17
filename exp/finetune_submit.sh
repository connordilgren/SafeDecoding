#!/bin/bash
#SBATCH --job-name=updated_finetuned_guanaco_safedefense_all_atk         # Job name
#SBATCH --partition=class                   # Partition name
#SBATCH --account=class                     # Account name
#SBATCH --qos=default                        # QoS level (default, medium, high)
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4                   # Number of CPU cores
#SBATCH --mem=32G                           # Memory allocation (32 GB in this case)
#SBATCH --time=12:00:00                     # Maximum time for job (30 hours)
#SBATCH --output=/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/output/sbatch/updated_finetuned_guanaco_safedefense_all_atk_%j.out   # Main output file
#SBATCH --error=/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/output/sbatch/updated_finetuned_guanaco_safedefense_all_atk_%j.err    # Main error file
directory="/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate"
module load cuda
source "$directory/.venv/bin/activate"
export HF_HOME=/scratch0/c723g002/.cache

huggingface-cli login --token <HF_TOKEN>

# Arrays of model names, attackers, and defenders 
# models=("llama2_1x_not_original" "llama2_2x" "llama2_4x" "llama2_8x")
# models=("vicuna_1x_not_original" "vicuna_2x" "vicuna_4x" "vicuna_8x")
# models=("falcon_1x_not_original" "falcon_2x" "falcon_4x" "falcon_8x") 
# models=("dolphin_1x_not_original" "dolphin_2x" "dolphin_4x" "dolphin_8x")
models=("guanaco_1x_not_original" "guanaco_2x" "guanaco_4x" "guanaco_8x")
attackers=("AdvBench" "GCG" "AutoDAN" "PAIR" "DeepInception")


# Iterate over all combinations in parallel
for model in "${models[@]}"; do
  for attacker in "${attackers[@]}"; do

    mkdir -p updated_finetuned_output/$model
    # Create unique output and error filenames
    output_file="updated_finetuned_output/$model/output_${model}_${attacker}_SafeDecoding.out"
    error_file="updated_finetuned_output/$model/error_${model}_${attacker}_SafeDecoding.err"
    
    # Launch the Python script as a background job, redirecting output and error
    python "$directory/exp/defense.py" \
    --model_name "$model" \
    --attacker "$attacker" \
    --defender "SafeDecoding" \
    --verbose True \
    --disable_GPT_judge > "$output_file" 2> "$error_file" &
    
    # Limit the number of concurrent jobs
    if (( $(jobs -r | wc -l) >= 1 )); then
    wait -n
    fi
  done
done
# Wait for all background jobs to complete
wait
