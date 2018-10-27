# coding: utf-8

"""

    This module sort the markdown file alphabetically regardless case sensitivity

    Read markdown file as normal file and chop it in four segment header,
    table_content, content, footer by Thematic breaks and sort table_content,
    content. Finally they were wrote in same file.

"""

import re


def read_file(path):
    """
    read_file

    read file from passed path

    read file and return content

    Parameters
    ----------
    path : str
        the path of the file you want to read

    Returns
    -------
    str
        the content of file you want to read
    """

    with open(path, 'r')as reader:
        return reader.read()


def make_four_part(content):
    """
    make_four_part

    split file with Thematic breaks to four part and return it in list

    split file with (- - -\n) to four part

    Parameters
    ----------
    content : str
        whole text of the markdown file

    Returns
    -------
    list
        list of four elements
    """

    return content.split('- - -\n')


def process_table_content(table_content):
    """
    process_table_content

    process table of content and made indented dictionary

    process markdown file with regex and make indented dictionary with group
    and subgroup names respectively as keys ans values

    Parameters
    ----------
    table_content : str
        one part of whole text as table of contents

    Returns
    -------
    dictionary
        intended dictionary which group names as keys and subgroup names
        as value
    """

    table_content_structure = {}  # for storing structure and return it
    for line in table_content.split('\n'):
        # regex match major subject or group name
        if re.match(r'(^-\s\[)', line):
            table_content_structure[line] = []
            group_name = line
        # regex match minor subject or subgroup name
        if re.match(r'(^\s{4}-\s\[)', line):
            table_content_structure[group_name].append(line)
    return table_content_structure


def process_content(content):
    """
    process_content

    process the content part and return the structure

    process the content file with regex and made intended dictionary with
    subgroup names, list of items in each subgroups, and descriptio of each
    one respectively as keys, items part, description part

    Parameters
    ----------
    content : str
        one part of text which is the main part of that

    Returns
    -------
    dictionary
        intended dictionary with subgroups as keys and items, description of
        each subgroups as values
    """

    content_structure = {}  # for storing structure and return it
    for line in content.split('\n'):
        # regex match subgroup names in content part
        if re.match(r'^##\s', line):
            content_structure[line] = {
                'items': []
            }
            subgroup_name = line
        # regex match items of each subgroups
        if re.match(r'^\*\s\[', line):
            content_structure[subgroup_name]['items'].append(line)
        # regex match description of each subgroups
        if re.match(r'^\*\b', line):
            content_structure[subgroup_name]['description'] = line
    return content_structure


def write_file(structure, path):
    """
    write_file

    get structure of file and path of file, and process the structure and wrote
    it as valid markdown style in file

    get structure file which is the dictionary sort the values and keys part
    and wrote with valid markdown style in file

    Parameters
    ----------
    structure : dictionary
        dictionary with four part header, table_content, content, footer
        (It must contain these parts)
    path : str
        path of the file you want to wrote in it

    """

    with open(path, 'w+') as writer:
        writer.write(structure['header'])  # wrote header part with no change
        writer.write('- - -\n')  # separator between main parts
        # sorted and wrote the group names from table of content in file
        # as list markdown
        for group_name in sorted(structure['table_content'],
                                 key=lambda s: s.casefold()):
            writer.write(group_name + '\n')
            # sorted and wrote the subgroup names from table of content in file
            for subgroup in sorted(structure['table_content'][group_name],
                                   key=lambda s: s.casefold()):
                writer.write(subgroup + '\n')
        writer.write('- - -\n')  # separator between main parts
        # sorted and wrote the subgroup names from content part in file
        # as section and list markdown
        for subgroup in sorted(structure['content'],
                               key=lambda s: s.casefold()):
            writer.write(subgroup + '\n')
            # if a subgroup has description it was wrote with Emphasis
            # annotation
            if 'description' in structure['content'][subgroup]:
                writer.write(structure['content'][subgroup]['description'] + '\n')
            # sorted and wrote the items of each subgroup in file
            for item in sorted(structure['content'][subgroup]['items'],
                               key=lambda s: s.casefold()):
                writer.write(item + '\n')
        writer.write('- - -\n')  # separator between main parts
        writer.write(structure['footer'] + '\n')  # wrote footer part with no change
        writer.close()
    return True


def main():
    """
    main

    read file and made file structure and finally wrote in file


    """

    content_file = read_file('README.md')
    structure = {}
    structure['header'], toc, content, structure['footer'] = make_four_part(content_file)
    structure['table_content'] = process_table_content(toc)
    structure['content'] = process_content(content)
    result = write_file(structure, 'README.md')
    if result is not True:
        raise Exception('operation field')

if __name__ == '__main__':
    main()
