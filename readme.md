# Alphanumeric Markdown Footnote

A Sublime Text 3 plugin.

Similar to [MarkdownFootnotes](https://github.com/classicist/MarkdownFootnotes), having these shared features:

- Adds a footnote label to the cursor position and a corresponding footnote entry to the bottom of the file.
- Automatically handles footnote numbers, keeping them consecutive, like Microsoft Word.
- Automatically places cursor in the footnote entry so you can just start typing away at your note.

It differs from MarkdownFootnotes by:

- handling non-integer footnote ids
- ignoring your currently selected text when creating the footnote
- not bothering to validate all of your footnotes
- when footnote ids end with a number, use that prefix for the new footnote, but adjust all the numbers to line up
- less code
- tests

## Example

```
This is a test paragraph

And here is another[^chapter1-1]

[^chapter1-1]: Totally a footnote
```

With the cursor at the end of the first line, hitting the shortcut produces this:

```
This is a test paragraph[^chapter1-1]

And here is another[^chapter1-2]

[^chapter1-1]: 

[^chapter1-2]: Totally a footnote
```

with the cursor on the footnote line immediately after `[^chapter1-1]: `.

## Keybinding

- ctrl+f: Insert Footnote (OS X)
- ctrl+alt+super+f: Insert Footnote (Linux, Windows)

## License

[WTFPL](http://wtfpl2.com/)
