from FootnoteFunctions import insert_footnote

def assert_equal(expected, actual):
	if expected != actual:
		raise AssertionError('Expected: "' + str(expected) + '"\nbut got: "' + str(actual) + '"')

test_string = r"""
what's going on then[^ch1-1]

tell me all[^chb2] about it[^chc3]

[^ch1-1]: thingy

	stuff

   yeah

[^chb2]: meh?

	muh

wat

[^chc3]: whatever

"""

def output(result):
	body = result['body']
	cursor = result['cursor']

	print(body[:cursor] + 'CURSOR' + body[cursor:])

# output(insert_footnote(test_string, 34))
# output(insert_footnote(test_string, 54))

# output(insert_footnote('what do you mean', 4))

# output(insert_footnote(test_string, 7))

assert_equal(insert_footnote('what do you mean', 4)['body'], r"""what[^1] do you mean

[^1]: 

""")

assert_equal(insert_footnote(test_string, 7)['body'], r"""
what's[^ch1-1] going on then[^ch1-2]

tell me all[^chb3] about it[^chc4]

[^ch1-1]: 

[^ch1-2]: thingy

	stuff

   yeah

[^chb3]: meh?

	muh

wat

[^chc4]: whatever

""")

assert_equal(insert_footnote(test_string, 34)['body'], r"""
what's going on then[^ch1-1]

tel[^ch1-2]l me all[^chb3] about it[^chc4]

[^ch1-1]: thingy

	stuff

   yeah

[^ch1-2]: 

[^chb3]: meh?

	muh

wat

[^chc4]: whatever

""")

assert_equal(insert_footnote(test_string, 54)['body'], r"""
what's going on then[^ch1-1]

tell me all[^chb2] abou[^chb3]t it[^chc4]

[^ch1-1]: thingy

	stuff

   yeah

[^chb2]: meh?

	muh

[^chb3]: 

wat

[^chc4]: whatever

""")

test_string_2 = r"""
- find the previous footnote in the body
- pick a new number: the previous footnote's number, plus one
- find all footnotes greater to or equal than that number, and increment them in both the body and where the footnote contents are identified
- find the previous footnote's content block[^ch1-1]
- create a new footnote identifier where the cursor is[^ch1-2]
- create a new footnote contents block immediately after that content block
- move the cursor to the new footnote contents block

[^ch1-1]: yeah, footnote here


[^ch1-2]: aw yeah


"""

# output(insert_footnote(test_string_2, 11))

assert_equal(insert_footnote(test_string_2, 11)['body'], r"""
- find the[^ch1-1] previous footnote in the body
- pick a new number: the previous footnote's number, plus one
- find all footnotes greater to or equal than that number, and increment them in both the body and where the footnote contents are identified
- find the previous footnote's content block[^ch1-2]
- create a new footnote identifier where the cursor is[^ch1-3]
- create a new footnote contents block immediately after that content block
- move the cursor to the new footnote contents block

[^ch1-1]: 

[^ch1-2]: yeah, footnote here


[^ch1-3]: aw yeah


""")

print('Passing!')
