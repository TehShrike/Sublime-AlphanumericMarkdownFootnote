# Alphanumeric Markdown Footnote

A Sublime Text 3 plugin.

When a shortcut is pressed, inserts footnotes where the cursor is.

If the cursor is inside a footnote, you can hit a different shortcut to go back to where the footnote marker is in the document.

Similar to [MarkdownFootnotes](https://github.com/classicist/MarkdownFootnotes), having these shared features:

- Adds a footnote label to the cursor position and a corresponding footnote entry to the bottom of the file.
- Automatically handles footnote numbers, keeping them consecutive, like Microsoft Word.
- Automatically places cursor in the footnote entry so you can just start typing away at your note.

It differs from MarkdownFootnotes by:

- handling non-integer footnote ids
- ignoring your currently selected text when creating the footnote
- not bothering to validate all of your footnotes
- when footnote ids end with a number, use that prefix for the new footnote, but adjust all the numbers to line up
- having a "go back to the footnote marker" shortcut
- less code
- tests

## Example

```bat
This is a test paragraph|

And here is another[^chapter1-1]

[^chapter1-1]: Totally a footnote
```

With the cursor at the end of the first line, hitting the shortcut produces this:

```bat
This is a test paragraph[^chapter1-1]

And here is another[^chapter1-2]

[^chapter1-1]: |

[^chapter1-2]: Totally a footnote
```

with the cursor on the footnote line immediately after `[^chapter1-1]: `.

## Keybinding

### Insert footnote

- ctrl+f (OS X)
- ctrl+alt+f (Linux, Windows)

### Move to footnote

- ctrl+alt+f (OS X)
- ctrl+alt+super+f (Linux, Windows)

## To run tests

```sh
python3 test.py
```

## License

[WTFPL](http://wtfpl2.com/)
