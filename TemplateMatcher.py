import os
import numpy as np
import cv2 as cv
import time


class TemplateMatcher():


    def __init__(self, template_duplicate_count):
        self.splash_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Splashes/'
        self.icon_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Icons/'

        self.champlist_path = 'D:/Scripts/Python/ChampSelectAnalyser/champlist.txt/'
        self.champ_select_path = 'D:/Scripts/Python/ChampSelectAnalyser/ChampSelectScreenshots/'
        self.template_path = 'D:/Scripts/Python/ChampSelectAnalyser/Templates/'
        self.results_path = 'D:/Scripts/Python/ChampSelectAnalyser/Results/'

        self.accuracy_filepath_picks = 'D:/Scripts/Python/ChampSelectAnalyser/Accuracy/accuracy_splash.txt/'
        self.accuracy_filepath_bans = 'D:/Scripts/Python/ChampSelectAnalyser/Accuracy/accuracy_icons.txt/'

        self.champlist = self.importChamplist()
        self.duplicate_count = template_duplicate_count


    def clear_results(self):
        """ Clears results directory of any previous results """

        previous_results = [f for f in os.listdir(self.results_path) if f.endswith(".bmp")]

        for f in previous_results:
            os.remove(os.path.join(self.results_path, f))


    def organise_templates(self):
        all_templates = os.listdir(self.template_path)
        templates_per_slot = ((self.duplicate_count * 2) + 1)  # X sml, X big + original

        pick_names = ['b1', 'b2', 'b3', 'b4', 'b5', 'r1', 'r2', 'r3', 'r4', 'r5']
        picks = [template for template in all_templates if template[0:2] in pick_names]
        picks = np.array(picks)
        picks.shape = (10, templates_per_slot)

        ban_names = ['bb1', 'bb2', 'bb3', 'bb4', 'bb5', 'rb1', 'rb2', 'rb3', 'rb4', 'rb5']
        bans = [template for template in all_templates if template[0:3] in ban_names]
        bans = np.array(bans)
        bans.shape = 10, templates_per_slot

        return picks, bans


    def match(self, templates, slot_type='picks'):
        """
        Clusterfuck of logic that template matches champ select crops against
        champion splashes and ban icons

        Effectively it follow this procedure:
            - takes a template from the 2D array
            - steps through every champion in champlist
            - checks the template against both splash/icon, normal and inverted
            - if it finds a successful match over the given threshold, it
              moves onto the next set of templates, skipping all the resized
              duplicates in that row

        Given that procedure it seems very simple, but this code needs to be
        cleaned up a LOT, this is a nested mess of break statements, terrible
        """

        search_results = []

        if slot_type == 'bans':
            threshold = .70
            image_filepath = self.icon_path
        else:
            threshold = 0.93
            image_filepath = self.splash_path


        for row in templates:
            skip_slot = False

            for template_label in row:
                template_image = cv.imread(f'{self.template_path}{template_label}', 0)
                matches = 0
                champ_found = False

                if skip_slot:
                    break

                for name in self.champlist:
                    if champ_found:
                        skip_slot = True
                        break

                    print(' Matching --> ' + template_label + '   -   ' + name)
                    image_filepaths = [
                        f'{image_filepath}{name}.bmp',
                        f'{image_filepath}{name}_inverted.bmp'
                    ]

                    for filepath in image_filepaths:
                        compare_image = cv.imread(filepath, 0)

                        res = cv.matchTemplate(compare_image, template_image, cv.TM_CCOEFF_NORMED)
                        loc = np.where(res >= threshold)

                        for match in zip(*loc[::-1]):
                            champ_found = True
                            matches += 1

                        if champ_found:
                            print(f'                                        Found {matches} matches: -- ' + name)
                            search_results.append(f'{template_label} - {name} - {matches}')

                            if slot_type == 'bans':
                                self.updateAccuracy(name, matches, bans=True)
                            else:
                                self.updateAccuracy(name, matches)

                            break


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
        with open(self.accuracy_filepath_picks, 'r') as f:
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
        with open(self.accuracy_filepath_picks, 'r') as f:
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

    def updateAccuracy(self, name, num_matches, bans=True):
        """ Updates accuracy trackers """

        overall_match_accuracy = []

        if bans:
            accuracy_filepath = self.accuracy_filepath_bans
        else:
            accuracy_filepath = self.accuracy_filepath_picks

        with open(accuracy_filepath, 'r') as f:
            for line in f:
                champname, acc = line.split('-')
                champname = champname.strip()
                acc = acc.strip()
                overall_match_accuracy.append(champname)
                overall_match_accuracy.append(acc)

        index = overall_match_accuracy.index(name)
        overall_match_accuracy[index + 1] = num_matches

        with open(accuracy_filepath, 'w') as f:
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
            with open(self.accuracy_filepath_bans, 'w') as f:
                for name in self.champlist:
                    f.write(name + ' - ' + '0 \n')
        else:
            with open(self.accuracy_filepath_bans, 'w') as f:
                for name in self.champlist:
                    f.write(name + ' - ' + '0 \n')


    """ CHAMPLIST """

    def importChamplist(self):
        with open(self.champlist_path, 'r') as f:
            return [name.strip() for name in f]