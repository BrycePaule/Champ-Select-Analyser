import os
import numpy as np
import cv2 as cv
import time

from AccuracyManager import AccuracyManager
from TemplateCropper import TemplateCropper


class TemplateMatcher:

    def __init__(self, template_duplicate_count):
        self.splash_path = f'{os.getcwd()}/Assets/Splashes/'
        self.icon_path = f'{os.getcwd()}/Assets/Icons/'

        self.champlist_path = f'{os.getcwd()}/champlist.txt/'
        self.champ_select_path = f'{os.getcwd()}/ChampSelectScreenshots/'
        self.template_path = f'{os.getcwd()}/Templates/'
        self.results_path = f'{os.getcwd()}/Results/'

        self.accuracy_filepath_picks = f'{os.getcwd()}/Accuracy/accuracy_splash.txt/'
        self.accuracy_filepath_bans = f'{os.getcwd()}/Accuracy/accuracy_icons.txt/'

        self.champlist = self.import_champlist()
        self.duplicate_count = template_duplicate_count

        self.cropper = TemplateCropper(self.duplicate_count)
        self.champ_select_slots = [
            'bb1', 'bb2', 'bb3', 'bb4', 'bb5',
            'rb1', 'rb2', 'rb3', 'rb4', 'rb5',
            'b1', 'b2', 'b3', 'b4', 'b5',
            'r1', 'r2', 'r3', 'r4', 'r5',
        ]


    """ TEMPLATE MATCHING """

    def get_champ_select_image(self, all_templates=False):
        """
        Returns the latest champ select screenshot, or a list of all
        screenshots in the directory if all=True
        """

        if all_templates:
            return (f for f in os.listdir(self.champ_select_path) if f.endswith(".bmp"))
        else:
            return [[f for f in os.listdir(self.champ_select_path) if f.endswith(".bmp")][-1]]

    def match(self, champ_select_image_number):
        """
        Returns a dict of match results:
            slot: (champion name, match counter)

        Effectively follows this procedure:
            - takes a template from the 2D array
            - steps through every champion in champlist
            - checks the template against both splash/icon, normal and inverted
            - if it finds a successful match over the given threshold, it
              moves onto the next set of templates, skipping all the resized
              duplicates in that row
            - otherwise it resizes the template, and continues matching
        """

        self.clear_stored_results()
        results = {slot: None for slot in self.champ_select_slots}

        for slot in self.champ_select_slots:

            # if bans
            if len(slot) == 3:
                match_accuracy_threshold = 0.70
                image_filepath = self.icon_path

            # if picks
            else:
                match_accuracy_threshold = 0.93
                image_filepath = self.splash_path

            for template_number in range(self.duplicate_count * 2 + 1):
                template = self.cropper.create_template(champ_select_image_number, slot, template_number)

                for champion in self.champlist:
                    print(f'Matching: {slot} (attempt {template_number + 1}) > {champion}')

                    if not os.path.exists(f'{image_filepath}{champion}.bmp'):
                        raise Exception(f'{champion} does not have a downloaded image.')

                    champ_image = cv.imread(f'{image_filepath}{champion}.bmp', 0)
                    matches_default = self.template_match(champ_image, template, match_accuracy_threshold)

                    champ_image_inverted = cv.imread( f'{image_filepath}{champion}_inverted.bmp', 0)
                    matches_inverted = self.template_match(champ_image_inverted, template, match_accuracy_threshold)

                    best_match = max(matches_default, matches_inverted)

                    if best_match > 0:
                        print(f'{" " * 20} Match -- {champion} ({best_match})')
                        results[slot] = (champion, best_match)
                        break

                # break case - if already found a match
                if results[slot] is not None:
                    break

            if results[slot] is None:
                results[slot] = (None, 0)

        return results

    def template_match(self, champ_image, template_image, match_accuracy_threshold):
        res = cv.matchTemplate(champ_image, template_image, cv.TM_CCOEFF_NORMED)

        reasonable_matches = np.where(res >= match_accuracy_threshold)
        matches = np.count_nonzero(reasonable_matches) // 2
        # this is halved, because it's counting both x and y coords of matches, meaning two non-zeros = one match

        return matches


    """ MISC """

    def clear_stored_results(self):
        """ Clears results directory of any previous results """

        previous_results = [f for f in os.listdir(self.results_path) if f.endswith(".bmp")]

        for f in previous_results:
            os.remove(os.path.join(self.results_path, f))


    def update_accuracy(self, results, bans=False):
        """ Updates TemplateMatcher accuracy trackers. """

        accuracy_manager = AccuracyManager()
        accuracy_manager.update_accuracy_file(results, bans)


    """ OUTPUT """

    def print_results(self, results):
        """ Print results to console. """

        bans = list(results.values())[:10]
        bans = [('x', 0) if result[0] is None else result for result in bans]
        bans = zip(bans[:5], bans[5:])

        picks = list(results.values())[10:]
        picks = [('x', 0) if result[0] is None else result for result in picks]
        picks = zip(picks[:5], picks[5:])

        max_champ_name_len = max((len(result[0]) for result in results.values() if result[0] is not None))

        print('\n -----------  Bans  ----------- ')
        for row in bans:
            blue_champ, blue_accuracy = row[0][0], row[0][1]
            red_champ, red_accuracy = row[1][0], row[1][1]
            b_pick = f'{blue_champ.ljust(max_champ_name_len)} {str(blue_accuracy).ljust(2)}'
            r_pick = f'{str(red_accuracy).ljust(2)}  {red_champ.ljust(max_champ_name_len)}'
            print(f'{b_pick}     |     {r_pick}')

        print('\n -----------  Picks  ----------- ')
        for row in picks:
            blue_champ, blue_accuracy = row[0][0], row[0][1]
            red_champ, red_accuracy = row[1][0], row[1][1]
            b_pick = f'{blue_champ.ljust(max_champ_name_len)} {str(blue_accuracy).ljust(2)}'
            r_pick = f'{str(red_accuracy).ljust(2)}  {red_champ.ljust(max_champ_name_len)}'
            print(f'{b_pick}     |     {r_pick}')


    """ CHAMPLIST """

    def import_champlist(self):
        """ Imports champlist from file. """

        with open(self.champlist_path, 'r') as f:
            return [name.strip() for name in f]