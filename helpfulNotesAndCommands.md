how to use python debugger (analagous to GDB):
1. first make an interactive slurm session, running this command will put you into a ne bash shell, though it wont really be obvious, you can just assume it worked, and at any time you can `exit` to leave and get back to your normal session
`srun --time=02:30:00 --mem=32G --gres=gpu:1 --cpus-per-task=8 --qos=medium --account=class --partition=class --job-name=pdb_testing --pty /bin/bash`
2. set up the environment and stuff
```bash
groupdirectory="/fs/class-projects/fall2024/cmsc723/c723g002"
directory="$groupdirectory/SafeDecodingRealAndUpToDate"
module load cuda
source "$directory/.venv/bin/activate"
export HF_HOME="$groupdirectory/.cache"
export OPENAI_API_KEY=<APIKEY>

huggingface-cli login --token <HUGGINGFACETOKEN>
```
3. then run python with pdb
```bash
python -m pdb defense.py \
    --model_name llama2 \
    --attacker AdvBench \
    --defender SafeDecoding \
    --GPT_API <APIKEY>
```
[heres the docs for the debugger commands](https://docs.python.org/3/library/pdb.html#debugger-commands)
4. then set breakpoints if you want with `b filename:linenumber`, or `b functionname` (i think if you `run` withouut breaking, you can `ctrl + c` to break wherever the program currently is)
5. then run the program `run`
6. once the program breaks, you can use `step` `next` `continue`,  etc
7. if you want to evaluate an expression or print something, use `p <expression>`


change group ownership
`chown -vhR c7230010:c723g002 /scratch0/c723g002`

allow anyone in the group to access it
`chmod -R g+rw <directory>`

add a job to queue
`sbatch script_run_trial1.sh`
list all queued jobs
`squeue -A class`
list info about a job
`scontrol show job <jobID>`
kill job
`scancel <jobID>`

list all of <your> past jobs and their exit statuses
`sacct`


hehe hibas OPENAPI key
`export OPENAI_API_KEY=<OPENAPIKEY>`


[i found an extension that lets you watch log files live](https://dev.to/rajeshroyal/how-to-view-server-logs-in-real-time-in-vs-code-26he#:~:text=Add%20the%20below%20code%20to%20your%20vs%20code%20settings.&text=Open%20the%20Command%20Palette%20with,%2F12%2D02%2D2024.)




run the same input throuh all finetuned models, and see the token probabilities that each model produces, for easy comparisions




HAMZA LOOK HERE, this was my post rewquest cuz i didnt wanna figure out postman

```bash
export OPENAI_API_KEY=<OPENAPIKEY>
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
```