import sublime_plugin

class UpgradeBracketsCommand(sublime_plugin.TextCommand):
    """docstring for UpgradeBracketsCommand"""
    
    brackets = [('(', ')'), ('[', ']'), ('\\lvert', '\\rvert'), ('\{', '\}'), ('\|', '\|')]
    banned_tokens_left = ['\\', '\\left', '\\big'] #  we do not upgrade brackets which were already modified
    banned_tokens_right = ['\\', '\\right', '\\big'] # or are, in fact, start/end of math environment: \[\], \(\)
    
    def run(self, edit):
        def find_right_bracket(s):
            i = 0
            right_brackets = [pairs[1] for pairs in self.brackets]
            while i < len(s):
                for br in right_brackets:
                    if s[i:].startswith(br):
                        # print(br)
                        # print(i)
                        return (i, br)
                i += 1
            return -1, False

        def find_left_bracket(s):
            i = len(s)
            left_brackets = [pairs[0] for pairs in self.brackets]
            while i > -1:
                for br in left_brackets:
                    if s[:i].endswith(br):
                        # print(br)
                        # print(i - len(br))
                        return (i - len(br), br)
                i -= 1
            return -1, False

        def brackets_match(x, y):
            for pairs in self.brackets:
                if (x == pairs[0]) and (y == pairs[1]):
                    print('a match')
                    return True
            return False
        region = self.view.sel()[0]   # current cursor position (assuming no text selection)
        row, col = self.view.rowcol(region.begin())
        global_string = self.view.substr(self.view.line(region))
        l, brl = find_left_bracket(global_string[:col])
        r, brr = find_right_bracket(global_string[col:])
        do_upgrade = False
        if (l >= 0) and (r >= 0) and brackets_match(brl, brr):
            do_upgrade = True
        if do_upgrade:
            for br in banned_tokens_left:
                if global_string[:l].rstrip().endswith(br):
                    do_upgrade = False
            for br in banned_tokens_right:
                if global_string[:r].rstrip().endswith(br):
                    do_upgrade = False
        if do_upgrade:
            global_string = global_string[:l] + '\\left' + global_string[l:col + r] + '\\right'+ global_string[col + r:]
            self.view.replace(edit, self.view.line(region), global_string)
            self.view.sel().clear()  # clear selection and jump to the place where the cursor used to be
            self.view.sel().add(self.view.text_point(row, col + 5))  # the only difficult point here - what to do with multiple selections

