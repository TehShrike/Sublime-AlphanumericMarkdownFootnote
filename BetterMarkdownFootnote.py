import sublime
import sublime_plugin

from .FootnoteFunctions import insert_footnote

class InsertBetterMarkdownFootnoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		whole_view_region = sublime.Region(0, self.view.size())
		buffer_contents =  self.view.substr(whole_view_region)

		selection = self.view.sel()
		new_contents = insert_footnote(buffer_contents, selection[0].b)

		self.view.erase(edit, whole_view_region)
		self.view.insert(edit, 0, new_contents['body'])
		
		new_cursor_position = new_contents['cursor']
		new_cursor_region = sublime.Region(new_cursor_position, new_cursor_position)

		selection.clear()
		selection.add(new_cursor_region)
		self.view.show(new_cursor_region)

