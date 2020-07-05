import cv2 as cv
import numpy as np
import os
import time
import datetime
import gspread
import sys
from PIL import Image
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import cProfile
# import xlsxwriter


# ----------------------------------------------------------------------------------
# CONSTANTS


champlist_path = Path('D:/Scripts/Python/Champ_Select_Analyser/champlist.txt')
splash_path = Path('D:/Scripts/Python/Champ_Select_Analyser/ChampSplashesFixed')
icon_path = Path('D:/Scripts/Python/Champ_Select_Analyser/ChampIconsFixed')
champ_select_path = 'D:/Scripts/Python/Champ_Select_Analyser/ImageCropper/champ_selects/'

template_path = Path('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/Templates/')
results_path = Path('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/Results/')

# ----------------------------------------------------------------------------------
# SETUP

def importChamplist():

    with open(champlist_path, 'r') as f:
        return [name.strip() for name in f]


def removePreviousResults():
    previous_results = [ f for f in os.listdir(results_path) if f.endswith(".bmp") ]

    for f in previous_results:
        os.remove(os.path.join(results_path, f))


def removePreviousTemplates():
    templates = [ f for f in os.listdir(template_path) if f.endswith(".bmp") ]

    for f in templates:
        os.remove(os.path.join(template_path, f))


# false = saves to cropper folder
# true = saves to matcher folder
def saveToMatcher(bool):
    if (bool):
        cropPath = Path("D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/Templates/")
    else:
        cropPath = Path("D:/Scripts/Python/Champ_Select_Analyser/ImageCropper/temp_images/")

    return cropPath


# ----------------------------------------------------------------------------------
#  MATCHER


def organiseTemplates(number_of_copies):
    all_templates_unorganized = os.listdir(template_path)
    total_for_each_slot = ((number_of_copies * 2) + 1)     # 3 sml, 3 big + original


    # sort picks from entire template list, shape into numpy array
    pick_names = ['b1','b2','b3','b4','b5','r1','r2','r3','r4','r5']
    picks = [template for template in all_templates_unorganized if template[0:2] in pick_names]

    picks = np.array(picks)
    picks.shape = 10, total_for_each_slot


    # sort bans from entire template list, shape into numpy array
    ban_names = ['bb1','bb2','bb3','bb4','bb5','rb1','rb2','rb3','rb4','rb5']
    bans = [template for template in all_templates_unorganized if template[0:3] in ban_names]

    bans = np.array(bans)
    bans.shape = 10, total_for_each_slot

    return picks, bans


def template_match(champlist, templates_array, number_of_copies, image_filepath, type):
    search_results = []

    row = 0
    column = 0

    if type == 'bans':
        threshold = .70
    elif type == 'picks':
        threshold = 0.93
    else:
        return

    for i in range(10*number_of_copies):
        # math for iterating through the numpy array of templates
        if (column == number_of_copies):
            column = 0
            row += 1
            if not flag:
                search_results.append(current_template + ' - ' + '___' + ' - ' + '___')

        # when hitting the end of the last row, end
        if ( row >= 10):
            break

        flag = False

        current_template = templates_array[row][column]
        template = cv.imread(str(Path.joinpath(template_path, current_template)),0)

        matches = 0

        for name in champlist:

            if (flag):
                break

            print(' Matching --> '+ current_template + '   -   ' + name)
            files_to_check = (f for f in os.listdir(image_filepath) if name in f)

            for file in files_to_check:

                compare_image = cv.imread(str(image_filepath) + '\\' + file, 0)

                w, h = template.shape[::-1]

                res = cv.matchTemplate(compare_image, template, cv.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)

                for pt in zip(*loc[::-1]):

                    flag = True
                    matches += 1

                    _, max_val, _, max_loc = cv.minMaxLoc(res)
                    top_left = max_loc
                    bottom_right = (top_left[0] + w, top_left[1] + h)
                    cv.rectangle(compare_image, top_left, bottom_right, (255,255,255), 5)


                if (flag):
                    current_template2 = current_template.replace('.bmp', '')

                    print('                                        Found ' + str(matches) + ' matches: -- ' + name)
                    # cv.imwrite('Results/'+ current_template2 + '_' + name + '.bmp', compare_image)
                    search_results.append(current_template + ' - ' + name + ' - ' + str(matches))

                    if type == 'bans':
                        updateAccuracy(name, matches, 'accuracy_icons.txt')
                    else:
                        updateAccuracy(name, matches, 'accuracy_splash.txt')

                    column = -1
                    row += 1
                    # time.sleep(0.2)
                    break

        column += 1

    return search_results


