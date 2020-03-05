"""input() and the readline module support single-line input. I.e., each time the dude typing on the
keyboard resses Enter, that ends the line of input, which is then added to the history maintained by
readline. It would be nice to type a \\ at the end of the line, and continue typing a command on the next line
(as happens on bash), but that doesn't work.

input() and readline can, however, deal with history items that happen to be multi-line due to embedded \n.
MultiLineReader takes advantage of this. If a line of input is terminated by a continuation string (e.g. \\),
then an additional line of input is requested. This continues until a line is provided that does not end with
the continuation string. MultiLineReader.input reads lines until it detects one not terminated by a continuation
string, and returns those lines concatenated into a string (removing the \\ and \n terminating each non-terminal line).

History items are correctly maintained, replacing multiple continued lines, with the one joined-together line.
When one of these multi-line history items is edited, it shows up to the keyboard dude as it was typed in
originally: multiple lines, with all but the last ending in the continuation string.
"""

import readline


class MultiLineReader:

    def __init__(self, continuation='\\'):
        """continuation is the string which is used to denote that an input line is going to be
        continued. It is typically \\, which is the default."""
        self.continuation = continuation

    def input(self, prompt, continuation_prompt):
        """Get input from the user, similar to the Python input() function. The prompt is printed
        before the first line of input. If the input line ends with the continuation string,
        then additional lines are requested, using the continuation prompt."""
        lines = []
        while True:
            line = input(prompt if len(lines) == 0 else continuation_prompt)
            if len(line) > 0:
                readline.remove_history_item(readline.get_current_history_length() - 1)
                # If line was recalled from history, then convert to its original multiline form.
                from_history = self._multiline(line)
                if from_history is None:
                    # Wasn't from history
                    lines.append(line)
                else:
                    lines = from_history
                    line = lines[-1]
                if not line.endswith(self.continuation):
                    break
        # Store history as a single line with continuations and line breaks.
        readline.add_history('\n'.join(lines))
        # Return a single string without continuations and line breaks.
        lines[-1] += self.continuation
        return ''.join([line[:-len(self.continuation)] for line in lines])

    # A line recalled from history is a single string, constructed by joining together the individual lines
    # with \n. Return the original multi-line form. Return None if the input was not a joined-together line
    # from history.
    def _multiline(self, line):
        lines = []
        join_pattern = self.continuation + '\n'
        position = 0
        start = 0
        while position >= 0:
            position = line.find(join_pattern, start)
            if position >= 0:
                lines.append(line[start:(position + len(self.continuation))])
                start = position + len(join_pattern)  # For next iteration
            else:
                lines.append(line[start:])
        return lines if start > 0 else None


def main():
    m = MultiLineReader()
    multilines = []
    try:
        while True:
            multilines.append(m.input('> ', '+ '))
    except EOFError:
        pass
    print('MULTILINES:')
    for x in multilines:
        print(x)
    print('HISTORY:')
    for i in range(readline.get_current_history_length()):
        item = readline.get_history_item(i + 1)  # 1-based
        print(item)


if __name__ == '__main__':
    main()
