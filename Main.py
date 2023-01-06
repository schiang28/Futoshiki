from Ui import Terminal, Gui
from sys import argv


# Display menu option to the terminal
# The user should press g or t to choose between the GUI and terminal
def usage():
    print(
        f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal"""
    )
    quit()


if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    elif argv[1] == "t":
        ui = Terminal()
    elif argv[1] == "g":
        ui = Gui()
    else:
        usage()

    ui.run()
