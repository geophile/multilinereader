`MultiLineReader`
=================

`input()` and the `readline` module support single-line input. I.e., each time the dude typing on the
keyboard presses Enter, that ends the line of input, which is then added to the history maintained by
readline. It would be nice to type a \ at the end of the line, and continue typing a command on 
the next line(as happens on bash), but that doesn't work.

`input()` and `readline` can, however, deal with history items that happen to be multi-line due to 
embedded `\n` characters.
The `MultiLineReader` class takes advantage of this. If a line of input is terminated by a 
continuation string (e.g. \),
then an additional line of input is requested. This continues until a line is provided 
that does not end with
the continuation string. `MultiLineReader.input` reads lines until it detects one not 
terminated by a continuation
string, and returns those lines concatenated into a string 
(removing the \ and `\n` terminating each non-terminal line).

History items are correctly maintained, replacing multiple continued lines, 
with the one joined-together line.
When one of these multi-line history items is edited, it shows up to the keyboard 
dude as it was typed in
originally: multiple lines, with all but the last ending in the continuation string.

Usage
-----

Create a `MultiLineReader` using the constructor. Specify the location
of your application's history file, if you want the history of input
lines to survive process boundaries. E.g.

    reader = MultiLineReader(history_file='/home/marcel/.app_history')
    
This creates a multi-line reader, using \ as the continuation string.
If you want a different continuation string, specify a
value for the `continuation` argument.
    
To read lines from the console use `MultiLineReader.input()` instead of 
Python's `input()` function. (`MultiLineReader.input` wraps `input()`). E.g.

    line = reader.input('> ', '+ ')

This reads one or more lines from `stdin`. Lines that are to be 
continued must end with the continuation string (\ by default). 
`> ` is the prompt for the first line of input. `+ ` is used for
continuation lines.

Call `MultiLineReader.close()` when you are done with input. This will
record the history file on disk.

Integration with the `readline` module
---------------------------------------

You can configure `readline` as you ordinarily do. But you should not
call `readline.read_history_file`, `readline.write_history_file`, or 
any functions that modify history items, as these will interfere with
the operation of `MultiLineReader`.

main()
------

The `main()` function included solicits input, and then when input is complete, prints
the lines returned by `input()` and the history. The lines show multilines concatenated together,
while the history lines show the line breaks and cotinuations. 