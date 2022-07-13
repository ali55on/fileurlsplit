# FileUrlSplit

https://github.com/w-a-gomes/fileurlsplit

A python class that handles file url divisions, such as path, name and 
extension.

It will not check if the file from the given URL already exists, nor will it 
change the name or path of an actual file. The point is just to split and 
work with the string.

No dependencies, just use the standard library.

#### Definition:

```
FileUrlSplit(file_url: str = None)
```

**file_url** (*str*): It is the only parameter of this class, and receives 
as an argument, a string that represents the url of a file.

If the URL contains backslashes '\\', then it must 
be escaped or passed as a raw string, like: r'c:\path', 'c:\\\path'

```Python console
>>> file_url = FileUrlSplit(file_url='file:///home/user/photo.png')
>>> print(file_url)
FileUrlSplit("/home/user/photo.png")
```

#### Validation:
Not all error checks are performed upon object instantiation. 
This is because it is implied that the URL passed is a valid URL where the 
path, name and extension were taken from a real OS. The goal is to avoid 
processing unnecessary checks. It's a bit faster and can be really significant 
when working with very large batches of files.

When an object is instantiated, the only check performed is whether the URL 
passed is an absolute URL. Character and name validations are performed when 
setting a property (setter - setattr)

If the URL of the object to be instantiated has not been taken from a real 
context, and you want all error checking to occur, then instantiate an empty 
object (will automatically create a root URL like '/'), and use the "url" 
property to configure it. Example:

Checks only if the URL is absolute: (Use for existing url)
```Python console
>>> file_url = FileUrlSplit('/home/user/book.pdf')
>>>
```

Setter performs all error checks: (Use for dummy URLs)
```Python console
>>> file_url = FileUrlSplit()
>>> file_url.url = '/my/dummy/URL.test'
>>>
```
#### Properties:
The properties are 'url', 'path', 'name', 'filename' and 'extension'. See 
the examples.

url
```Python console
>>> file_url.url
'/home/user/photo.png'
```
path
```Python console
>>> file_url.path
'/home/user/'
```
file name without the extension
```Python console
>>> file_url.name
'photo'
```
filename with the extension
```Python console
>>> file_url.filename
'photo.png'
```
extension
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

#### Exception:
(*AbsolutePathError*): Raised when a passed URL doesn't have an absolute path
prefix like a slash "/" or "file://".

(*FileUrlNotAPathError*): Raised when the URL passed ends with a slash "/", as 
if it were a path without the file at the end. 
To pass paths use the "path" property

(*InvalidCharacterError*): Raised when the string contains a character 
not allowed.

(*InvalidFilenameError*): Raised when the name is reserved for the exclusive 
use of the operating system

(*FilenameTooLongError*): Raised when the filename (with extension) is too 
long. Usually longer than 255 characters.

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
