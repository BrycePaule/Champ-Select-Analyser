import os
import numpy as np
import cv2 as cv


class TemplateMatcher():


    def __init__(self):
        self.splash_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Splashes'
        self.icon_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Icons'

        self.champlist_path = 'D:/Scripts/Python/ChampSelectAnalyser/champlist.txt/'
        self.champ_select_path = 'D:/Scripts/Python/ChampSelectAnalyser/ChampSelectScreenshots/'
        self.template_path = 'D:/Scripts/Python/ChampSelectAnalyser/Templates/'
        self.results_path = 'D:/Scripts/Python/ChampSelectAnalyser/Results/'

        self.accuracy_filepath_splash = 'D:/Scripts/Python/ChampSelectAnalyser/Accuracy/accuracy_splash.txt/'
        self.accuracy_filepath_icons = 'D:/Scripts/Python/ChampSelectAnalyser/Accuracy/accuracy_icons.txt/'

        self.champlist = self.importChamplist()


    def removePreviousResults(self):
        previous_results = [f for f in os.listdir(self.results_path) if
                            f.endswith(".bmp")]

        for f in previous_results:
            os.remove(os.path.join(self.results_path, f))


    def organiseTemplates(self, number_of_copies):
        all_templates_unorganized = os.listdir(self.template_path)
        total_for_each_slot = ((number_of_copies * 2) + 1)  # 3 sml, 3 big + original

        # sort picks from entire template list, shape into numpy array
        pick_names = ['b1', 'b2', 'b3', 'b4', 'b5', 'r1', 'r2', 'r3', 'r4', 'r5']
        picks = [template for template in all_templates_unorganized if
                 template[0:2] in pick_names]

        picks = np.array(picks)
        picks.shape = 10, total_for_each_slot

        # sort bans from entire template list, shape into numpy array
        ban_names = ['bb1', 'bb2', 'bb3', 'bb4', 'bb5', 'rb1', 'rb2', 'rb3', 'rb4', 'rb5']
        bans = [template for template in all_templates_unorganized if
                template[0:3] in ban_names]

        bans = np.array(bans)
        bans.shape = 10, total_for_each_slot

        return picks, bans


    def match(self, champlist, templates_array, number_of_copies, image_filepath, type):
        search_results = []

        row = 0
        column = 0

        if type == 'bans':
            threshold = .70
        elif type == 'picks':
            threshold = 0.93
        else:
            return

        for i in range(10 * number_of_copies):
            # math for iterating through the numpy array of templates
            if column == number_of_copies:
                column = 0
                row += 1
                if not flag:
                    search_results.append(current_template + ' - ' + '___' + ' - ' + '___')

            # when hitting the end of the last row, end
            if (row >= 10):
                break

            flag = False

            current_template = templates_array[row][column]
            template = cv.imread(f'{self.template_path}{current_template}', 0)

            matches = 0

            for name in champlist:

                if (flag):
                    break

                print(' Matching --> ' + current_template + '   -   ' + name)
                files_to_check = (f for f in os.listdir(image_filepath) if
                                  name in f)

                for file in files_to_check:

                    compare_image = cv.imread(
                        str(image_filepath) + '\\' + file, 0)

                    w, h = template.shape[::-1]

                    res = cv.matchTemplate(compare_image, template,
                                           cv.TM_CCOEFF_NORMED)
                    loc = np.where(res >= threshold)

                    for pt in zip(*loc[::-1]):
                        flag = True
                        matches += 1

                        _, max_val, _, max_loc = cv.minMaxLoc(res)
                        top_left = max_loc
                        bottom_right = (top_left[0] + w, top_left[1] + h)
                        cv.rectangle(compare_image, top_left, bottom_right, (255, 255, 255), 5)

                    if (flag):
                        print('                                        Found ' + str(matches) + ' matches: -- ' + name)
                        search_results.append(current_template + ' - ' + name + ' - ' + str(matches))

                        # TODO NEEDS FIXING ---------------------------
                        # if type == 'bans':
                        #     self.updateAccuracy(name, matches, icons=True)
                        # else:
                        #     self.updateAccuracy(name, matches)

                        column = -1
                        row += 1
                        break

            column += 1

        return search_results


    def editTemplates(self, template_array, desired_pick_filename):
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
            template_array = np.where(template_array == str(filename),
                                      desired_pick_filename, template_array)

        return template_array


    """ OUTPUTS """

    def printResultsToConsole(self, results_array):
        for i in range(len(results_array)):
            a, b, c = results_array[i].split('-')

            if (i == 0):
                print(' -> Blue:')

            if (i == 5):
                print(' -> Red:')

            print(' ' + a + ' = ' + b + ' ... ' + c)
        print()


    def printUnknownAccuracy(self):
        with open(self.accuracy_filepath_splash, 'r') as f:
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


    def printLowAccuracy(self):
        with open(self.accuracy_filepath_splash, 'r') as f:
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
            print(
                'Total: ' + str(counter) + ' low accuracy champs')


    """ ACCURACY """

    def updateAccuracy(self, name, num_matches):
        # TODO: NEEDS FIXING --------------------------------------------------------------
        overall_match_accuracy = []

        with open(self.accuracy_filepath_splash, 'r') as f:
            for line in f:
                champname, acc = line.split('-')
                champname = champname.strip()
                acc = acc.strip()
                overall_match_accuracy.append(champname)
                overall_match_accuracy.append(acc)

        index = overall_match_accuracy.index(name)
        overall_match_accuracy[index + 1] = num_matches

        with open(self.accuracy_filepath_splash, 'w') as f:
            counter = 0
            for match in overall_match_accuracy:

                if (counter % 2) == 0:
                    champname = match
                else:
                    champ_matches = match
                    f.write(champname + ' - ' + str(champ_matches) + '\n')

                counter += 1


    def createDefaultAccuracyFile(self, icons=False):
        if icons:
            with open(self.accuracy_filepath_icons, 'w') as f:
                for name in self.champlist:
                    f.write(name + ' - ' + '0 \n')
        else:
            with open(self.accuracy_filepath_icons, 'w') as f:
                for name in self.champlist:
                    f.write(name + ' - ' + '0 \n')


    """ CHAMPLIST """

    def importChamplist(self):
        with open(self.champlist_path, 'r') as f:
            return [name.strip() for name in f]