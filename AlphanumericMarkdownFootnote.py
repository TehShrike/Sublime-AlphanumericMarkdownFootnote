import sublime
import sublime_plugin

from .FootnoteFunctions import insert_footnote, find_enclosing_footnote_id, find_footnote_marker_position

class InsertAlphanumericMarkdownFootnoteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		whole_view_region = sublime.Region(0, self.view.size())
		buffer_contents = self.view.substr(whole_view_region)

		selection = self.view.sel()
		cursor_position = selection[0].b

		enclosing_footnote_id = find_enclosing_footnote_id(buffer_contents, cursor_position)

		if (enclosing_footnote_id is None):
			new_contents = insert_footnote(buffer_contents, cursor_position)

			self.view.erase(edit, whole_view_region)
			self.view.insert(edit, 0, new_contents['body'])

			new_cursor_position = new_contents['cursor']
			set_cursor_position(self, selection, new_cursor_position)

class MoveToFootnoteMarkerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		whole_view_region = sublime.Region(0, self.view.size())
		buffer_contents = self.view.substr(whole_view_region)

		selection = self.view.sel()
		cursor_position = selection[0].b

		enclosing_footnote_id = find_enclosing_footnote_id(buffer_contents, cursor_position)

		if (enclosing_footnote_id is not None):
			footnote_marker_position = find_footnote_marker_position(buffer_contents, enclosing_footnote_id)

			if (footnote_marker_position is not None):
				set_cursor_position(self, selection, footnote_marker_position)

def set_cursor_position(self, selection, position):
	new_cursor_region = sublime.Region(position, position)

	selection.clear()
	selection.add(new_cursor_region)
	self.view.show(new_cursor_region)