def editTemplates(template_array, desired_pick_filename):
    """ manually overrides the list, for quicker testing """

    # turns np.array into list
    picks_list = template_array.tolist()
    mains_list = []

    # removes the picks we don't want
    for i in range(10):
        mains_list.append(picks_list[i][0])

    mains_list.remove(desired_pick_filename)

    # changes original template_array to the file we want
    for filename in mains_list:
        template_array = np.where(template_array == str(filename), desired_pick_filename, template_array)

    return template_array


def updateAccuracy(name, num_matches, filename):
    overall_match_accuracy = []
    with open('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/' + filename, 'r') as f:
        for line in f:
            champname, acc = line.split('-')
            champname = champname.strip()
            acc = acc.strip()
            overall_match_accuracy.append(champname)
            overall_match_accuracy.append(acc)


    index = overall_match_accuracy.index(name)
    overall_match_accuracy[index + 1] = num_matches

    with open('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/' + filename, 'w') as f:
        counter = 0
        for match in overall_match_accuracy:

            if ((counter % 2) == 0):
                champname = match
            else:
                champ_matches = match
                f.write(champname + ' - ' + str(champ_matches) + '\n')

            counter +=1


def createDefaultAccuracyFile(filename, champlist):
    with open('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/' + filename, 'w') as f:
        for name in champlist:
            f.write(name + ' - ' + '0 \n')



# ----------------------------------------------------------------------------------
#  RESULT OUTPUT


def printResultsToConsole(results_array):
    for i in range(len(results_array)):
        a, b, c = results_array[i].split('-')

        if (i == 0):
            print(' -> Blue:')

        if (i == 5):
            print(' -> Red:')

        print(' ' + a + ' = ' + b + ' ... ' + c)
    print()


def outputToGoogleSheet(bans_results, picks_results, sheet_name, worksheet_name, row_start, col_start):
    scope  = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds  = ServiceAccountCredentials.from_json_keyfile_name('CSA_secrets_GSuite.json', scope)
    client = gspread.authorize(creds)
    sheet  = client.open_by_url(sheet_name).worksheet(worksheet_name)

    total_results = bans_results + picks_results

    # placeholder results for testing
    # total_results = ['bb1.bmp - JarvanIV - 6', 'bb2.bmp - LeBlanc - 28', 'bb3.bmp - Olaf - 9',
    #                 'bb4.bmp - Rumble - 15', 'bb5.bmp - Nautilus - 29', 'rb1.bmp - Ornn - 9',
    #                 'rb2.bmp - Aphelios - 6', 'rb3.bmp - Sett - 6', 'rb4.bmp - Pantheon - 219',
    #                 'rb5.bmp - Renekton - 8',

    #                 'b1.bmp - Maokai - 16', 'b2.bmp - Elise - 15', 'b3.bmp - Azir - 2',
    #                 'b4.bmp - Ezreal - 4', 'b5.bmp - Senna - 13', 'r1.bmp - Kennen - 6',
    #                 'r2.bmp - LeeSin - 80', 'r3.bmp - VelKoz - 6', 'r4.bmp - TahmKench - 4',
    #                 'r5.bmp - Varus - 5']

    row = row_start
    col = col_start

    sheet.update_cell(row    , col    , (bans_results[0].split(' - '))[1])
    sheet.update_cell(row + 1, col    , (bans_results[1].split(' - '))[1])
    sheet.update_cell(row + 2, col    , (bans_results[2].split(' - '))[1])
    sheet.update_cell(row + 3, col    , (bans_results[3].split(' - '))[1])
    sheet.update_cell(row + 4, col    , (bans_results[4].split(' - '))[1])

    sheet.update_cell(row    , col + 1, (picks_results[0].split(' - '))[1])
    sheet.update_cell(row + 1, col + 1, (picks_results[1].split(' - '))[1])
    sheet.update_cell(row + 2, col + 1, (picks_results[2].split(' - '))[1])
    sheet.update_cell(row + 3, col + 1, (picks_results[3].split(' - '))[1])
    sheet.update_cell(row + 4, col + 1, (picks_results[4].split(' - '))[1])

    sheet.update_cell(row    , col + 2, (picks_results[5].split(' - '))[1])
    sheet.update_cell(row + 1, col + 2, (picks_results[6].split(' - '))[1])
    sheet.update_cell(row + 2, col + 2, (picks_results[7].split(' - '))[1])
    sheet.update_cell(row + 3, col + 2, (picks_results[8].split(' - '))[1])
    sheet.update_cell(row + 4, col + 2, (picks_results[9].split(' - '))[1])

    sheet.update_cell(row    , col + 3, (bans_results[5].split(' - '))[1])
    sheet.update_cell(row + 1, col + 3, (bans_results[6].split(' - '))[1])
    sheet.update_cell(row + 2, col + 3, (bans_results[7].split(' - '))[1])
    sheet.update_cell(row + 3, col + 3, (bans_results[8].split(' - '))[1])
    sheet.update_cell(row + 4, col + 3, (bans_results[9].split(' - '))[1])


