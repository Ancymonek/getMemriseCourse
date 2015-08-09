# getMemriseCourse
Grab a Memrise course by ID and save all words of every level into a text file

This works for Python 2.7 and probably also on Python 3 (try update the Print statement, untested) and requires the following packages:

Requests, lxml, BeautifulSoup

Simply use the get_course(id) function in the download_course.py file with a valid Memrise course ID.

example output (requires Korean alphabet):
```
오늘		Today
날씨		Weather
있다		To have / To exist (Plain)
없다		To not have / To not exist (Plain)
친구		Friend
시간		Time
재미		Fun / Interesting
```
