# This file formats XML files so that they can be parsed without error.

from typing import List


# open file
def read_file(file_name: str):
    __file = open(file_name)
    message_in = __file.read()
    return message_in


# parse command line
def parse_command_line():
    """
       Parses command line

       """

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input filename")
    #parser.add_argument("output", help="output filename")
    args_in = parser.parse_args()
    return args_in


def get_format(index: int, each_line: List[str], line_substring_in: List[str]):
    """
       reformat line so that the data in line is clean xml

       Arguments
       ---------
       index : int
           an index for each line of the original xml
       each_line : List[str]
           line to be reformatted
       line_substring_in:
           inner piece of xml string

       """

    # each_line = each_line.split()
    line_substring2_in = each_line[0]
    line_substring2_in = line_substring2_in[1:]
    message_lines[index] = re.sub(str('>.+?<'), '>' + str(line_substring_in) + '<', str(each_line))
    message_lines[index] = re.sub(str('<.+?>'), '</' + str(line_substring2_in) + '>', str(message_lines[index]))

    # final format
    m_line1 = list(message_lines[index])
    m_line = (m_line1[1:len(m_line1)])
    m_line[2] = ''
    m_line = ''.join(m_line)
    message_lines[index] = m_line
    return m_line


if __name__ == "__main__":

    import re
    import argparse
    from bs4 import BeautifulSoup
    from typing import List
    import glob
    import os

    args = parse_command_line()
    os.mkdir('format_output')


    j = 1
    # for any xml file in the directory
    for file in glob.glob('/home/kristina/PycharmProjects/pythonProject4/' + str(args.infile) + '/*.xml'):

        #path = '/home/kristina/PycharmProjects/pythonProject4/'+args.output
        #os.mkdir(path)

        # read in using beautiful soup which will place a symbol on every ill-formed line
        input_file = open(file, "r")
        contents = input_file.read()
        soup = str(BeautifulSoup(contents, 'xml'))

        # write to xml file to be able to locate errors in input data
        f = open("soup_xml.xml", "w")
        f.write(soup)
        f.close()

        # read xml with errors marked
        args = parse_command_line()
        message = open('soup_xml.xml', "r+")
        message_lines = message.readlines()

        i = 0
        while i < len(message_lines) - 1:

            line = (message_lines[i])

            line_substring = line[line.find('>') + 1:line.rfind('<')]
            line_substring = line_substring.split()

            # if there is an error symbol
            if line.count('&gt;') > 0:

                # fixes no tag
                # get tag
                tag_line = line.split()
                tag_line = tag_line[0]

                # if no tag, label no tag
                if (tag_line.count('=')) > 0:
                    message_lines[i] = re.sub(str('>.+?<'), ' > ' + str(line_substring) + ' < ', str(line))
                    message_lines[i] = re.sub(str('<.+?>'), '<' + 'no_tag' + ' > ', str(message_lines[i]))
                    continue

                line_substring = line_substring[len(line_substring) - 1:len(line_substring)]

                # if there is a units attributes
                if line.count('unit') > 0:

                    # find unit start index
                    line = line.split()
                    indexUnit = message_lines[i].find('unit')

                    # find unit attribute end
                    firstIndex = message_lines[i].find('"', indexUnit)
                    endIndex = message_lines[i].find('"', firstIndex + 1)

                    line_substring2 = line[0]
                    line_substring2 = line_substring2[1:]
                    line_substring2 = list(line_substring2)

                    # find <> indices
                    bracket1 = message_lines[i].find('<')
                    bracket2 = message_lines[i].find('>')

                    # find string inside <>
                    line_substring2 = line_substring2[bracket1:bracket2 - 1]
                    line_substring2 = ''.join(line_substring2)

                    # get unit attribute
                    line_substring3 = message_lines[i]
                    line_substring3 = line_substring3[indexUnit:endIndex + 1]

                    mLine = get_format(i, line, line_substring)

                    # add in unit attribute
                    mLine = mLine.split()
                    mLine[1] = line_substring3 + '>'
                    mLine = ' '.join(mLine)
                    message_lines[i] = mLine

                else:

                    get_format(i, line, line_substring)

            message_lines[i] = message_lines[i].replace('[', "")
            message_lines[i] = message_lines[i].replace(']', "")
            message_lines[i] = message_lines[i].replace("'", "")
            print(message_lines[i])
            i = i + 1

        # write file
        message_lines = ' '.join([str(elem) for elem in message_lines])
        f = open("format_output/"+args.infile+"_"+str(j)+".xml", 'a')
        f.write(str(message_lines))
        f.close()

        j=j+1
