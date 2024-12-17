#!/bin/bash

# Define arrays for model names and lora dropout values
model_names=("dolphin" "llama2" "vicuna" "guanaco" "falcon")
lora_dropout=(0.05 0.1 0 0.05 0)

# Loop over each model and use the corresponding lora_dropout value
for i in "${!model_names[@]}"; do
    model="${model_names[$i]}"
    dropout="${lora_dropout[$i]}"
    
    echo "Running finetune.py with model_name=$model and lora_dropout=$dropout"
    python finetune.py --model_name "$model" --lora_dropout "$dropout" --GPT_API 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
done
