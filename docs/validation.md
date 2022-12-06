# Validation details

This works with an ***string***. Use `os.path.isfile()` to validate
an existing URL in the OS.

## Existing URLs vs dummy URLs
Not all error checks are performed on object instantiation.
This is because it is common to pass a valid URL, where the path, name and
extension were taken from a real OS. The purpose of this approach is to avoid
unnecessary checks. It's a bit faster and can be really significant when
working with very large batches of files.

When an object is instantiated, the only check performed is whether the URL
passed in is an absolute URL. The other validations such as character and name
error are performed using the ***setter***, that is, when we set the value of a
property (setter - setattr)

If the URL wasn't taken from a real context, and for that reason you want all
the error checking to be performed, then instantiate an empty object
(this will automatically create a root URL like `'/'`) and use the property
setter `url`. Example:

Checks only if the URL is absolute: (Use for existing URLs)
```Python
>>> file_url = FileUrlSplit(file_url='/home/user/book.pdf')
>>>
```

Setter run all error checks: (Use for dummy URLs)
```Python
>>> file_url = FileUrlSplit()
>>> file_url.url = '/my/dummy/URL.test'
>>>
```
## Setters behavior
Updating a property will affect related properties.
```Python
>>> print(f"'{file_url.url}', '{file_url.filename}', '{file_url.extension}'")
'/home/user/photo.png', 'photo.png', '.png'
>>>
>>> file_url.extension = 'jpg'
>>>
>>> print(f"'{file_url.url}', '{file_url.filename}', '{file_url.extension}'")
'/home/user/photo.jpg', 'photo.jpg', '.jpg'
```

## Extensions are part of the name
When we use the `name` property to remove the file name. If the file has an extension,
then the extension is recognized as the filename.
This is exactly what happens when we rename a file by removing
its name.
```Python
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

## There is always the path
There is no URL without path. There will always be a path.
```Python
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
