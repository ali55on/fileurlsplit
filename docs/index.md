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
