# This program takes in an example XML file and create a given number of random XML files
import argparse
import numpy as np
import sys
import xml.etree.ElementTree as ET


# read in input, output files, and number of XML files
def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="input filename")
    parser.add_argument("output", help="output filename")
    parser.add_argument("xmlNumber", type=int, help="an integer for number of xml files")
    arg = parser.parse_args()
    return arg


# open file
def read_file(file_name):
    __file = open(file_name)
    message = __file.read()
    return message


# separate different values in a string by space
def convert(string):
    li = list(string.split(" "))
    return li


# find random values depending on distribution
def recurse(node_in):

    for child_in in node_in:

        attribute_in = child_in.attrib

        if attribute_in.get('distribution') == 'uniform':
            min_in = attribute_in.get('min')
            max_in = attribute_in.get('max')

            try:
                # find random value
                random_uniform_in = np.random.uniform(float(min_in), float(max_in))
                child_in.text = str(random_uniform_in)
                # remove unnecessary data
                child_in.attrib.pop("min", None)
                child_in.attrib.pop("max", None)
                child_in.attrib.pop("std", None)
                child_in.attrib.pop("unit", None)
                child_in.attrib.pop("distribution", None)
                child_in.attrib.pop("updated", None)

            except:

                print("The max and min must be strings of numbers.")

                # remove unnecessary data
                child_in.attrib.pop("min", None)
                child_in.attrib.pop("max", None)
                child_in.attrib.pop("std", None)
                child_in.attrib.pop("unit", None)
                child_in.attrib.pop("distribution", None)
                child_in.attrib.pop("updated", None)

                continue
            child_in.text = str(random_uniform_in)
        elif attribute_in.get('distribution') == 'normal':

            std_in = attribute_in.get('std')
            max_in = attribute_in.get('max')

            try:
                # find random value
                random_normal_in = np.random.normal(float(std_in), float(max_in))
                child_in.text = str(random_normal_in)

                child_in.attrib.pop("min", None)
                child_in.attrib.pop("max", None)
                child_in.attrib.pop("std", None)
                child_in.attrib.pop("unit", None)
                child_in.attrib.pop("distribution", None)
                child_in.attrib.pop("updated", None)
            except:
                print("The max and min must be strings of numbers.")

                # remove unnecessary data
                child_in.attrib.pop("min", None)
                child_in.attrib.pop("max", None)
                child_in.attrib.pop("std", None)
                child_in.attrib.pop("unit", None)
                child_in.attrib.pop("distribution", None)
                child_in.attrib.pop("updated", None)

                continue

        else:

            # remove unnecessary data
            child_in.attrib.pop("min", None)
            child_in.attrib.pop("max", None)
            child_in.attrib.pop("std", None)
            child_in.attrib.pop("unit", None)
            child_in.attrib.pop("distribution", None)
            child_in.attrib.pop("updated", None)
            continue




try:
    # read in file for xml file number
    args = parse_command_line()
    tree = ET.parse(args.infile)
    root = tree.getroot()
except:
    print("The file could not be read in.")
    sys.exit()

j = 1
while j <= args.xmlNumber:
    try:
        args = parse_command_line()
        tree = ET.parse(args.infile)
        root = tree.getroot()
    except:
        print("The file could not be read in.")
        sys.exit()

    for child in root:

        # get xml attributes in each xml line
        attribute = (child.attrib)

        if attribute.get('distribution') == 'uniform':

            # get variable values for distribution
            min_out = attribute.get('min')
            max_out = attribute.get('max')

            try:
                # find random value
                randomUniform = np.random.uniform(float(min_out), float(max_out))
                child.text = str(randomUniform)

            except:
                print(
                    "The max and min values are not correct. They must be strings of numbers. The error is in node " + str(
                        child.tag))
                continue

        elif attribute.get('distribution') == 'normal':
            std_out = attribute.get('std')
            max_out = attribute.get('max')

            try:
                # find random value
                randomNormal = np.random.normal(float(std_out), float(max_out))
            except:
                print("The max and std values are not correct. They must be strings of numbers. The error is in node " + str(
                        child.tag))
                continue

            child.text = str(randomNormal)

    # Find grandchildren
    for child in root:
        node = root.find(child.tag)
        print(node)
        recurse(node)

    i = 0
    for child in root:
        #node = root.find(child.tag)

        if child.tag == 'aero_table':

            # create random value for table
            randomNormal1 = np.random.uniform(-1000, 1000)

            # separate table values by space
            separated_string = convert(child.text)

            # remove whitespace
            while '' in separated_string:
                separated_string.remove('')

            i = 0
            a = np.empty(len(separated_string) - 1)

            # create table with the same number of values as the original table
            while i < len(separated_string) - 1:
                number = str(np.random.uniform(-300, 300))
                a[i] = str(number)
                i = i + 1

            child.text = str(a)

    # remove unnecessary data
    for child in root:
        child.attrib.pop("min", None)
        child.attrib.pop("max", None)
        child.attrib.pop("std", None)
        child.attrib.pop("unit", None)
        child.attrib.pop("distribution", None)
        child.attrib.pop("updated", None)

    # write tree to file
    tree.write('xmlOutput/' + str(j) + "_" + str(args.output))

    # counter for number of XML files
    j = j + 1
