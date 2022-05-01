# perara seed
# v1.5.6
# Last update: 30 Apr 2022

# Dumps JP and EN text from all 8 msyt directories in an easy-to-read csv format.
# Hopefully paves the way for more accurate English translation work.

# Comment clean-up.


import os  # Need this for creating directories.
import re  # Regex (Regular Expressions)
import unicodecsv as csv  # Need Unicode for writing the csv files correctly

import msvcrt as m  # Required for letting the user "Press any key to continue"
import time  # Required for "pausing" after the print statements
from tqdm import tqdm  # Required for showing progress bars


# Generate the directories for holding the extracted text.
def makeMTJPexDir():  

    pathMTJPex = 'output'
    pathMTJPex_AT = 'output/ActorType'
    pathMTJPex_DM = 'output/DemoMsg'
    pathMTJPex_EFM = 'output/EventFlowMsg'
    pathMTJPex_LM = 'output/LayoutMsg'
    pathMTJPex_QM = 'output/QuestMsg'
    pathMTJPex_ShM = 'output/ShoutMsg'
    pathMTJPex_StM = 'output/StaticMsg'
    pathMTJPex_T = 'output/Tips'

    outputDir = os.path.isdir(pathMTJPex)
    od_AT = os.path.isdir(pathMTJPex_AT)
    od_DM = os.path.isdir(pathMTJPex_DM)
    od_EFM = os.path.isdir(pathMTJPex_EFM)
    od_LM = os.path.isdir(pathMTJPex_LM)
    od_QM = os.path.isdir(pathMTJPex_QM)
    od_ShM = os.path.isdir(pathMTJPex_ShM)
    od_StM = os.path.isdir(pathMTJPex_StM)
    od_T = os.path.isdir(pathMTJPex_T)

    if not outputDir:
        os.mkdir(pathMTJPex)
    if not od_AT:
        os.mkdir(pathMTJPex_AT)
    if not od_DM:
        os.mkdir(pathMTJPex_DM)
    if not od_EFM:
        os.mkdir(pathMTJPex_EFM)
    if not od_LM:
        os.mkdir(pathMTJPex_LM)
    if not od_QM:
        os.mkdir(pathMTJPex_QM)
    if not od_ShM:
        os.mkdir(pathMTJPex_ShM)
    if not od_StM:
        os.mkdir(pathMTJPex_StM)
    if not od_T:
        os.mkdir(pathMTJPex_T)

# =========================================================
# 		Functions for extracting English text
# =========================================================


