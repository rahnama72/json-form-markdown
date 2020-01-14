def json_book_chapters_form_markdown(book_object):
    """

    Json Book Chapters Creator form Markdown
    **************************

    Introduction
    ============
    In this function we focus on getting some markdown content, specify its heading tags,
    and finally create json file from these tags. **So in short we can say we are making
    json file (or object for saving in DB) from markdown text.**

    Implementation
    ==============
    There are few way to convert markdown objects to json files. We use ``BeautifulSoup4`` and
    ``Moratab`` packages to achieve this. This procedure involves the following steps:
        1. Create HTML string from ``Markdown`` content with ``Moratab``.
        2. Create HTML object with ``BeautifulSoup4``.
        3. Make list of ``<h1>``, ``<h2>`` ,and ``<h3>`` tags in their **original order**.
        4. Make dictionary of chapters in order of tree relation with **Nested Loops**.
        5. Convert python dictionary object to json object.
    The most difficult part of this implementation was in the "Nested Loops" section. Each list
    had to be divided into sub-lists and the biggest <h> tag should have been at the first of this
    list. After that, the process was repeated again for the elements of each sub-list. At the end,
    lists and dictionaries filled recursively and the final dictionary was built.


    .. warning::
        Don't try to change name of lists and dicts in this function! DO NOT FUCK-UP!

    :param book_object: Book object that contain **title**, **content**, and other requirments.
    :return: Dictionary of chapters
    """
    # Create HTML from Markdown content.
    html_string = moratab.render(book_object.content)

    # Create BeautifulSoup html object form HTML string.
    html_object = BeautifulSoup(html_string)

    # Find all <h1>, <h2> ,and <h3> tags.
    h_tags_list = html_object.find_all(re.compile(r'h[1-3]+'))

    # Regular expression pattern for find out text of each tag.
    h1_tag_pattern = re.compile(r'<h1>.*</h1>')
    h1_pattern = re.compile(r'h1')
    h2_tag_pattern = re.compile(r'<h2>.*</h2>')
    h2_pattern = re.compile(r'h2')
    h3_tag_pattern = re.compile(r'<h3>.*</h3>')
    h3_pattern = re.compile(r'h3')

    # Make a list of chapters in their original order.
    # Each item in this list is a dictionary of "tag name":"tag value".
    data = []
    for item in h_tags_list:
        temp_dict = {}
        if h1_tag_pattern.match(str(item)):
            temp_dict['h1'] = item.text
        if h2_tag_pattern.match(str(item)):
            temp_dict['h2'] = item.text
        if h3_tag_pattern.match(str(item)):
            temp_dict['h3'] = item.text
        data.append(temp_dict)

    # Make dictionary of all chapters that contains tree of tags.
    book_chapters = {}
    final_list = []
    for item in reversed(data):
        h1_dict = {}
        for key in item:
            if h1_pattern.match(key):
                h1_list = data[data.index(item):]
                data[data.index(item):] = []
                final_h2_list = []
                for item in reversed(h1_list):
                    for key, value in item.items():
                        if h2_pattern.match(key):
                            h2_list = h1_list[h1_list.index(item):]
                            h1_list[h1_list.index(item):] = []
                            h2_dict = {}
                            h3_list = []
                            if len(h2_list) == 1:
                                h2_dict.update({"title": h2_list[0]})
                                h2_dict.update({"h3s": []})
                            else:
                                for item in reversed(h2_list[1:]):
                                    for key, value in item.items():
                                        if h3_pattern.match(key):
                                            h3_list.append(item)
                                            h2_list[h2_list.index(item):] = []
                                            h3_list.reverse()
                                            h2_dict.update({"title": h2_list[0]})
                                            h2_dict.update({"h3s": h3_list})
                            final_h2_list.append(dict(h2_dict))
                            h2_dict.clear()
                final_h2_list.reverse()
                h1_dict.update(({"title": h1_list[0]}))
                h1_dict.update(({"h2s": final_h2_list}))
                final_list.append(dict(h1_dict))
                h1_dict.clear()
    final_list.reverse()
    book_chapters.update({"title": book_object.title})
    book_chapters.update({"h1s": final_list})

    return book_chapters
