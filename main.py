from blessed import Terminal
import os
import subprocess
import configparser

term = Terminal()

currentPath = os.getcwd()
shellScriptPath = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "result.txt")

currentPathCoordinates = (0, 0)
inputCoordinates = (0, 1)
fileCoordinates = (0, 3)

KEY_DELETE = 263
KEY_TAB = 512
KEY_ENTER = 343

config = {
    "showHiddenFiles": False,
    "display": "grid",
    "jumpSingleNestedDirectories": True,
    "autoJumpOnPathHit": False
}

# clears the terminal


def run():
    print(term.home() + term.clear())
    end = False

    while not end:
        currentPath = os.getcwd()
        with term.location(currentPathCoordinates[0], currentPathCoordinates[1]):
            print(term.clear_eol() + term.bright_blue(currentPath))

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
                            os.chdir(os.path.join(
                                currentPath, autoComplete[0]))
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

    changeParentDirectory(currentPath)


def printFiles(path, tmpPath):
    directory = [item for item in os.listdir(path) if (tmpPath in item)]
    if config["showHiddenFiles"] is False and not tmpPath.startswith('.'):
        directory = [item for item in directory if not (item.startswith('.'))]

    folders = [f for f in directory if os.path.isdir(os.path.join(path, f))]
    files = [f for f in directory if (f not in folders)]

    longest_path = 0
    if len(directory) != 0:
        longest_path = len(max(directory, key=len)) + 2

    with term.location(fileCoordinates[0], fileCoordinates[1]):
        print(term.clear_eos(), end="")

        if config["display"] == "grid":
            line = ""
            for folder in folders:
                paddedString = folder + (" " * (longest_path - len(folder)))
                if len(line + paddedString) > term.width:
                    print(term.bold_green(line))
                    line = paddedString
                else:
                    line += paddedString
            
            tmpLineBuffer = len(line)
            if tmpLineBuffer > 0:
                print(term.bold_green(line), end="")
                line = ""

            for fileItem in files:
                paddedString = fileItem + (" " * (longest_path - len(fileItem)))
                if len(line + paddedString) + tmpLineBuffer > term.width:
                    print(term.black(line))
                    line = paddedString
                    tmpLineBuffer = 0
                else:
                    line += paddedString
            if len(line) > 0:
                print(term.black(line))

    if len(folders) == 1:
        return (folders[0], "directory")
    if len(files) == 1 and len(folders) == 0:
        return (files[0], "file")

    return None


def confirmExit(path):
    with term.location(inputCoordinates[0], inputCoordinates[1]):
        print(term.clear_eol(
        ) + term.bold_bright_white_on_red(term.center("exit in: " + path + "   [ENTER]")))
        with term.cbreak():
            if term.inkey().code == KEY_ENTER:
                return True
    return False


def changeParentDirectory(path):
    print(term.home() + term.clear())
    term.close()
    with open(shellScriptPath, "w") as f:
        string = path + "\n"
        f.write(string)


def checkConfig():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def configBashrc():
    pass


if __name__ == "__main__":
    # if not checkConfig():
    #     configBashrc()
    run()
