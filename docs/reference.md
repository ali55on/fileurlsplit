# Class Reference

## FileUrlSplit
(class)

Definition:
```
FileUrlSplit(file_url: str = None)
```

Properties:

* [extension](#extension): str
* [filename](#filename): str
* [name](#name): str
* [path](#path): str
* [url](#url): str

A python class that handles file URL splits such as path, name and extension.

`file_url`: It is an optional parameter of type `str`.
It is the only parameter of this `class`, and takes as an argument, a
string that represents the URL of a file.

```Python
>>> file_url = FileUrlSplit(file_url='file:///home/user/book.pdf')
>>> print(file_url)
FileUrlSplit("/home/user/book.pdf")
>>>
>>> file_url = FileUrlSplit(file_url='/home/user/book.pdf')
>>> file_url.url
'/home/user/book.pdf'
>>>
```

If the URL contains backslashes ` \ `, it must be escaped or passed as a raw
string, like: `r'c:\path'`, `'c:\\path'`
```Python
>>> file_url = FileUrlSplit(file_url=r'C:\Windows\user\book.pdf')
>>> file_url.url
'/Windows/user/book.pdf'
>>>
>>> file_url = FileUrlSplit(file_url='C:\\Windows\\user\\book.pdf')
>>> file_url.url
'/Windows/user/book.pdf'
>>>
```
Also accepts string as a *UrlEncode*.

```Python
>>> file_url = FileUrlSplit('file%3A%2F%2F%2Fhome%2Fuser%2Fbook.pdf')
>>> file_url.url
'/home/user/book.pdf'
>>>
```

### extension
(Property) `FileUrlSplit.extension -> str`

Get file extension only, without the name and path.

```Python
>>> file_url = FileUrlSplit(file_url='/home/user/photo.png')
>>> file_url.extension
'.png'
```

### filename
(Property) `FileUrlSplit.filename -> str`

Filename with the extension but without the path.

```Python
>>> file_url = FileUrlSplit(file_url='/home/user/photo.png')
>>> file_url.filename
'photo.png'
```

### name
(Property) `FileUrlSplit.name -> str`

Only the file name without the extension and without the path.
```Python
>>> file_url = FileUrlSplit(file_url='/home/user/photo.png')
>>> file_url.name
'photo'
```

### path
(Property) `FileUrlSplit.path -> str`

Get file path only, without the file name and extension.
Always ends with a slash '/' to maintain consistency.

```Python
>>> file_url = FileUrlSplit(file_url='/home/user/photo.png')
>>> file_url.path
'/home/user/'
```

### url
(Property) `FileUrlSplit.ulr -> str`

Cleaned of prefixes and UrlEncode.
URL without the file prefix, such as "file://".

```Python
>>> file_url = FileUrlSplit(file_url='/home/user/photo.png')
>>> file_url.url
'/home/user/photo.png'
```
