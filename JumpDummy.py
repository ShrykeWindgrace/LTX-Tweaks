import sublime_plugin


class JumpToDummyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        start_point = self.view.sel()[0].begin()  # starting position for our search
        where = self.view.find('<\+\+>', start_pt=start_point)  # found next occurrence of our dummy
        if where.begin() > 0:
            cont = self.view.substr(where)  # get the string containing the dummy
            cont = cont.replace("<++>", "")  # delete the dummy in that string
            self.view.replace(edit, where, cont)  # replace that string in the original text
            self.view.sel().clear()  # clear selection and jump to the place where the dummy used to be
            self.view.sel().add(where.begin())  # the only difficult point here - what to do with multiple selections


class UpgradeBracketsCommand(sublime_plugin.TextCommand):
    """docstring for UpgradeBracketsCommand"""
    brackets = [('(', ')'), ('[', ']'), ('ltext', 'rtext')]

    def run(self, edit):
        region = self.view.sel()[0]   # current cursor position (assuming no text selection)
        global_string = self.view.line(region)
        l, brl = find_left_bracket(global_string[:region.begin()])
        r, brr = find_left_bracket(global_string[region.end():])
        if (l > 0) and (r > 0) and (brl == brr):
            self.view.insert(edit, l, " \\left ")
            self.view.insert(edit, r, " \\right ")

    def find_right_bracket(s):
        global brackets
        i = 0
        right_brackets = [pairs[1] for pairs in brackets]
        while i < len(s):
            for br in right_brackets:
                if s[i:].startswith(br):
                    return (i, br)
            i += 1
        return -1, False

    def find_left_bracket(s):
        global brackets
        i = len(s)
        left_brackets = [pairs[0] for pairs in brackets]
        while i > -1:
            for br in left_brackets:
                if s[:i].endswith(br):
                    return (i - len(br), br)
            i -= 1
        return -1, False
