#!/bin/bash

scriptPath="/home/jorstad/git/interactive-cd/main.py"
resultPath="/home/jorstad/git/interactive-cd/result.txt"

python $scriptPath

while IFS= read -r line; do
    cd "$line"
done < $resultPath

# cd "/home/jorstad"
