# Exceptions

The `AbsolutePathError` exception can be raised when the `path` and `url`
*setters* are used. The other exceptions can be raised by all *setters*.

#### AbsolutePathError
```
AbsolutePathError(message: str)
    message: str
```

Raised when a passed URL doesn't have
an absolute path prefix like a slash "/" or "file://".

`message`: A message about the error


#### InvalidCharacterError
```
InvalidCharacterError(
        message: str, invalid_character_found: str, all_invalid_characters_list: list)
    message: str
    invalid_character_found: str
    all_invalid_characters_list: list
```

Raised when the string contains a character not allowed.

`message`: A message about the error

`invalid_character_found`: The character that caused the error

`all_invalid_characters_list`: String list of all disallowed characters

#### InvalidFilenameError
```
InvalidFilenameError(message: str, all_invalid_filename_list: list)
    message: str
    all_invalid_filename_list: list
```

Raised when the name is reserved for the exclusive use of the operating system.

`message`: A message about the error

`all_invalid_filename_list`: String list of all disallowed filenames

#### FilenameTooLongError
```
FilenameTooLongError(message: str)
    message: str
```

Raised when the filename (with extension) is too long. Usually longer than 255 characters.

`message`: A message about the error