def enMTExtract(str1, str2, str3, comSegTitle):

    pattern1 = r'text: .*'  # pattern for detecting the text.

    # Pattern for detecting field_3
    patFieldFurLen = r'field_3: [0-9]{1,2}[:.,-]?$'

    furDel = 0		# Integer for determining how many furigana there are at the beginning of a line
    # = how many characters from the beginning of the line to delete

    # String that will contain the isolated Japanese text for each part of the Quest description.
    enText = ''
    segTitle = ''

    # potTitle = Potential Title. Holds the title of each segment in the msyt file.
    potTitle = ''

    # Write the output csv file, in the directory output
    # with open('output/'+str3+str2+'.csv', 'wb') as file:		# Uses unicodecsv

    # Define the csv writer. Need the "encoding" piece to handle the Japanese text correctly.
    # filewriter = csv.writer(file, encoding='utf-8')   

    # Write the column headers into the csv file
    # filewriter.writerow((column0, column1, column2))

    numLines = 0  # Value for column '#'

    # Read from the input msyt file.
    with open('msyt_EN/'+str3+str1, "r", encoding="utf-8") as x:

        lines = x.readlines()  # Get a list of every line of the input msyt file

        # Parse through each input file line.
        for i in lines:

            if 'field_3' in i:		# should never be touched with the EN msyt files

                value_num = (re.compile(patFieldFurLen)).search(i)
                # Takes the relevant pattern into account... Now value_num has all the text of line i, with that pattern factored in.

                value_split = (value_num.group(0)).split()
                # value_split is now a list of all the text in value_num, with each item having been split by a ' ' (space) by default.
                # For example, the original line "field_3: 6" is now stored in value_split as ['field_3', '6']
                
                furDel = int(value_split[1])
                # Takes the value of field_3, converts this string into an integer, then
                # gives that integer to furDel. This is the total number of bytes of furigana characters in the next "text:" line.
                # Dividing this number by 2 gives the number of furigana characters to delete.
                # Remember that each character is 2 bytes.

            # if statement for detecting the segment title. The 'contents' field is always the line after the segment title.
            elif 'contents:' in i:

                if segTitle[:-1] == comSegTitle:
                    return enText

                # Reset the 3 values to correctly dump the output from the next segment.
                enText = ''
                segTitle = ''
                numLines += 1

                # Store the title of the new segment in segTitle
                title_split = potTitle.split()
                segTitle = title_split[0]

            elif 'text:' in i:  # Capture the Japanese text in each line that starts with 'text:'

                furDel = furDel//2  # This is the correct format for Integer Division

                # Look for pattern1 in line i.
                # If pattern1 is not there, value_num becomes a None object
                value_num = (re.compile(pattern1)).search(i)

                minusQuo = ''

                if value_num != None:

                    # Take all of the text in value_num.group(0) that is separated by spaces,
                    # put each chunk into one list all together.
                    value_split = (value_num.group(0)).split()

                    # Handle cases where the text itself is separated by spaces.
                    if len(value_split) > 1:

                        minusQuo += value_split[1]

                        spaceNum = 2

                        while spaceNum < len(value_split):

                            if value_split[spaceNum] != '\"':

                                minusQuo += ' '
                                minusQuo += value_split[spaceNum]

                                spaceNum += 1

                            else:
                                spaceNum += 1

                    # Remove double quotation marks.
                    # Remove the leading quotation mark
                    if len(minusQuo) > 1 and minusQuo[0] == '\"':

                        minusQuo = minusQuo[1:]

                        if minusQuo[-1] == '\"':

                            # Remove the trailing quotation mark
                            minusQuo = minusQuo[:-1]

                    # Remove double \\n's, format the text appropriately.
                    if '\\n\\n' in minusQuo:
                        # Split JP text with double \n as a separator.
                        value_newL = minusQuo.split('\\n\\n')

                        minusQuo = (value_newL[0])[furDel:]
                        minusQuo += '\n'
                        minusQuo += '\n'

                        vnlNum = 1
                        while vnlNum < len(value_newL):

                            if vnlNum != (len(value_newL)-1):

                                minusQuo += (value_newL[vnlNum])
                                minusQuo += '\n'
                                minusQuo += '\n'

                                vnlNum += 1

                            else:
                                minusQuo += (value_newL[vnlNum])

                                vnlNum += 1

                    # Remove single \\n's, format the text appropriately.
                    if '\\n' in minusQuo:
                        value_sNewL = minusQuo.split('\\n')

                        minusQuo = (value_sNewL[0])
                        minusQuo += '\n'

                        vsnlNum = 1

                        while vsnlNum < len(value_sNewL):

                            if vsnlNum != (len(value_sNewL)-1):

                                minusQuo += (value_sNewL[vsnlNum])
                                minusQuo += '\n'

                                vsnlNum += 1

                            else:

                                minusQuo += (value_sNewL[vsnlNum])

                                vsnlNum += 1

                    enText += minusQuo

                    furDel = 0  # Reset the counter for how many furigana characters to delete

            # Extracts the correct line with the section title.
            potTitle = i

    # Write the final segment of text to the csv file.
    if segTitle[:-1] == comSegTitle:
        return enText


