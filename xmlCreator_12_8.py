# This program takes in an example XML file and creates a given number of random XML files
# If a string is added to the table of floats an NA will replace the string

import argparse
import numpy as np
import sys
import xml.etree.ElementTree as eT
import xml.dom.minidom
import glob
import os


# read in input, output files, and number of XML files
def parse_command_line():
    """
       Parses command line

       """

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input filename")
    parser.add_argument("output", help="output filename")
    parser.add_argument("xmlNumber", type=int, help="an integer for number of xml files")
    arg = parser.parse_args()
    return arg


# open file
def read_file(file_name):
    """
       read file and place in message

       Arguments
       ---------
       file_name : str
           a filename to read
       """

    __file = open(file_name)
    message = __file.read()

    return message


# separate different values in a string by space
def convert(string):
    """
       Creates list of words from string

       Arguments
       ---------
       string : str
           a string to be separated
       """
    li = list(string.split(" "))
    return li


if __name__ == "__main__":

    import argparse
    import numpy as np
    import sys
    import xml.etree.ElementTree as eT
    import xml.dom.minidom
    import glob
    import os

    # parse command line
    args = parse_command_line()
    os.mkdir(args.output)

    j = 1
    # for every XML file in the directory
    for file in glob.glob('/home/kristina/PycharmProjects/pythonProject4/' + str(args.infile) + '/*.xml'):

        try:
            # read in file for xml file number
            tree = eT.parse(file)
            root = tree.getroot()
        except eT.ParseError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("The file is not in correct XML format. The error is on line " + str(exc_tb.tb_lineno) + ".")
            sys.exit()

        path = '/home/kristina/PycharmProjects/pythonProject4/' + args.output + '/sample' + str(j)
        os.mkdir(path)

        k = 1
        # number of random XML files to create
        while k <= args.xmlNumber:

            i = 0
            for child in tree.iter():
                attribute = child.attrib

                # if data is a table
                if len(child.text.split()) > 1:

                    # convert table to string
                    separated_string = convert(child.text)
                    updated_string = separated_string

                    p = 0

                    # get each table element
                    for element in separated_string:
                        element = str(element)

                        if element and element.strip():

                            # replace original number with new random number
                            if '\n' in element:
                                try:
                                    element = str(
                                        np.random.uniform(.5 * (float(element) + .01), 1.5 * (float(element) + .01)))
                                    element = element + '\n'
                                except ValueError:
                                    element = 'NA' + ' \n'
                            else:
                                try:
                                    element = str(
                                        np.random.uniform(.5 * (float(element) + .01), 1.5 * (float(element) + .01)))
                                except ValueError:
                                    element = 'NA'
                            updated_string[p] = element

                        p = p + 1
                    # using list comprehension
                    listToStr = ' '.join([str(elem) for elem in updated_string])
                    child.text = (str(listToStr))

            for child in tree.iter():

                # get xml attributes in each xml line
                attribute = child.attrib

                if attribute.get('distribution') == 'uniform':

                    # get variable values for distribution
                    min_out = attribute.get('min')
                    max_out = attribute.get('max')

                    try:
                        # find random value
                        randomUniform = np.random.uniform(float(min_out), float(max_out))
                        child.text = str(randomUniform)
                        # print(child.text)

                    # except TypeError:
                    except TypeError:
                        print(
                            "The max and min values must be strings of numbers. The error is in node " + str(
                                child.tag))
                        child.text = child.text[2:len(child.text) - 2]
                        continue

                elif attribute.get('distribution') == 'normal':
                    std_out = attribute.get('std')
                    mean_out = attribute.get('mean')
                    if mean_out is None:
                        mean_out = attribute.get('max')
                        print('As no mean value exists, the max value is being used')

                    try:
                        # find random value
                        randomNormal = np.random.normal(float(std_out), float(mean_out))
                    except TypeError:
                        print("The mean and std values must be strings of numbers. The error is in node " + str(
                            child.tag))
                        continue

                    child.text = str(randomNormal)

            # remove unnecessary data
            for child in tree.iter():
                child.attrib.pop("min", None)
                child.attrib.pop("max", None)
                child.attrib.pop("std", None)
                child.attrib.pop("distribution", None)
                child.attrib.pop("updated", None)

            # write tree to file
            tree.write(str(k) + "_" + str(args.output))

            # make xml pretty
            dom = xml.dom.minidom.parse(str(k) + "_" + str(args.output))  # or xml.dom.minidom.parseString(xml_string)
            pretty_xml_as_string = dom.toprettyxml()

            # remove extra files
            os.remove(str(k) + "_" + str(args.output))

            # get input filename to name output
            fileParts = file.split('/')
            fileLast = fileParts[-1].split('.')
            fileName = fileLast[0]

            # write final file
            f = open(args.output + "/sample" + str(j) + "/" + fileName + "_" + str(k) + ".xml", 'a')
            f.write(pretty_xml_as_string)
            f.close()

            k = k + 1
        j = j + 1
