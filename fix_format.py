# This file formats XML files so that they can be parsed without error.

import re
import argparse
from bs4 import BeautifulSoup


# open file
def read_file(file_name):
    __file = open(file_name)
    message_in = __file.read()
    return message_in


# parse command line
def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input filename")
    parser.add_argument("output", help="output filename")
    parser.add_argument('xmlNumber', type=int, help='an integer for number of xml files')
    args_in = parser.parse_args()
    return args_in


# read in using beautiful soup which will place a symbol on every ill-formed line
args = parse_command_line()
infile = open(args.infile, "r")
contents = infile.read()
soup = str(BeautifulSoup(contents, 'xml'))

# write to xml file to be able to use readlines() with input data
f = open("soup_xml.xml", "w")
f.write(soup)
f.close()

# read in using readlines()
args = parse_command_line()
message = open('soup_xml.xml', "r+")
message_lines = message.readlines()

i = 0
while i < len(message_lines)-1:

    line = (message_lines[i])

    line_substring = line[line.find('>')+1:line.rfind('<')]
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

        line_substring = line_substring[len(line_substring)-1:len(line_substring)]

        # if there is a units attributes
        if line.count('unit') > 0:

            # find unit start index
            line = line.split()
            indexUnit = message_lines[i].find('unit')

            # find unit attribute end
            firstIndex = message_lines[i].find('"', indexUnit)
            endIndex = message_lines[i].find('"', firstIndex+1)

            line_substring2 = line[0]
            line_substring2 = line_substring2[1:]
            line_substring2 = list(line_substring2)

            # find <> indices
            bracket1 = message_lines[i].find('<')
            bracket2 = message_lines[i].find('>')

            # find string inside <>
            line_substring2 = line_substring2[bracket1:bracket2-1]
            line_substring2 = ''.join(line_substring2)

            # get unit attribute
            line_substring3 = message_lines[i]
            line_substring3 = line_substring3[indexUnit:endIndex+1]

            # replace bad XML with tag and keep original value for random variable
            message_lines[i] = re.sub(str('>.+?<'), ' > ' + str(line_substring) + ' < ', str(line))
            message_lines[i] = re.sub(str('<.+?>'), '</' + str(line_substring2) + ' > ', str(message_lines[i]))

            mLine1 = list(message_lines[i])
            mLine = mLine1[1:len(mLine1)]
            mLine[2] = ''
            mLine = ''.join(mLine)

            # add in unit attribute
            mLine = mLine.split()
            mLine[1] = line_substring3 + '>'
            mLine = ' '.join(mLine)
            message_lines[i] = mLine

        else:

            # replace bad XML with just tag as unit was not provided
            line = line.split()
            line_substring2 = line[0]
            line_substring2 = line_substring2[1:]
            message_lines[i] = re.sub(str('>.+?<'), '>' + str(line_substring)+'<', str(line))
            message_lines[i] = re.sub(str('<.+?>'), '</' + str(line_substring2) + '>', str(message_lines[i]))

            # final format
            mLine1 = list(message_lines[i])
            mLine = (mLine1[1:len(mLine1)])
            mLine[2] = ''
            mLine = ''.join(mLine)
            message_lines[i] = mLine

    message_lines[i] = message_lines[i].replace('[', "")
    message_lines[i] = message_lines[i].replace(']', "")
    message_lines[i] = message_lines[i].replace("'", "")
    print(message_lines[i])
    i = i + 1

# write file
message_lines = ' '.join([str(elem) for elem in message_lines])
f = open("formatted.xml", 'a')
f.write(str(message_lines))
f.close()
