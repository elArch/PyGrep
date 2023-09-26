# Task description:
# Implement an analog of GNU/Linux grep with 2 OPTIONS on your choice.
# grep [OPTION]... PATTERN [FILE]...

# Commentary for customer
# This implementation of grep supports - 5 options:
# [-h, --help], [v, --version], [-c, --count], [-n, --line-number], [-i, --ignore-case]

# Written for Python 3.7.5


import sys
import os.path


def show_semantic_error_and_exit():
    print('Usage: grep [OPTION]... PATTERN [FILE]...\n'
          'Try ''grep --help'' for more information.')
    exit()


def show_file_existence_error_and_exit(_file_path):
    if os.path.isdir(_file_path):
        print('grep: {}: Is a directory'.format(_file_path))
    else:
        print('grep: {}: No such file or directory'.format(_file_path))
    exit()


def show_options_error_and_exit(_option):
    print('grep: invalid option -- {}'.format(_option))
    exit()


def parsing_and_checking_arguments(_args):
    """ Parsing and checking arguments """
    # In sys.argv Indexing starts from zero [0, 1, ..., MAX_ARGS], where zero [0] is a name of executable file.
    # Semantics check
    if len(_args) - 1 == 0:
        show_semantic_error_and_exit()

    # For simplify parsing let's skip zero index and shift sys.argv by one [1] unit.
    args_list = _args[1::]

    # Basic Configuration Variables
    _options   = []
    _file_path = []
    _pattern   = ''

    _is_pattern_or_file = True

    # If the PATTERN exists, then it is always located to the left of the FILE

    for index in range(len(args_list)):

        arg = args_list[index]

        if arg and arg[0] == '-':
            _options.append(arg)
            continue
        elif _is_pattern_or_file:
            if os.path.exists(arg) and os.path.isfile(arg):
                _file_path.append(arg)
                _is_pattern_or_file = False
            else:
                _pattern = arg
                _is_pattern_or_file = False
        elif os.path.exists(arg) and os.path.isfile(arg):
            _file_path.append(arg)
        else:
            show_file_existence_error_and_exit(arg)

    # Save parameters to dictionary
    parameters = {
        'OPTIONS': _options,
        'PATTERN': _pattern,
        'FILES'  : _file_path
    }
    return parameters


def show_help_and_exit():
    """" Shows description of all arguments and options """

    print('SYNOPSIS')
    print('\tUsage: grep [OPTION]... PATTERN [FILE...]'
          '\n\tSearch for PATTERN in FILE.'
          '\n\tExample: grep -i ''hello world'' main.c\n')

    print('DESCRIPTION:')
    print('\tgrep searches for PATTERN in FILES.'
          '\n\tBy default, grep prints the matching lines.'
          '\n\tIf no FILE is given the grep terminates.'
          '\n\tIf no PATTERN is given the grep shows file contents'
          '\n\tIf no OPTIONS is given will be used default options'
          '\n\tgrep is sensitive to quotes, please use "" if pattern includes whitespaces.\n')

    print('OPTIONS')
    print('Pattern selection and interpretation:'
          '\n\t-i, --ignore-case\tignore case distinctions\n')

    print('Miscellaneous:'
          '\n\t-v, --version\t\tdisplay version information and exit'
          '\n\t-h, --help\t\tdisplay this help text and exit\n')

    print('Output control:'
          '\n\t-c, --count\t\tprint only a count of selected lines per FILE'
          '\n\t-n, --line-number\tprefix each line of output with the 1-based line number within its input file.')
    exit()


def show_version_and_exit():
    """ Shows Version & Author """

    version = '1.5'
    author = 'Artem Tepanov'
    e_mail = 'a.tepanov@gmail.com'
    github = 'https://github.com/elArch'

    print('grep version {}'
          '\nThis is free software: you are free to change and redistribute it.'
          '\n\tWritten by\t{}'
          '\n\te-mail:\t{}'
          '\n\tgithub:\t{}'
          .format(version, author, e_mail, github))
    exit()


def setup_configuration(parsed_arguments_dictionary):
    """ Applying sent options/keys or using default configuration """

    # List of supported Keys
    _supported_keys = [
        'h', '--help',
        'c', '--count',
        'v', '--version',
        'i', '--ignore-case',
        'n', '--line-number'
    ]

    # List of real Keys
    _parsed_keys = [

    ]

    _options = parsed_arguments_dictionary.get('OPTIONS', None)

    _help        = False
    _count       = False
    _version     = False
    _ignore_case = False
    _line_number = False

    # Apply Default settings if OPTION's is Empty or None
    if not _options or _options is None:
        _ignore_case = False
        _help = _version = False
        _count = _line_number = False
        pass
    else:
        for key in _options:
            # Checking long key
            if key[0:2] == '--':
                if key not in _supported_keys:
                    show_options_error_and_exit(key)
                else:
                    _parsed_keys.append(key)
            # Checking short key or mix of short keys
            elif key[0] == '-':
                for short_key in key[1:]:
                    if short_key not in _supported_keys:
                        show_options_error_and_exit(short_key)
                    else:
                        _parsed_keys.append(short_key)
            else:
                show_options_error_and_exit(key)

    # SetUp configuration after parsing keys
    for key in _parsed_keys:
        if key == 'h' or key == '--help':
            _help = True
        if key == 'c' or key == '--count':
            _count = True
        if key == 'v' or key == '--version':
            _version = True
        if key == 'i' or key == '--ignore-case':
            _ignore_case = True
        if key == 'n' or key == '--line-number':
            _line_number = True

    # Save configuration to dictionary
    settings = {
        'HELP'       : _help,
        'COUNT'      : _count,
        'VERSION'    : _version,
        'IGNORE_CASE': _ignore_case,
        'LINE_NUMBER': _line_number,
    }
    return settings


def processing(settings_dictionary, arguments_dictionary):
    """ All magic is here """
    _help        = settings_dictionary.get('HELP',        False)
    _count       = settings_dictionary.get('COUNT',       False)
    _version     = settings_dictionary.get('VERSION',     False)
    _ignore_case = settings_dictionary.get('IGNORE_CASE', False)
    _line_number = settings_dictionary.get('LINE_NUMBER', False)

    _raw_pattern = arguments_dictionary.get('PATTERN', '')
    _file_path   = arguments_dictionary.get('FILES', None)

    if _help:
        show_help_and_exit()
    if _version:
        show_version_and_exit()

    # Possibility for searching in multiple files is supported by keeping FILE paths in a list() []
    if _file_path is None:
        show_semantic_error_and_exit()

    for path in _file_path:
        with open(path, 'rt') as inf:
            print('\n{}'.format(path))
            match_counter = 0
            lines_counter = 0
            for _raw_line in inf:
                pattern = _raw_pattern
                line = _raw_line
                lines_counter += 1

                # --ignore-case
                if _ignore_case:
                    pattern = _raw_pattern.lower()
                    line = _raw_line.lower()

                # Print strings containing PATTERN and count all matches
                if pattern in line:
                    if _count:
                        match_counter += 1
                        continue
                    elif _line_number:
                        print('{}:'.format(lines_counter) + _raw_line.strip('\n'))
                    else:
                        print(_raw_line.strip('\n'))

            # Print count of matched lines
            if _count:
                print(match_counter)


def grep(_args):
    """ This is core function """
    arguments = parsing_and_checking_arguments(_args)
    settings = setup_configuration(arguments)
    processing(settings, arguments)


# Entry Point
if __name__ == "__main__":
    grep(sys.argv)
    exit()