# FileUrlSplit

[https://wbin01.github.io/fileurlsplit](https://wbin01.github.io/fileurlsplit)

A python ***class*** that handles file URL splits such as path, name and
extension.

No dependencies, just use the standard library.

```Python
>>> file_url = FileUrlSplit(file_url='/home/user/photo.png')
>>>
>>> file_url.url
'/home/user/photo.png'
>>>
>>> file_url.path
'/home/user/'
>>>
>>> file_url.name
'photo'
>>>
>>> file_url.filename
'photo.png'
>>>
>>> file_url.extension
'.png'
>>>
>>> print(f"'{file_url.url}', '{file_url.filename}', '{file_url.extension}'")
'/home/user/photo.png', 'photo.png', '.png'
>>>
>>> file_url.extension = 'jpg'
>>>
>>> print(f"'{file_url.url}', '{file_url.filename}', '{file_url.extension}'")
'/home/user/photo.jpg', 'photo.jpg', '.jpg'
```
Useful for choosing names for multiple files without changing their extensions.
```Python
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
