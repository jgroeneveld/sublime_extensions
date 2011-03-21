"""
This underlines every line in which a function is declared or defined.
Basically every line where a entity.name.function scope selector fits.

Jaap Groeneveld
menodev.de
github.com/menodev
"""

import sublime
import sublime_plugin
import re

class UnderlineFunctions(sublime_plugin.EventListener):

    def on_modified(self, view):
        self.draw_underlines(view)

    def on_activated(self, view):
        self.draw_underlines(view)

    def on_load(self, view):
        self.draw_underlines(view)


    def draw_underlines(self, view):
        matching_lines = self.find_all_function_lines(view)
        trimmed_lines = self.trim_lines(view,matching_lines)
        empty_regions = []

        for line in trimmed_lines:
            empty_regions += self.empty_regions_from_line(view, line)

        view.add_regions("lines_with_function_names", empty_regions, 'comment', sublime.DRAW_EMPTY_AS_OVERWRITE)

    def find_all_function_lines(self, view):
        lines = view.find_all('.+') # all lines with content
        matching_lines = []

        for line in lines:
            for point in range(line.begin(), line.end()):
                scope_name = view.scope_name(point)
                if scope_name.find('entity.name.function') >= 0:
                    matching_lines.append(line)
                    break

        return matching_lines

    def trim_lines(self, view, lines):
        trimmed_lines = []
        for line in lines:
            offset = re.search('\S', view.substr(line)).start()
            begin = line.begin() + offset
            end = line.end()
            trimmed_lines.append(sublime.Region(begin, end))

        return trimmed_lines

    def empty_regions_from_line(self, view, line):
        return [sublime.Region(i,i) for i in range(line.begin(), line.end())]