def enMTEvExtract(str1, str2, str3, comSegTitle):
    pattern1 = r'text: .*'  # pattern for detecting the text.

    # Pattern for detecting field_3
    patFieldFurLen = r'field_3: [0-9]{1,2}[:.,-]?$'

    furDel = 0		# Integer for determining how many furigana there are at the beginning of a line
    # # = how many characters from the beginning of the line to delete

    # String that will contain the isolated Japanese text for each part of the Quest description.
    enText = ''
    segTitle = ''

    # potTitle = Potential Title. Holds the title of each segment in the msyt file.
    potTitle = ''

    numLines = 0  # Value for column '#'

    # Read from the input msyt file.
    with open('msyt_EN/'+str3+str1, "r", encoding="utf-8") as x:

        lines = x.readlines()  # Get a list of every line of the input msyt file

        # Counter for proper indexing so that i and the two lines before it are stored at all times.
        store2L = 0
        # This holds the segment title. In this folder, the segment title is always 2 lines before the 'contents' field.
        str2L = ''

        # Parse through each input file line.
        for i in lines:

            if 'field_3' in i:		# should never be touched with the EN msyt files

                value_num = (re.compile(patFieldFurLen)).search(i)
                # Takes the relevant pattern into account.
                # Now value_num has all the text of line i, with that pattern factored in.
                
                value_split = (value_num.group(0)).split()
                # value_split is now a list
                # of all the text in value_num, with each item having been split by a ' ' (space) by default.
                # For example, the original line "field_3: 6" is now stored in value_split as ['field_3', '6']
                
                furDel = int(value_split[1])
                # Takes the value of field_3, converts this string into an integer, then
                # gives that integer to furDel. This is the total number of bytes of furigana characters in the next "text:" line.
                # Dividing this number by 2 gives the number of furigana characters to delete.
                # Remember that each character is 2 bytes.

            # if statement for detecting the segment title. The 'contents' field is always the line after the segment title.
            elif 'contents:' in i:

                if segTitle[:-1] == comSegTitle:
                    return enText

                # Reset the 3 values to correctly dump the output from the next segment.
                enText = ''
                segTitle = ''
                numLines += 1

                # Store the title of the new segment in segTitle
                title_split = str2L.split()
                segTitle = title_split[0]

            elif 'text:' in i:  # Capture the Japanese text in each line that starts with 'text:'

                furDel = furDel//2  # This is the correct format for Integer Division

                # Look for pattern1 in line i.
                # If pattern1 is not there, value_num becomes a None object
                value_num = (re.compile(pattern1)).search(i)

                minusQuo = ''

                if value_num != None:

                    value_split = value_num.group(0)[6:]  # Remove 'text: '

                    minusQuo += value_split

                    # Remove double quotation marks.
                    # Remove the leading quotation mark
                    if len(minusQuo) > 1 and minusQuo[0] == '\"':

                        minusQuo = minusQuo[1:]

                        if minusQuo[-1] == '\"':

                            # Remove the trailing quotation mark
                            minusQuo = minusQuo[:-1]

                    # Remove double \\n's, format the text appropriately.
                    if '\\n\\n' in minusQuo:
                        # Split JP text with double \n as a separator.
                        value_newL = minusQuo.split('\\n\\n')

                        minusQuo = (value_newL[0])[furDel:]
                        minusQuo += '\n'
                        minusQuo += '\n'

                        vnlNum = 1
                        while vnlNum < len(value_newL):

                            if vnlNum != (len(value_newL)-1):

                                minusQuo += (value_newL[vnlNum])
                                minusQuo += '\n'
                                minusQuo += '\n'

                                vnlNum += 1

                            else:

                                minusQuo += (value_newL[vnlNum])

                                vnlNum += 1

                    # Remove single \\n's, format the text appropriately.
                    if '\\n' in minusQuo:
                        value_sNewL = minusQuo.split('\\n')

                        minusQuo = (value_sNewL[0])
                        minusQuo += '\n'

                        vsnlNum = 1

                        while vsnlNum < len(value_sNewL):

                            if vsnlNum != (len(value_sNewL)-1):

                                minusQuo += (value_sNewL[vsnlNum])
                                minusQuo += '\n'

                                vsnlNum += 1

                            else:
                                minusQuo += (value_sNewL[vsnlNum])

                                vsnlNum += 1

                    enText += minusQuo

                    furDel = 0  # Reset the counter for how many furigana characters to delete

            if store2L != 1:
                store2L += 1
            else:
                str2L = potTitle
            # Extract the correct line with the section title.
            potTitle = i

    # Write the final segment of text to the csv file.
    if segTitle[:-1] == comSegTitle:
        return enText


# =========================================================
# 		Functions for extracting Japanese text
# =========================================================

