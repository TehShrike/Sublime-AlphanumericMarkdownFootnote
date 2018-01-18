import re
from collections import deque

BEGINNING = 1
END = 2

any_footnote_id = r'([^\]]*?)(\d+)'
any_footnote_id_holder = r'\[\^' + any_footnote_id + '\]'

any_footnote_id_holder_regex = re.compile(any_footnote_id_holder)
footnote_marker_regex = re.compile(r'[^\n]' + any_footnote_id_holder)


def insert_footnote(string, position):
	start = string[:position]
	end = string[position:]

	footnote_reference = find_reference_footnote(start, end)

	position = footnote_reference['position']

	new_footnote_number = footnote_reference['new_number']
	new_footnote_id = footnote_reference['prefix'] + str(new_footnote_number)
	new_footnote_block = footnote_brackets(new_footnote_id)

	body_without_new_footnote_contents = increment_footnotes_gte(start, new_footnote_number) \
		+ new_footnote_block \
		+ increment_footnotes_gte(end, new_footnote_number)

	if footnote_reference['reference_number_after_incrementing'] is None:
		new_footnote_contents_position = len(body_without_new_footnote_contents)
	else:
		reference_footnote_id = footnote_reference['prefix'] + str(footnote_reference['reference_number_after_incrementing'])
		new_footnote_contents_position = get_new_footnote_body_position(body_without_new_footnote_contents, reference_footnote_id, position)

	footnote_body_starter = new_footnote_block + ': '

	newlines_before = newlines_to_put_before_position(body_without_new_footnote_contents, new_footnote_contents_position)

	body = body_without_new_footnote_contents[:new_footnote_contents_position] \
		+ newlines_before \
		+ footnote_body_starter \
		+ '\n\n' \
		+ body_without_new_footnote_contents[new_footnote_contents_position:]

	cursor = new_footnote_contents_position + len(newlines_before + footnote_body_starter)

	return { 'body': body, 'cursor': cursor }

def newlines_to_put_before_position(string, position):
	already_one = string[position - 1] == '\n'
	already_two = already_one and string[position - 2] == '\n'

	if already_two:
		return ''

	if already_one:
		return '\n'

	return '\n\n'

def find_reference_footnote(first_half, last_half):
	previous_footnote_deetz = get_last_footnote(first_half)

	if previous_footnote_deetz is not None:
		previous_footnote_deetz['new_number'] = previous_footnote_deetz['number'] + 1
		previous_footnote_deetz['reference_number_after_incrementing'] = previous_footnote_deetz['number']
		return previous_footnote_deetz

	next_footnote_deetz = get_first_footnote(last_half)

	if next_footnote_deetz is not None:
		next_footnote_deetz['new_number'] = next_footnote_deetz['number']
		next_footnote_deetz['reference_number_after_incrementing'] = next_footnote_deetz['number'] + 1
		return next_footnote_deetz

	return make_first_footnote_deetz(len(first_half) + len(last_half))


def make_first_footnote_deetz(length):
	return { 'prefix': '', 'number': None, 'new_number': 1, 'position': length, 'reference_number_after_incrementing': None }

def make_footnote_deetz_from_match(match, position):
	groups = match.groups()
	return { 'prefix': groups[0], 'number': int(groups[1]), 'position': position }

def get_last_footnote(string):
	matches = re.finditer(footnote_marker_regex, string)
	try:
		lastMatch = deque(matches, maxlen=1).pop()
	except IndexError:
		return None

	return make_footnote_deetz_from_match(lastMatch, END)

def get_first_footnote(string):
	match = footnote_marker_regex.search(string)
	return None if match is None else make_footnote_deetz_from_match(match, BEGINNING)


def increment_footnotes_gte(string, number):
	matches = re.finditer(any_footnote_id_holder_regex, string)
	match_queue = deque(matches)

	while len(match_queue) > 0:
		match = match_queue.pop()
		groups = match.groups()

		footnote_number = int(groups[1])

		if footnote_number >= number:
			footnote_prefix = groups[0]

			new_footnote_number = footnote_number + 1
			new_footnote = footnote_brackets(footnote_prefix + str(new_footnote_number))

			string = string[:match.start()] + new_footnote + string[match.end():]

	return string

def get_footnote_body_regex_string(identifier_position_regex):
	return r'\[\^' + identifier_position_regex + r'\]:.*\n(?:(?:[ \t]+.*\n)|\n)+'

def get_new_footnote_body_position(string, previous_footnote_id, position):
	footnote_body_regex = re.compile(get_footnote_body_regex_string(re.escape(previous_footnote_id)))
	match = re.search(footnote_body_regex, string)

	if (match is None):
		return len(string)

	return match.end() if position == END else match.start()

def footnote_brackets(footnote_id):
	return '[^' + footnote_id + ']'








def find_enclosing_footnote_id(string, position):
	start = string[:position] + get_first_line(string[position:])
	# print('checking |' + start + '\n\n|')
	regex = get_footnote_body_regex_string(r'([^\]]*?)') + r'$'
	# print(regex)
	match = re.search(regex, start + '\n\n')

	if (match is None):
		return None

	return match.group(1)

	# this_footnote_marker_regex = re.compile(r'[^\n]' + footnote_brackets(footnote_id))

	# marker_matches = re.findall(this_footnote_marker_regex, string)

	# if (len(marker_matches) == 0)
	# 	return None

def find_footnote_marker_position(string, footnote_id):
	regex = re.escape(footnote_brackets(footnote_id))
	match = re.search(regex, string)

	return None if match is None else match.end()


def get_first_line(string):
	return string.split('\n', 1)[0]
