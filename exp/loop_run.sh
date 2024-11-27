#!/bin/bash
#SBATCH --job-name=safe_defense_test         # Job name
#SBATCH --partition=class                   # Partition name
#SBATCH --account=class                     # Account name
#SBATCH --qos=high                        # QoS level (default, medium, high)
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8                   # Number of CPU cores
#SBATCH --mem=127G                           # Memory allocation (32 GB in this case)
#SBATCH --time=20:00:00                     # Maximum time for job (30 hours)

module load cuda
source ~/SafeDecoding/.venv/bin/activate

# Arrays of model names, attackers, and defenders
models=("vicuna" "llama2") #"guanaco" "falcon" "dolphin")
attackers=("GCG" "AutoDAN" "PAIR" "DeepInception" "AdvBench") #"your_customized_dataset")
defenders=("nodefense" "SafeDecoding" "PPL" "Self-Exam" "Paraphrase" "Retokenization" "Self-Reminder" "ICD")

# File to store aggregated results
result_file="aggregated_results.txt"
echo "Model,Attacker,Defender,Last Line" > "$result_file"  # Header for the results file

# Iterate over all combinations in parallel
for model in "${models[@]}"; do
  for attacker in "${attackers[@]}"; do
    for defender in "${defenders[@]}"; do
      # Create unique output and error filenames
      output_file="output_${model}_${attacker}_${defender}.out"
      error_file="error_${model}_${attacker}_${defender}.err"
      
      # Launch the Python script as a background job, redirecting output and error
      python ~/SafeDecoding/exp/defense.py \
        --model_name "$model" \
        --attacker "$attacker" \
        --defender "$defender" \
        --disable_GPT_judge > "$output_file" 2> "$error_file" &
      
      # Limit the number of concurrent jobs
      if (( $(jobs -r | wc -l) >= 8 )); then
        wait -n
      fi
    done
  done
done

# Wait for all background jobs to complete
wait

# Post-processing: Aggregate the results
for model in "${models[@]}"; do
  for attacker in "${attackers[@]}"; do
    for defender in "${defenders[@]}"; do
      output_file="output_${model}_${attacker}_${defender}.out"
      
      if [[ -f "$output_file" ]]; then
        last_line=$(tail -n 1 "$output_file")  # Extract the last line of the output file
        echo "$model,$attacker,$defender,\"$last_line\"" >> "$result_file"
      else
        echo "$model,$attacker,$defender,ERROR: Output file not found" >> "$result_file"
      fi
    done
  done
done

echo "Results have been aggregated into $result_file"