# Function for extracting the Japanese text from ActorType, DemoMsg, LayoutMsg, ShoutMsg, StaticMsg, and Tips.
# Originally intended to write a unique function for each directory, but the files in all but EventFlowMsg
# are formatted in essentially the same way. I wrote this function 2nd, after jpQuestExtract.
def jpDemoExtract(str1, str2, str3):
    # str1 is the name of the msyt file, including the msyt extension.
    # str2 is the name of the msyt file, without the msyt extension.
    # str3 is the name of the folder that both contains the input file (in the input directory)
    # and contains the output file (in the output directory). e.g., 'ActorType'

    pattern1 = r'text: .*'  # pattern for detecting the text.

    # Pattern for detecting field_3
    patFieldFurLen = r'field_3: [0-9]{1,2}[:.,-]?$'

    furDel = 0		# Integer for determining how many furigana there are at the beginning of a line
    # = how many characters from the beginning of the line to delete

    # String that will contain the isolated Japanese text for each part of the Quest description.
    jpText = ''
    segTitle = ''
    enText = ''

    # potTitle = Potential Title. Holds the title of each segment in the msyt file.
    potTitle = ''

    # Write the output csv file, in the directory called 'output'
    with open('output/'+str3+str2+'.csv', 'wb') as file:		# Uses unicodecsv

        # Define the csv writer. Need the "encoding" piece to handle the Japanese text correctly.
        filewriter = csv.writer(file, encoding='utf-8')

        # Column headers
        column0 = '#'       # Denotes the order of each text segment in the msyt file.
        column1 = 'Title'   # Denotes the segment title.
        column2 = 'JPja'    # Denotes the JP text in each segment.
        column3 = 'USen'

        # Write the column headers into the csv file
        filewriter.writerow((column0, column1, column2, column3))

        numLines = 0  # Value for column '#'

        # Read from the input msyt file.
        with open('msyt_JP/'+str3+str1, "r", encoding="utf-8") as x:

            lines = x.readlines()  # Get a list of every line of the input msyt file

            # Parse through each input file line.
            for i in lines:

                if 'field_3' in i:		# if statement to get the integer value of field_3

                    value_num = (re.compile(patFieldFurLen)).search(i)
                    # Takes the relevant pattern into account.
                    # Now value_num has all the text of line i, with that pattern factored in.
                    
                    value_split = (value_num.group(0)).split()
                    # value_split is now a list
                    # of all the text in value_num, with each item having been split by a ' ' (space) by default.
                    # For example, the original line "field_3: 6" is now stored in value_split as ['field_3', '6']
                    
                    furDel = int(value_split[1])
                    # Takes the value of field_3, converts this string into an integer, then
                    # gives that integer to furDel. This is the total number of bytes of furigana characters in the next "text:" line.
                    # Dividing this number by 2 gives the number of furigana characters to delete.
                    # Remember that each character is 2 bytes.

                # if statement for detecting the segment title. The 'contents' field is always the line after the segment title.
                elif 'contents:' in i:

                    if numLines > 0:  # Removes an extra blank row between the column headers and the content.
                        # Write the #, segment title, and Japanese text to the csv file
                        enText = enMTExtract(str1, str2, str3, segTitle[:-1])

                        filewriter.writerow(
                            [numLines, segTitle[:-1], jpText, enText])

                    # Reset the 3 values to correctly dump the output from the next segment.
                    jpText = ''
                    segTitle = ''
                    enText = ''
                    numLines += 1

                    # Store the title of the new segment in segTitle
                    title_split = potTitle.split()
                    segTitle = title_split[0]

                elif 'text' in i:  # Capture the Japanese text in each line that starts with 'text:'

                    furDel = furDel//2  # This is the correct format for Integer Division

                    # Look for pattern1 in line i.
                    # If pattern1 is not there, value_num becomes a None object.
                    value_num = (re.compile(pattern1)).search(i)

                    if value_num != None:

                        # Take all of the text in value_num.group(0) that is separated by spaces,
                        # put each chunk into one list all together.
                        value_split = (value_num.group(0)).split()

                        # Store the actual game text in minusQuo. value_split[0] should be 'text:'
                        minusQuo = ''

                        # Accommodate instances where the text itself is split up by spaces.

                        if len(value_split) > 1:

                            minusQuo += value_split[1]

                            valueNum = 2

                            while valueNum < len(value_split):

                                if value_split[valueNum] != '\"':

                                    minusQuo += ' '
                                    minusQuo += value_split[valueNum]

                                    valueNum += 1

                                else:

                                    valueNum += 1

                        # Remove double quotation marks.
                        # Remove the leading quotation mark
                        if len(minusQuo) > 1 and minusQuo[0] == '\"':

                            minusQuo = minusQuo[1:]

                            if minusQuo[-1] == '\"':

                                # Remove the trailing quotation mark
                                minusQuo = minusQuo[:-1]
                        # Users can use Google Sheets or Visual Studio Code for viewing the final csv files.

                        # Remove the furigana after removing any quotation marks
                        minusQuo = minusQuo[furDel:]

                        # Remove double \\n's, format the text appropriately.
                        if '\\n\\n' in minusQuo:
                            # Split JP text with double \n as a separator.
                            value_newL = minusQuo.split('\\n\\n')

                            minusQuo = (value_newL[0])
                            minusQuo += '\n'
                            minusQuo += '\n'

                            vnlNum = 1
                            while vnlNum < len(value_newL):

                                if vnlNum != (len(value_newL)-1):

                                    minusQuo += (value_newL[vnlNum])
                                    minusQuo += '\n'
                                    minusQuo += '\n'

                                    vnlNum += 1

                                else:

                                    minusQuo += (value_newL[vnlNum])

                                    vnlNum += 1

                        # Remove single \\n's, format the text appropriately.
                        if '\\n' in minusQuo:
                            value_sNewL = minusQuo.split('\\n')

                            minusQuo = (value_sNewL[0])
                            minusQuo += '\n'

                            vsnlNum = 1

                            while vsnlNum < len(value_sNewL):

                                if vsnlNum != (len(value_sNewL)-1):

                                    minusQuo += (value_sNewL[vsnlNum])
                                    minusQuo += '\n'

                                    vsnlNum += 1

                                else:

                                    minusQuo += (value_sNewL[vsnlNum])

                                    vsnlNum += 1

                        jpText += minusQuo

                        furDel = 0  # Reset the counter for how many furigana characters to delete

                # Extract the correct line with the section title.
                potTitle = i

        # Write the final segment of text to the csv file.
        enText = enMTExtract(str1, str2, str3, segTitle[:-1])

        if numLines > 0:
            filewriter.writerow([numLines, segTitle[:-1], jpText, enText])


