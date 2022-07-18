# FileUrlSplit

https://github.com/w-a-gomes/fileurlsplit

A python class that handles file url splits such as path, name and extension.

It only works with the "string" and does not check if the given URL file exists, nor does it change the name or path of an actual file.

No dependencies, just use the standard library.

#### Definition:

```
FileUrlSplit(file_url: str = None)
``` 

**file_url**: It is an **optional** parameter of type "**str**". 
It is the only parameter of this class, and takes as an argument, a string 
that represents the URL of a file.
```Python console
>>> file_url = FileUrlSplit(file_url='file:///home/user/book.pdf')
>>> print(file_url)
FileUrlSplit("/home/user/book.pdf")
>>>
>>> file_url = FileUrlSplit(file_url='/home/user/book.pdf')
>>> file_url.url
'/home/user/book.pdf'
>>> 
```

If the URL contains backslashes '\\', it must be escaped or passed as a raw 
string, like: r'c:\path', 'c:\\\path'
```Python console
>>> file_url = FileUrlSplit(file_url=r'C:\Windows\user\book.pdf')
>>> file_url.url
'/Windows/user/book.pdf'
>>>
>>> file_url = FileUrlSplit(file_url='C:\\Windows\\user\\book.pdf')
>>> file_url.url
'/Windows/user/book.pdf'
>>> 
```

Also accepts string as a UrlEncode.

```Python console
>>> file_url = FileUrlSplit('file%3A%2F%2F%2Fhome%2Fuser%2Fbook.pdf')
>>> file_url.url
'/home/user/book.pdf'
>>> 
```

#### Validation:
Not all error checks are performed on object instantiation. 
This is because it is common to pass a valid URL, where the path, name and 
extension were taken from a real OS.

The purpose of this approach is to avoid unnecessary checks. It's a bit faster 
and can be really significant when working with very large batches of files.

When an object is instantiated, the only check performed is whether the URL 
passed in is an absolute URL. The other validations such as character and name 
error are performed using the setter, that is, when we set the value of a 
property (setter - setattr)

If the URL wasn't taken from a real context, and for that reason you want all 
the error checking to be performed, then instantiate an empty object 
(this will automatically create a root URL like '/') and use the property 
setter "url". Example:

Checks only if the URL is absolute: (Use for existing url)
```Python console
>>> file_url = FileUrlSplit(file_url='/home/user/book.pdf')
>>>
```

Setter performs all error checks: (Use for dummy URLs)
```Python console
>>> file_url = FileUrlSplit()
>>> file_url.url = '/my/dummy/URL.test'
>>>
```

#### Exception:
- **AbsolutePathError**(*message*):
  Raised when a passed URL doesn't have 
  an absolute path prefix like a slash "/" or "file://".
    - **message** (*str*): A message about the error


- **InvalidCharacterError**(*message, invalid_character_found,
  all_invalid_characters_list*):
  Raised when the string contains a character not allowed.
    - **message** (*str*): A message about the error
    - **invalid_character_found** (*str*): The character that caused the error
    - **all_invalid_characters_list** (*list*): list of all disallowed characters


- **InvalidFilenameError**(*message, all_invalid_filename_list*):
  Raised when the name is reserved for the exclusive use of the operating 
  system.
    - **message** (*str*): A message about the error
    - **all_invalid_filename_list** (*list*): list of all disallowed filenames


- **FilenameTooLongError**(*message*):
  Raised when the filename (with extension) is too long. Usually longer than 
  255 characters.
    - **message** (*str*): A message about the error

#### Properties:
The properties are 'url', 'path', 'name', 'filename' and 'extension'. See 
the examples.

url: Cleaned of prefixes and UrlEncode
```Python console
>>> file_url.url
'/home/user/photo.png'
```
path: Always ends with a slash '/' to maintain consistency
```Python console
>>> file_url.path
'/home/user/'
```
name: Without the extension
```Python console
>>> file_url.name
'photo'
```
filename: With the extension
```Python console
>>> file_url.filename
'photo.png'
```
extension: With the dot
```Python console
>>> file_url.extension
'.png'
```
#### Setters:
Updating a property will affect related properties.
```Python console
>>> print(f"'{file_url.url}', '{file_url.filename}', '{file_url.extension}'")
'/home/user/photo.png', 'photo.png', '.png'
>>>
>>> file_url.extension = 'jpg'
>>>
>>> print(f"'{file_url.url}', '{file_url.filename}', '{file_url.extension}'")
'/home/user/photo.jpg', 'photo.jpg', '.jpg'
```
Useful for choosing names for multiple files without changing their extensions.
```Python console
>>> import os
>>> from fileurlsplit import FileUrlSplit
>>>
>>> files = [
... FileUrlSplit(os.path.abspath(x)) for x in os.listdir() if os.path.isfile(x)
... ]
>>> for num, file_url in enumerate(files):
...     print(f'old "{file_url.url}"')
...
...     file_url.name = f'New name {num}'
...
...     print(f'new "{file_url.url}"')
...     print()
...     
... 
old "/home/user/fileurlsplit/src/__init__.py"
new "/home/user/fileurlsplit/src/New name 0.py"

old "/home/user/fileurlsplit/src/fileurlsplit.py"
new "/home/user/fileurlsplit/src/New name 1.py"
>>>
```

#### Note:
Attention to details. For example, a relevant detail to remember is when we 
use the "name" property to remove the file name. If the file has an extension, 
then the extension is recognized as the filename. 
This is exactly what happens when we rename a file by removing 
its name.
```Python console
>>> file_url = FileUrlSplit(file_url='/home/user/book.pdf')
>>> print(f"'{file_url.filename}', '{file_url.name}', '{file_url.extension}'")
'book.pdf', 'book', '.pdf'
>>> 
>>> file_url.name = None
>>> 
>>> print(f"'{file_url.filename}', '{file_url.name}', '{file_url.extension}'")
'.pdf', '.pdf', ''
>>> 
```
Another detail. There is no URL without path. There will always be a path.
```Python console
>>> file_url = FileUrlSplit('/home/user/text.txt')
>>> file_url.url = ''
>>> 
>>> print(f"'{file_url.url}', '{file_url.path}', '{file_url.filename}'")
'/', '/', ''
>>> 
>>> file_url = FileUrlSplit('/home/user/text.txt')
>>> file_url.path = ''
>>> 
>>> print(f"'{file_url.url}', '{file_url.path}', '{file_url.filename}'")
'/text.txt', '/', 'text.txt'
>>> 
```
## Tests
Download the Git repository and with the terminal enter the 
project directory.

#### doctest
Running the main file without errors is the guarantee that the tests on 
the docstrings passed.
```console
python3 src/fileurlsplit.py
```

#### unittest
Standard library unit tests can be run as follows
```console
python3 -m unittest discover
```

#### coverage
Test coverage can be verified using the "coverage" lib. 
Use pip to install it.
```console
pip3 install --upgrade pip
pip3 install coverage
```
Then run the unit tests using the "coverage" command and then use the 
"report" argument to get the test coverage status.
```console
coverage run -m unittest discover
coverage report -m
```