def printUnknownAccuracy(filename):
    with open('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/' + filename, 'r') as f:
        counter = 0

        print()
        print('List of currently un-searched for champs:')
        print()

        for line in f:
            champname, acc = line.split(' - ')
            champname = champname.strip()
            acc = acc.strip()

            if (int(acc) == 0):
                counter += 1
                print(champname + ': ' + str(acc))

        print()
        print('Total: ' + str(counter) + ' unkown champs')


def printLowAccuracy(filename):
    with open('D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/' + filename, 'r') as f:
        counter = 0

        print()
        print('List of currently low accuracy champs: ')
        print()

        for line in f:
            champname, acc = line.split(' - ')
            champname = champname.strip()
            acc = acc.strip()

            if (int(acc) <= 5):
                counter += 1
                print(champname + ': ' + str(acc))

        print()
        print('Total: ' + str(counter) + ' low accuracy champs')



# ----------------------------------------------------------------------------------
# TEMPLATE CROPPER


# lists of champion select tuple coords (top-left point, bottom-right point)
# IF YOU CHANGE THESE - CHECK findEdges OUTPUT
def buildCropLocations():

    bb1 = ("bb1", (40, 980, 110, 1050))
    bb2 = ("bb2", (130, 980, 200, 1050))
    bb3 = ("bb3", (220, 980, 290, 1050))
    bb4 = ("bb4", (315, 980, 385, 1050))
    bb5 = ("bb5", (408, 980, 478, 1050))
    rb1 = ("rb1", (1820, 980, 1890, 1050))
    rb2 = ("rb2", (1725, 980, 1795, 1050))
    rb3 = ("rb3", (1630, 980, 1700, 1050))
    rb4 = ("rb4", (1538, 980, 1608, 1050))
    rb5 = ("rb5", (1445, 980, 1515, 1050))
    ban_coords = [bb1, bb2, bb3, bb4, bb5, rb1, rb2, rb3, rb4, rb5]

    b1 = ("b1", (90,180,290,320))
    b2 = ("b2", (90,335,290,475))
    b3 = ("b3", (90,495,290,635))
    b4 = ("b4", (90,655,290,795))
    b5 = ("b5", (90,810,290,950))
    r1 = ("r1", (1635,180,1835,320))
    r2 = ("r2", (1635,335,1835,475))
    r3 = ("r3", (1635,495,1835,635))
    r4 = ("r4", (1635,655,1835,795))
    r5 = ("r5", (1635,810,1835,950 ))
    pick_coords = [b1, b2, b3, b4, b5, r1, r2, r3, r4, r5]

    return ban_coords, pick_coords


# finds the width & height of both picks and ban slots
# also checks for inconsistency in crop coords (for if i manually change them)
def findEdges(list_of_coords):

    flag        = False
    width_test  = 0
    height_test = 0
    counter     = 0

    for label, coord_tuple in list_of_coords:
        a,b,c,d = coord_tuple
        width = (c - a)
        height = (d - b)

        width_test += width
        height_test += height
        counter += 1

        # checks for variance in each crop size
        if (width_test / counter != width):
            flag = True
        if flag:
            print(label + ' is cropped differently than other coords')
            # time.sleep(1)

    return width, height


def cropTemplates(champ_select_image, pick_coords, ban_coords, cropPath):

    for coords in pick_coords :
        cropped_image = champ_select_image.crop(coords[1])
        cropped_image.save(Path.joinpath(cropPath, coords[0] + ".bmp"))

    for coords in ban_coords:
        cropped_image = champ_select_image.crop(coords[1])
        cropped_image.save(Path.joinpath(cropPath, coords[0] + ".bmp"))


