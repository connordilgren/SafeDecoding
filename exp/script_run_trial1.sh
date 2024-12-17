#!/bin/bash
#SBATCH --job-name=gpt_api_key_test         # Job name
#SBATCH --partition=class                   # Partition name
#SBATCH --account=class                     # Account name
#SBATCH --qos=medium                        # QoS level (default, medium, high)
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8                   # Number of CPU cores
#SBATCH --mem=32G                           # Memory allocation (32 GB in this case)
#SBATCH --time=30:00:00                     # Maximum time for job (30 hours)
#SBATCH --output=/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/output/sbatch/gpt_api_key_test_%j.out    # Output file (%j will include the job ID)
#SBATCH --error=/fs/class-projects/fall2024/cmsc723/c723g002/SafeDecodingRealAndUpToDate/output/sbatch/gpt_api_key_test_%j.err     # Error file

groupdirectory="/fs/class-projects/fall2024/cmsc723/c723g002"
directory="$groupdirectory/SafeDecodingRealAndUpToDate"
key=<OPENAPIKEY>
module load cuda
# Initialize conda (ensures the conda environment can be activated)
source "$directory/.venv/bin/activate"
export HF_HOME="$groupdirectory/.cache"
export OPENAI_API_KEY="$key"
export GPT_API="$key"

huggingface-cli login --token <HFTOKEN>

output_file="$directory/exp/gpt_trial_output/output_llama2_AdvBench_SafeDecoding.out"
error_file="$directory/exp/gpt_trial_output/error_llama2_AdvBench_SafeDecoding.err"

python "$directory/exp/defense.py" \
    --model_name llama2_2x \
    --attacker AdvBench \
    --defender SafeDecoding \
    --GPT_API $key
#python my_script.py
# --disable_GPT_judge > "$output_file" 2> "$error_file" 