def jpEventFExtract(str1, str2, str3):

    pattern1 = r'text: .*'

    patFieldFurLen = r'field_3: [0-9]{1,2}[:.,-]?$'

    furDel = 0

    jpText = ''
    segTitle = ''

    potTitle = ''

    with open('output/'+str3+str2+'.csv', 'wb') as file:

        filewriter = csv.writer(file, encoding='utf-8')

        column0 = '#'
        column1 = 'Title'
        column2 = 'JPja'
        column3 = 'USen'

        filewriter.writerow((column0, column1, column2, column3))

        numLines = 0

        with open('msyt_JP/'+str3+str1, "r", encoding="utf-8") as x:

            lines = x.readlines()

            # Counter for proper indexing so that i and the two lines before it are stored at all times.
            store2L = 0
            # This holds the segment title. In this folder, the segment title is always 2 lines before the 'contents' field.
            str2L = ''

            for i in lines:

                if 'field_3' in i:

                    value_num = (re.compile(patFieldFurLen)).search(i)

                    value_split = (value_num.group(0)).split()

                    furDel = int(value_split[1])

                elif 'contents:' in i:

                    if numLines > 0:

                        enText = enMTEvExtract(str1, str2, str3, segTitle[:-1])
                        filewriter.writerow(
                            [numLines, segTitle[:-1], jpText, enText])

                    jpText = ''
                    segTitle = ''
                    numLines += 1

                    title_split = str2L.split()
                    segTitle = title_split[0]

                # Print each line in QL_100enemy.msyt that has text: * in it. (prints the Japanese text)
                elif 'text' in i:

                    furDel = furDel//2  # This is the correct format for Integer Division
                    value_num = (re.compile(pattern1)).search(i)

                    if value_num != None:

                        value_split = (value_num.group(0)).split()
                        # Another example: The original line "text: EX ohayou" is now stored in value_split as ['text:', 'EX', 'ohayou']

                        minusQuo = ''

                        # Handle cases where the text itself is separated by spaces.
                        if len(value_split) > 1:

                            minusQuo += value_split[1]

                            spaceNum = 2

                            while spaceNum < len(value_split):

                                if value_split[spaceNum] != '\"':

                                    minusQuo += ' '
                                    minusQuo += value_split[spaceNum]

                                    spaceNum += 1

                                else:

                                    spaceNum += 1

                        # Remove double quotation marks.
                        if len(minusQuo) > 1 and minusQuo[0] == '\"':

                            minusQuo = minusQuo[1:]

                            if minusQuo[-1] == '\"':

                                minusQuo = minusQuo[:-1]

                        minusQuo = minusQuo[furDel:]

                        if '\\n\\n' in minusQuo:

                            # Split JP text with double \n as a separator.
                            value_newL = minusQuo.split('\\n\\n')

                            minusQuo = (value_newL[0])

                            minusQuo += '\n'
                            minusQuo += '\n'

                            vnlNum = 1
                            while vnlNum < len(value_newL):

                                if vnlNum != (len(value_newL)-1):

                                    minusQuo += (value_newL[vnlNum])
                                    minusQuo += '\n'
                                    minusQuo += '\n'

                                    vnlNum += 1

                                else:

                                    minusQuo += (value_newL[vnlNum])

                                    vnlNum += 1

                        if '\\n' in minusQuo:

                            value_sNewL = minusQuo.split('\\n')

                            minusQuo = (value_sNewL[0])
                            minusQuo += '\n'

                            vsnlNum = 1

                            while vsnlNum < len(value_sNewL):

                                if vsnlNum != (len(value_sNewL)-1):

                                    minusQuo += (value_sNewL[vsnlNum])
                                    minusQuo += '\n'

                                    vsnlNum += 1

                                else:

                                    minusQuo += (value_sNewL[vsnlNum])

                                    vsnlNum += 1

                        jpText += minusQuo

                        furDel = 0

                if store2L != 1:
                    store2L += 1
                else:
                    str2L = potTitle

                potTitle = i

        enText = enMTEvExtract(str1, str2, str3, segTitle[:-1])
        if numLines > 0:
            filewriter.writerow([numLines, segTitle[:-1], jpText, enText])

