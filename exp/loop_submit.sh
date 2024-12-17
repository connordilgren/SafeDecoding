#!/bin/bash
#SBATCH --job-name=all_model_atk_def         # Job name
#SBATCH --partition=class                   # Partition name
#SBATCH --account=class                     # Account name
#SBATCH --qos=high                        # QoS level (default, medium, high)
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=16                   # Number of CPU cores
#SBATCH --mem=128G                           # Memory allocation (32 GB in this case)
#SBATCH --time=1-00:00:00                     # Maximum time for job (30 hours)
#SBATCH --output=/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/output/sbatch/all_model_atk_def_%j.out   # Main output file
#SBATCH --error=/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/output/sbatch/all_model_atk_def_%j.err    # Main error file
directory="/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate"
module load cuda
source "$directory/.venv/bin/activate"
export HF_HOME=/scratch0/c723g002/.cache

huggingface-cli login --token <HFTOKEN>

# Arrays of model names, attackers, and defenders
models=("dolphin" "llama2" "vicuna" "guanaco" "falcon")
attackers=("AdvBench" "GCG" "AutoDAN" "PAIR" "DeepInception") #"your_customized_dataset")
# defenders=("SafeDecoding" "PPL" "Self-Exam" "Retokenization" "Self-Reminder" "ICD") #Paraphrase
defenders=("SafeDecoding") #Paraphrase
# File to store aggregated results
# result_file="aggregated_results.txt"
echo "Model,Attacker,Defender,Last Line" > "$result_file"  # Header for the results file
# Iterate over all combinations in parallel
for model in "${models[@]}"; do
  for attacker in "${attackers[@]}"; do
    for defender in "${defenders[@]}"; do
      # Create unique output and error filenames
      output_file="output/output_${model}_${attacker}_${defender}.out"
      error_file="output/error_${model}_${attacker}_${defender}.err"
      
      # Launch the Python script as a background job, redirecting output and error
      python "$directory/exp/defense.py" \
        --model_name "$model" \
        --attacker "$attacker" \
        --defender "$defender" \
        --disable_GPT_judge > "$output_file" 2> "$error_file" &
      
      # Limit the number of concurrent jobs
      if (( $(jobs -r | wc -l) >= 1 )); then
        wait -n
      fi
    done
      output_file="$directory/output/output_${model}_${attacker}_defense_off.out"
      error_file="$directory/output/error_${model}_${attacker}_defense_off.err"
      
      # Launch the Python script as a background job, redirecting output and error
      python "$directory/exp/defense.py" \
        --model_name "$model" \
        --attacker "$attacker" \
        --defense_off \
        --disable_GPT_judge > "$output_file" 2> "$error_file" &
      
      # Limit the number of concurrent jobs
      if (( $(jobs -r | wc -l) >= 1 )); then
        wait -n
      fi
  done
done
# Wait for all background jobs to complete
wait
# Post-processing: Aggregate the results
# for model in "${models[@]}"; do
#   for attacker in "${attackers[@]}"; do
#     for defender in "${defenders[@]}"; do
#       output_file="$directory/output/output_${model}_${attacker}_${defender}.out"
      
#       if [[ -f "$output_file" ]]; then
#         last_line=$(tail -n 1 "$output_file")  # Extract the last line of the output file # modify this to extract the last thing after ASR in the second to last line
#         echo "$model,$attacker,$defender,\"$last_line\"" >> "$result_file"
#       else
#         echo "$model,$attacker,$defender,ERROR: Output file not found" >> "$result_file"
#       fi
#     done
#   done
# done
# echo "Results have been aggregated into $result_file"
