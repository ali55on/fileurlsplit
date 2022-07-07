# FileUrlSplit

https://github.com/w-a-gomes/fileurlsplit

A python class that handles file url divisions, such as path, name and 
extension.

It will not be checked if the file from the passed URL already exists.
The goal is just to split the string.

It also has no dependencies as it only uses the language standard library.

#### Definition:
    FileUrlSplit(file_url: str)

**file_url** (*str*): It is the only parameter of this class, and receives 
as an argument, a string that represents the url of a file.
```Python console
>>> file_url = FileUrlSplit(file_url='file:///home/user/photo.png')
>>> print(file_url)
<FileUrlSplit '/home/user/photo.png'>
```

#### Exception:
The URL must be absolute or an exception will be raised. This means
  that the string must start with a valid path prefix. Example: '/path',
  'c:/path', 'file:///path'.

  If the URL contains backslashes '\\', then it must be escaped or passed
  as a raw string, like: r'C:\path', 'c:\\\path'

#### Properties:
The properties are 'url', 'path', 'name', 'filename' and 'extension'. See 
the examples.

Get url
```Python console
>>> file_url.url
'/home/user/photo.png'
```
Get only file path
```Python console
>>> file_url.path
'/home/user/'
```
Get only file name without the extension
```Python console
>>> file_url.name
'photo'
```
Get filename with the extension
```Python console
>>> file_url.filename
'photo.png'
```
Get file extension
```Python console
>>> file_url.extension
'.png'
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
