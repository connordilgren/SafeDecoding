#!/bin/bash
#SBATCH --job-name=safe_defense_test         # Job name
#SBATCH --partition=class                   # Partition name
#SBATCH --account=class                     # Account name
#SBATCH --qos=medium                        # QoS level (default, medium, high)
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8                   # Number of CPU cores
#SBATCH --mem=32G                           # Memory allocation (32 GB in this case)
#SBATCH --time=30:00:00                     # Maximum time for job (30 hours)
#SBATCH --output=safe_defense_test_%j.out    # Output file (%j will include the job ID)
#SBATCH --error=safe_defense_test_%j.err     # Error file


module load cuda
# Initialize conda (ensures the conda environment can be activated)
source /fs/classhomes/fall2024/cmsc723/c7230002/SafeDecoding/.venv/bin/activate

python /fs/classhomes/fall2024/cmsc723/c7230002/SafeDecoding/exp/defense.py --model_name llama2 --attacker AdvBench --defender SafeDecoding --disable_GPT_judge
#--GPT_API hiba to add her key
#python my_script.py