def createResizedCopies(list_of_crops, number_of_copies, w, h, cropPath):

    for crop, coord in list_of_crops:

        crop_filename = crop + '.bmp'
        resize_factor_fixed = 0.01

        counter       = -1
        resize_factor = resize_factor_fixed

        #create 'number_of_copies' smaller copies
        for i in range(number_of_copies):
            width = w
            height = h
            counter = str(int(counter) + 2).zfill(2)
            height = int(round(height - (height * resize_factor)))
            width = int(round(width - (width * resize_factor)))

            copy_image = Image.open(Path.joinpath(cropPath, str(crop_filename)))
            copy_image = copy_image.resize((width, height))
            copy_image.save(str(cropPath) + '/' + crop + '_' + str(counter) + '(s).bmp')

            resize_factor += resize_factor_fixed

        counter       = 0
        resize_factor = resize_factor_fixed

        #create 'number_of_copies' bigger copies
        for i in range(number_of_copies):
            width = w
            height = h
            counter = str(int(counter) + 2).zfill(2)
            height = int(round(height + (height * resize_factor)))
            width = int(round(width + (width * resize_factor)))

            copy_image = Image.open(Path.joinpath(cropPath, str(crop_filename)))
            copy_image = copy_image.resize((width, height))
            copy_image.save(str(cropPath) + '/' + crop + '_' + str(counter) + '(b).bmp')

            resize_factor += resize_factor_fixed


def start_timer():
    return time.perf_counter()


def end_timer(time_start):
    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=time_stop - time_start, ))

    print('\n-----------------------')
    print(f'Runtime: {elapsed_time}')
    print('-----------------------')


def main():


    # ----------------------------------------------------------------------------------
    # MAIN



    # initial setup
    champlist = importChamplist()

    # Google Sheet output location + increments
    row_start = 23
    col_start = 13
    row_inc   = 0      # distance from top-left cell of game to game
    col_inc   = 5      # distance from top-left cell of game to game

    cropPath  = saveToMatcher(True)
    number_of_copies   = 3
    pick_coords, ban_coords = buildCropLocations()





    # ------------- ONLY UN-COMMENT ONE ---------------------------------------

    # ---- for all champ selects in the folder 'champ_select_path'
    # champselect_image_list = [f for f in os.listdir(champ_select_path) if f.endswith(".bmp")]

    # ---- for only the latest champ select
    champselect_image_list = [f for f in os.listdir(champ_select_path) if f.endswith(".bmp")]
    champselect_image_list = [champselect_image_list[-1]]

    # --------------------------------------------------------------------------



    if len(sys.argv) > 1:
        google_sheet_name = sys.argv[1]
        if sys.argv[2] == 'Game':
            worksheet_name = sys.argv[2] + ' ' + sys.argv[3]
        else:
            worksheet_name = sys.argv[2]
    else:
        google_sheet_name = input('Please enter sheet URL: ')
        worksheet_name = input('Please enter worksheet name: ')

    time_start = start_timer()

    print(google_sheet_name)
    print(worksheet_name)



    for image in champselect_image_list:

        # CROPPER
        print('Cropper working on: ' + image)

        removePreviousTemplates()
        removePreviousResults()

        champ_select_image = Image.open(champ_select_path + image)

        print('                                ... cropping templates')
        cropTemplates(champ_select_image, pick_coords, ban_coords, cropPath)

        print('                                ... making duplicates')
        icon_width_fixed, icon_height_fixed = findEdges(ban_coords)
        splash_width_fixed, splash_height_fixed = findEdges(pick_coords)

        createResizedCopies(ban_coords, number_of_copies, icon_width_fixed, icon_height_fixed, cropPath)
        createResizedCopies(pick_coords, number_of_copies, splash_width_fixed, splash_height_fixed, cropPath)


        # MATCHER
        print('Matcher working on: ' + image)

        picks, bans = organiseTemplates(number_of_copies)
        # picks = editTemplates(picks, 'r4.bmp')
        # bans = editTemplates(bans, 'rb3.bmp')

        bans_results = template_match(champlist, bans, number_of_copies, icon_path, 'bans')
        picks_results = template_match(champlist, picks, number_of_copies, splash_path, 'picks')

        print(' ------------ Bans ------------ ' )
        printResultsToConsole(bans_results)
        print(' ------------ Picks ------------ ' )
        printResultsToConsole(picks_results)

        end_timer(time_start)

        if google_sheet_name != '':
            print('Sending results to Google Sheet ... ')
            outputToGoogleSheet(bans_results, picks_results, google_sheet_name, worksheet_name, row_start, col_start)
            row_start += row_inc
            col_start += col_inc




    # printUnknownAccuracy('accuracy_splash.txt')
    # printLowAccuracy('accuracy_splash.txt')




    print()
    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds = time_stop - time_start, ))
    print('Time taken: ' + elapsed_time)




# ----------------------------------------------------------------------------------



# cProfile.run('main()')

main()