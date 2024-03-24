#!/bin/zsh

# Run the python script
python main.py

if [ $? -eq 0 ]; then
    # Check if there are any changes
    if [[ -n $(git status -s) ]]; then
        # Add changes to Git
        git add .

        # Commit changes
        git commit -m "Automated commit after running Python script"

        # Push changes to GitHub
        git push origin master
    else
        echo "No changes detected. Nothing to commit."
    fi
else
    echo "Python script execution failed. Changes not committed to Git."
fi