# Put all the actual extraction code into an extracting function.


def jpQuestExtract(str1, str2):

    pattern1 = r'text: .*'
    pattern2 = r'QL_.*'
    # Pattern for detecting field_3
    patFieldFurLen = r'field_3: [0-9]{1,2}[:.,-]?$'

    furDel = 0

    jpText = ''
    segTitle = ''
    enText = ''

    with open('output/QuestMsg/'+str2+'.csv', 'wb') as file:		# Uses unicodecsv

        filewriter = csv.writer(file, encoding='utf-8')

        column0 = '#'
        column1 = 'Title'
        column2 = 'JPja'
        column3 = 'USen'

        filewriter.writerow((column0, column1, column2, column3))

        numLines = 0

        with open('msyt_JP/'+'QuestMsg/'+str1, "r", encoding="utf-8") as x:

            lines = x.readlines()
            for i in lines:

                if 'field_3' in i:

                    value_num = (re.compile(patFieldFurLen)).search(i)

                    value_split = (value_num.group(0)).split()

                    furDel = int(value_split[1])

                elif 'QL_' in i:			# if statement to get the title of the segment of the Quest

                    if numLines > 0:
                        enText = enMTExtract(
                            str1, str2, 'QuestMsg/', segTitle[:-1])
                        filewriter.writerow(
                            [numLines, segTitle[:-1], jpText, enText])

                    # Reset jpText so that the final product is not ALL of the Japanese text in this msyt file.
                    jpText = ''
                    segTitle = ''
                    numLines += 1

                    value_num = (re.compile(pattern2)).search(i)
                    segTitle = value_num.group(0)

                # Print each line in QL_100enemy.msyt that has text: * in it. (prints the Japanese text)
                elif 'text' in i:

                    furDel = furDel//2  # This is the correct format for Integer Division
                    value_num = (re.compile(pattern1)).search(i)

                    if value_num != None:

                        value_split = (value_num.group(0)).split()
                        # Another example: The original line "text: EX ohayou" is now stored in value_split as ['text:', 'EX', 'ohayou']

                        minusQuo = ''

                        # Accommodate instances where the text itself is split up by spaces.
                        if len(value_split) > 1:

                            minusQuo += value_split[1]

                            valueNum = 2

                            while valueNum < len(value_split):

                                if value_split[valueNum] != '\"':

                                    minusQuo += ' '
                                    minusQuo += value_split[valueNum]

                                    valueNum += 1

                                else:

                                    valueNum += 1

                        # Remove double quotation marks.
                        if len(minusQuo) > 1 and minusQuo[0] == '\"':

                            minusQuo = minusQuo[1:]

                            if minusQuo[-1] == '\"':

                                minusQuo = minusQuo[:-1]

                        minusQuo = minusQuo[furDel:]

                        if '\\n\\n' in minusQuo:

                            # Split JP text with double \n as a separator.
                            value_newL = minusQuo.split('\\n\\n')

                            minusQuo = (value_newL[0])
                            minusQuo += '\n'
                            minusQuo += '\n'

                            vnlNum = 1
                            while vnlNum < len(value_newL):

                                if vnlNum != (len(value_newL)-1):

                                    minusQuo += (value_newL[vnlNum])
                                    minusQuo += '\n'
                                    minusQuo += '\n'

                                    vnlNum += 1

                                else:

                                    minusQuo += (value_newL[vnlNum])

                                    vnlNum += 1

                        if '\\n' in minusQuo:

                            value_sNewL = minusQuo.split('\\n')

                            minusQuo = (value_sNewL[0])
                            minusQuo += '\n'

                            vsnlNum = 1

                            while vsnlNum < len(value_sNewL):

                                if vsnlNum != (len(value_sNewL)-1):

                                    minusQuo += (value_sNewL[vsnlNum])
                                    minusQuo += '\n'

                                    vsnlNum += 1

                                else:

                                    minusQuo += (value_sNewL[vsnlNum])

                                    vsnlNum += 1

                        jpText += minusQuo

                        furDel = 0

        if numLines > 0:
            enText = enMTExtract(
                str1, str2, 'QuestMsg/', segTitle[:-1])
            filewriter.writerow([numLines, segTitle[:-1], jpText, enText])

