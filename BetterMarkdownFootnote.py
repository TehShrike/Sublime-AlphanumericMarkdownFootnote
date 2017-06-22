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
















# import re
# from collections import deque

# any_footnote_id_holder = r'\[\^(.*?)(\d+)\]'

# any_footnote_id_holder_regex = re.compile(any_footnote_id_holder)
# footnote_marker_regex = re.compile(r'[^\n]' + any_footnote_id_holder)


# def insert_footnote(string, position):
# 	start = string[:position]
# 	end = string[position:]

# 	last_footnote = get_last_footnote(start)
# 	new_footnote_number = last_footnote['number'] + 1
# 	new_footnote_id = last_footnote['prefix'] + str(new_footnote_number)
# 	new_footnote_block = footnote_brackets(new_footnote_id)

# 	body_without_new_footnote_contents = increment_footnotes_gte(start, new_footnote_number) \
# 		+ new_footnote_block \
# 		+ increment_footnotes_gte(end, new_footnote_number)

# 	last_footnote_id = last_footnote['prefix'] + str(last_footnote['number'])
# 	new_footnote_contents_position = get_new_footnote_body_position(body_without_new_footnote_contents, last_footnote_id)
# 	footnote_body_starter = new_footnote_block + ': '

# 	is_newline_before = body_without_new_footnote_contents[new_footnote_contents_position - 1] == '\n'
# 	newlines_before = '\n' if is_newline_before else '\n\n'
	
# 	body = body_without_new_footnote_contents[:new_footnote_contents_position] \
# 		+ newlines_before \
# 		+ footnote_body_starter \
# 		+ '\n\n' \
# 		+ body_without_new_footnote_contents[new_footnote_contents_position:]

# 	cursor = new_footnote_contents_position + len(newlines_before + footnote_body_starter)

# 	return { 'body': body, 'cursor': cursor }





# def get_last_footnote(string):
# 	matches = re.finditer(footnote_marker_regex, string)
# 	try:
# 		lastMatch = deque(matches, maxlen=1).pop()
# 	except IndexError:
# 		return { 'prefix': '', 'number': 0 }

# 	groups = lastMatch.groups()
# 	return { 'prefix': groups[0], 'number': int(groups[1]) }


# def increment_footnotes_gte(string, number):
# 	matches = re.finditer(any_footnote_id_holder_regex, string)
# 	match_queue = deque(matches)

# 	while len(match_queue) > 0:
# 		match = match_queue.pop()
# 		groups = match.groups()

# 		footnote_number = int(groups[1])

# 		if footnote_number >= number:
# 			footnote_prefix = groups[0]

# 			new_footnote_number = footnote_number + 1
# 			new_footnote = footnote_brackets(footnote_prefix + str(new_footnote_number))

# 			string = string[:match.start()] + new_footnote + string[match.end():]

# 	return string


# def get_new_footnote_body_position(string, previous_footnote_id):
# 	footnote_body_regex = re.compile(r'\[\^' + re.escape(previous_footnote_id) + r'\]:.*\n(:?(?:[ \t]+.*\n)|\n)+')
# 	match = re.search(footnote_body_regex, string)

# 	if (match == None):
# 		return len(string)
	
# 	return match.end()

# def footnote_brackets(footnote_id):
# 	return '[^' + footnote_id + ']'
