from blessed import Terminal
import os
import subprocess

term = Terminal()

currentPath = os.getcwd()

currentPathCoordinates = (0, 0)
inputCoordinates = (0, 1)
fileCoordinates = (0, 3)

KEY_DELETE = 263
KEY_TAB = 512
KEY_ENTER = 343

# clears the terminal


def run():
    print(term.home() + term.clear())
    end = False

    while not end:
        currentPath = os.getcwd()
        with term.location(currentPathCoordinates[0], currentPathCoordinates[1]):
            print(term.clear_eol() + term.red(currentPath))

        tmpPath = ""
        pathHit = False

        printFiles(currentPath, tmpPath)

        autoComplete = None
        while not pathHit:

            # clear the line & print the input path
            with term.location(inputCoordinates[0], inputCoordinates[1]):
                print(term.clear_eol() + "$ " + term.black(tmpPath), end="")

            # move cursor to end of the input path and await input
            with term.location(inputCoordinates[0] + len(tmpPath) + 2, inputCoordinates[1]):
                with term.cbreak():
                    key = term.inkey()
                    if key.code == KEY_DELETE and len(tmpPath) > 0:
                        tmpPath = tmpPath[:-1]
                    elif key.code == KEY_TAB and len(tmpPath) > 0 and autoComplete is not None:
                        print(term.home() + term.clear() + "os cd called")
                        if autoComplete[1] == "directory":
                            os.chdir(os.path.join(currentPath, autoComplete[0]))
                            pathHit = True
                    elif key.code == KEY_TAB:
                        pass
                    elif key.code == KEY_ENTER:
                        if (confirmExit(currentPath)):
                            pathHit = True 
                            end = True
                    elif key.code != KEY_DELETE:
                        tmpPath += str(key)

            if tmpPath == "..":
                os.chdir(os.path.join(currentPath, ".."))
                pathHit = True

            autoComplete = printFiles(currentPath, tmpPath)

    # TODO: the following line does not properly change directories
    subprocess.run(["cd", currentPath])


def printFiles(path, tmpPath):
    directory = [item for item in os.listdir(path) if (tmpPath in item)]

    folders = [f for f in directory if os.path.isdir(os.path.join(path, f))]
    files = [f for f in directory if (f not in folders)]

    with term.location(fileCoordinates[0], fileCoordinates[1]):
        print(term.clear_eos(), end="")

        for folder in folders:
            print(term.bold_green(str(folder)), end="  ")

        for fileItem in files:
            print(term.black(str(fileItem)), end="  ")

    if len(folders) == 1 and len(files) == 0:
        return (folders[0], "directory")
    if len(files) == 1 and len(folders) == 0:
        return (files[0], "file")

    return None

def confirmExit(path): 
    with term.location(inputCoordinates[0], inputCoordinates[1]):
        print(term.clear_eol() + term.bold_bright_white_on_red(term.center("exit in: " + path + "   [ENTER]")))
        with term.cbreak():
            if term.inkey().code == KEY_ENTER:
                return True
    return False

if __name__ == "__main__":
    run()