def main():
    print("Perara Seed v1.0.0 authenticated.")
    print('===')
    print()

    time.sleep(2)

    pathActor = 'msyt_JP/ActorType'
    actorFiles = os.listdir(pathActor)
    aF_num = 0

    # Parse through all msyt files in the directory DemoMsg.
    pathDemo = 'msyt_JP/DemoMsg'
    demoFiles = os.listdir(pathDemo)
    dF_num = 0

    pathEvent = 'msyt_JP/EventFlowMsg'
    eventFiles = os.listdir(pathEvent)
    eF_num = 0

    pathLay = 'msyt_JP/LayoutMsg'
    layFiles = os.listdir(pathLay)
    laF_num = 0

    # Parse through all msyt files in the directory QuestMsg.
    pathQuest = 'msyt_JP/QuestMsg'
    questFiles = os.listdir(pathQuest)
    qF_num = 0 

    pathShout = 'msyt_JP/ShoutMsg'
    shoutFiles = os.listdir(pathShout)
    shF_num = 0

    pathStat = 'msyt_JP/StaticMsg'
    statFiles = os.listdir(pathStat)
    stF_num = 0

    pathTips = 'msyt_JP/Tips'
    tipsFiles = os.listdir(pathTips)
    tF_num = 0

    makeMTJPexDir()

    fileCounter = 0

    print('Distilling ActorType text...')
    time.sleep(2)
    print('Expecting 33 files...')
    time.sleep(1)
    for aF in actorFiles:
        fileCounter += 1
    print('%i out of 33 files discovered.' % fileCounter)
    time.sleep(1)

    # Print a progress bar for file extraction.
    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpDemoExtract(actorFiles[i], (actorFiles[i])[:-5], 'ActorType/')
        aF_num += 1

    print('ActorType text extracted.')
    time.sleep(2)
    print('%i out of 33 files processed.' % aF_num)
    time.sleep(2)
    print()

    fileCounter = 0

    print('Distilling DemoMsg text...')
    time.sleep(2)
    print('Expecting 163 files...')
    time.sleep(1)
    for dF in demoFiles:
        fileCounter += 1
    print('%i out of 163 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpDemoExtract(demoFiles[i], (demoFiles[i])[:-5], 'DemoMsg/')
        dF_num += 1

    print('DemoMsg text extracted.')
    time.sleep(2)
    print('%i out of 163 files processed.' % dF_num)
    time.sleep(2)
    print()

    fileCounter = 0
    print('Distilling EventFlowMsg text...')
    time.sleep(2)
    print('Expecting 640 files...')
    time.sleep(1)
    for eF in eventFiles:
        fileCounter += 1
    print('%i out of 640 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpEventFExtract(eventFiles[i], (eventFiles[i])[:-5], 'EventFlowMsg/')
        eF_num += 1

    print('EventFlowMsg text extracted.')
    time.sleep(2)
    print('%i out of 640 files processed.' % eF_num)
    time.sleep(2)
    print()

    fileCounter = 0
    print('Distilling LayoutMsg text...')
    time.sleep(2)
    print('Expecting 55 files...')
    time.sleep(1)

    for laF in layFiles:
        fileCounter += 1
    print('%i out of 55 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpDemoExtract(layFiles[i], (layFiles[i])[:-5], 'LayoutMsg/')
        laF_num += 1

    print('LayoutMsg text extracted.')
    time.sleep(2)
    print('%i out of 55 files processed.' % laF_num)
    time.sleep(2)
    print()

    fileCounter = 0
    print('Distilling QuestMsg text...')
    time.sleep(2)
    print('Expecting 169 files...')
    time.sleep(1)
    for qF in questFiles:
        fileCounter += 1
    print('%i out of 169 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpQuestExtract(questFiles[i], (questFiles[i])[:-5])
        qF_num += 1

    print('QuestMsg text extracted.')
    time.sleep(2)
    print('%i out of 169 files processed.' % qF_num)
    time.sleep(2)
    print()

    fileCounter = 0
    print('Distilling ShoutMsg text...')
    time.sleep(2)
    print('Expecting 9 files...')
    time.sleep(1)
    for shF in shoutFiles:
        fileCounter += 1
    print('%i out of 9 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpDemoExtract(shoutFiles[i], (shoutFiles[i])[:-5], 'ShoutMsg/')
        shF_num += 1

    print('ShoutMsg text extracted.')
    time.sleep(2)
    print('%i out of 9 files processed.' % shF_num)
    time.sleep(2)
    print()

    fileCounter = 0
    print('Distilling StaticMsg text...')
    time.sleep(2)
    print('Expecting 13 files...')
    time.sleep(1)
    for stF in statFiles:
        fileCounter += 1
    print('%i out of 13 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpDemoExtract(statFiles[i], (statFiles[i])[:-5], 'StaticMsg/')
        stF_num += 1

    print('StaticMsg text extracted.')
    time.sleep(2)
    print('%i out of 13 files processed.' % stF_num)
    time.sleep(2)
    print()

    fileCounter = 0
    print('Distilling Tips text...')
    time.sleep(2)
    print('Expecting 9 files...')
    time.sleep(1)
    for tF in tipsFiles:
        fileCounter += 1
    print('%i out of 9 files discovered.' % fileCounter)
    time.sleep(1)

    for i in tqdm(range(fileCounter),
                  desc="Distilling…",
                  ascii=False, ncols=75):
        jpDemoExtract(tipsFiles[i], (tipsFiles[i])[:-5], 'Tips/')
        tF_num += 1

    print('Tips text extracted.')
    time.sleep(2)
    print('%i out of 9 files processed.' % tF_num)
    time.sleep(2)
    print()


def wait():
    print("Extraction complete. Press any key to continue. ")
    m.getch()


main()

wait()
