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
