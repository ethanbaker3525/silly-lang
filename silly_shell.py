import curses
from curses import wrapper
from time import sleep

from silly_interpreter import interp_code

# this is kinda a mess, you need to make some functions that can actually be used and maintained easily
# TODO write a function that prints out a str and handles the line and cursor movement
# TODO adapt current functions to handle offsets (y offset is the previous commands, x offset is the prompt)

class Shell():

    START_MSG = "silly shell :3"
    PROMPT = ""

    def __init__(self):

        self.win = curses.initscr()
        self.win.nodelay(True)
        self.win.keypad(True)
        self.ylim = (0, curses.LINES)
        self.xlim = (0, curses.COLS)
        self.x = 0
        self.y = 0
        self.exit_msg = ""

        self.commands = []

        curses.noecho()

    def run(self):
        running = True
        cmds = [""]
        cid = 0
        self.win.addstr(0, 0, self.__class__.START_MSG)
        while running:
            try:
                self.win.move(self.y, 0) # go to start of line for clearing (next function clears from cursor to eol)
                self.win.clrtoeol() # clear line before writing
                #self.win.addstr(self.y, 0, self.__class__.PROMPT)
                self.win.addstr(self.y, 0, cmds[cid]) # write the current command
                self.win.move(self.y, self.x) # update the cursor to the correct position (self.y and self.x are the master values)
                c = self.win.getch() # get char
                # running a command
                if c == curses.KEY_ENTER or c == 10 or c == 13:
                    s = interp_code(cmds[cid], print_result=False)
                    self.win.addstr(self.y+1, 0, s)
                    self.commands.append(cmds[cid])
                    cmds = list(self.commands)
                    cid = len(cmds)
                    cmds.append("")
                    self.move(self.y+2, 0)
                # removing characters
                elif c == curses.KEY_BACKSPACE:
                    cmds[cid] = cmds[cid][:self.x-1] + cmds[cid][self.x:]
                    self.move(self.y, self.x-1)
                    self.win.delch(self.y, self.x)
                elif c == curses.KEY_DC:
                    cmds[cid] = cmds[cid][:self.x] + cmds[cid][self.x+1:]
                    self.win.delch(self.y, self.x)
                # arrow key functionality
                elif c == curses.KEY_LEFT:
                    self.move(self.y, self.x-1)
                elif c == curses.KEY_RIGHT:
                    self.move(self.y, self.x+1)
                elif c == curses.KEY_UP:
                    if cid > 0:
                        cid -= 1
                elif c == curses.KEY_DOWN:
                    if cid < len(cmds) - 1:
                        cid += 1
                # other characters
                elif c >= 0:
                    cmds[cid] = cmds[cid][:self.x] + chr(c) + cmds[cid][self.x:]
                    self.move(self.y, self.x+1)

                else:
                    #self.win.addch(c)
                    pass

            except KeyboardInterrupt as e:
                self.exit_msg = "keyboard interupt"
                running = False
            except Exception as e:
                self.exit_msg = str(e)
                running = False

    
    def exit(self):
        self.win.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def move(self, y, x):
        if y >= self.ylim[0] and y <= self.ylim[1]:
            self.y = y
        if x >= self.xlim[0] and x <= self.xlim[1]:
            self.x = x

    def read_command(self):
        pass

if __name__ == "__main__":
    shell = Shell()
    shell.run()
    shell.exit()
    print(shell.exit_msg)