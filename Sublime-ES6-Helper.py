import sublime, sublime_plugin, re

class ConditionExpressionToIfCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        mark = self.view.sel()[0]
        line = self.view.line(mark.a)
        content = self.view.substr(line)
        conditionGroups = re.match(r'^(\s*)(\S.*\S)(\s*)$', content)
        indentations = conditionGroups.group(1)
        code = conditionGroups.group(2)
        codeGroups = re.match(r'(\S.*\S)\s*&&\s*(\S.*\S)', code);
        condition = codeGroups.group(1)
        result = codeGroups.group(2)
        self.view.replace(edit, line, indentations + 'if (' + condition + ') {\n' + indentations + '    ' + result + '\n' + indentations + '}')

class VarToConstCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lines = self.view.lines(self.view.sel()[0])
        results = ''
        for line in lines:
            content = self.view.substr(line)
            groups = re.match(r'^(\s*)(var\s|let\s)?(.*)\s=\s(.*)(,|;)$', content)
            if groups:
                indentations = groups.group(1)
                varDeclaration = groups.group(2)
                varName = groups.group(3)
                varValue = groups.group(4)
                seperator = groups.group(5)
                indentations = indentations if varDeclaration else indentations[:-4]
                results += indentations + 'const ' + varName + ' = ' + varValue + ';\n'

        self.view.erase(edit, sublime.Region(lines[0].begin(), self.view.full_line(lines[len(lines) - 1]).end()))
        self.view.insert(edit, lines[0].begin(), results)

