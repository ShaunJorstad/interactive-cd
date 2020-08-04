# interactive-cd
interactive CD command to make changing directories more intuitive

# install 
clone repo locally, edit variables in `main.sh` to ponit to the correct files 

# use 
run the program with `source {path/to/main/sh}` 

Typing in the program will filter the current files and directories in the Working Directory. 
When there is a single match hit `tab` to autocomplete the rest of the filepath, navigate to that directory, and reset the prompt. 

Typing `..` into the prompt will navigate up a directory

To exit the program hit enter, and confirm the prompt by hitting enter again. 

Exiting the program with `ctr-c` will not navigate to the chosen directory

# Future features 
- navigating to a directory that only contains a single directory will automatically move to the nested directory as well. Moving up will always navigate individually.
- `Tab` and `Shift+Tab` when there are multiple matched files and directories will enter a selection mode. Hitting enter on any option will prompt the user with a list of programs to open that selection with. Selecting an option will exit the program, navigate the shell to the last working directory, and will open the file or directory with the chosen program. 
- Selection mode could open a preview of the file beneath the list of files and directories