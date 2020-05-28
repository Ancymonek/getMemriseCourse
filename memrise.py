from lxml import html
import os.path
import requests
from bs4 import BeautifulSoup


# Find the ID of your course and use the function get_course(course_id).
# The ID can be found in the URL of the course page, for example:
#      http://www.memrise.com/course/169732/ttmik-talk-to-me-in-korean-level-3/
#      where 169732 is the ID of this course.
# Example use:
# get_course(47179,'Talk To Me In Korean 1')
# get_course(85652,'Talk To Me In Korean 2',True)
# get_course(169732)

def get_course(course_id, filename=False, collect=False, word_separator='#', line_separator=''):
    # Set collect True if all levels can be merged in a single list.
    # Optionally set a fileName, default is the course ID.

    course_id = str(course_id)
    if not filename:
        filename = course_id

    # Start a request session
    with requests.Session() as s:
        # get HTML source of course main page
        rc = s.get('http://www.memrise.com/course/' + course_id)

        # Parse it for python and extract each level URL
        pool = BeautifulSoup(rc.content, features="lxml")
        level_urls = []
        for tag in pool.findAll(attrs={'class': 'level clearfix'}):
            level_urls.append(tag['href'])

        course = u''  # Save source in unicode text string

        for url in level_urls:
            rc = s.get('http://www.memrise.com' + url)
            pool = BeautifulSoup(rc.content, features="lxml")
            for tag in pool.findAll('div',
                                    attrs={'class': 'col_a col text'}):  # Search for parent divs that contain words
                word = html.fromstring(
                    tag.next.next).text  # Take word from child divs and parse any html escape characters
                translation = html.fromstring(
                    tag.findNextSibling().next.next).text  # Take the translation, which is a sibling div and parse
                # any html escape characters
                course = course + word + word_separator + translation + u'\n'  # Paste word into our course
            if not collect:
                course = course + line_separator  # End of level, do we want an empty line to seperate levels?

        course = course[:-2]  # cut last empty line
        if not collect:
            course = course[:-2]  # cut another remaining empty line if levels were seperated

        # Now wrap it up and save in an utf-8 encoded text file.
        output_file = os.path.join('{}.csv'.format(filename))
        with open(output_file, 'wb') as f:
            f.write(course.encode('utf8'))

        print("Data saved in {}".format(filename))
