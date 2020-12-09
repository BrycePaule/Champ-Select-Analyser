import os
import numpy as np
import cv2 as cv

from AccuracyManager import AccuracyManager
from TemplateCropper import TemplateCropper


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

        self.champlist = self.import_champlist()
        self.duplicate_count = template_duplicate_count

        self.cropper = TemplateCropper(self.duplicate_count)


    """ TEMPLATE MATCHING """

    def analyse_champion_select(self, image):
        """
        Main function to be called externally.

        Crops the given champ select into relevant templates.  TemplateMatches
        those to find which slot is which champion, returns results
        """

        self.cropper.create_templates(image)

        bans, picks = self.organise_templates()

        # bans = self.manual_template_override(bans, 'bb2.bmp')
        # picks = self.manual_template_override(picks, 'r4.bmp')

        ban_results = self.match(bans, bans=True)
        pick_results = self.match(picks)

        self.print_results(ban_results, bans=True)
        self.print_results(pick_results)

        return ban_results, pick_results


    def get_champ_select_image(self, all_templates=False):
        """
        Returns the latest champ select screenshot, or a list of all
        screenshots in the directory if all=True
        """

        if all_templates:
            return (f for f in os.listdir(self.champ_select_path) if f.endswith(".bmp"))
        else:
            return [[f for f in os.listdir(self.champ_select_path) if f.endswith(".bmp")][-1]]


    def organise_templates(self):
        """
        Organises an unsorted list of all templates in the directory into
        pick / ban numpy arrays for ease of use.
        """

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

        return bans, picks


    def match(self, templates, bans=False):
        """
        Clusterfuck of logic that template matches champ select crops against
        champion splashes and ban icons.

        Returns a list strings containing:
            image label, champion name, and match counter

        Effectively follows this procedure:
            - takes a template from the 2D array
            - steps through every champion in champlist
            - checks the template against both splash/icon, normal and inverted
            - if it finds a successful match over the given threshold, it
              moves onto the next set of templates, skipping all the resized
              duplicates in that row

        Given that procedure it seems very simple, but this code needs to be
        cleaned up a LOT, this is a nested mess of break statements, terrible
        """

        self.clear_stored_results()
        results = []

        if bans:
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
                match_found = False

                if skip_slot:
                    break

                for champ_name in self.champlist:
                    if match_found:
                        skip_slot = True
                        break

                    print(f' Matching --> {template_label}   -   {champ_name}')
                    image_filepaths = [
                        f'{image_filepath}{champ_name}.bmp',
                        f'{image_filepath}{champ_name}_inverted.bmp'
                    ]

                    for filepath in image_filepaths:
                        compare_image = cv.imread(filepath, 0)

                        res = cv.matchTemplate(compare_image, template_image, cv.TM_CCOEFF_NORMED)
                        loc = np.where(res >= threshold)

                        for match in zip(*loc[::-1]):
                            match_found = True
                            matches += 1

                        if match_found:
                            print(f'                                        Found {matches} matches: -- ' + champ_name)
                            results.append([template_label, champ_name, matches])
                            break

                if template_label == row[-1] and not match_found:
                    results.append([row[0], None, 0])

        self.update_accuracy(results, bans)

        return results


    def manual_template_override(self, templates, desired_label):
        """
        Manually overrides the template list with a single given label,
        for quicker testing.

        e.g. manual_template_override(picks, 'r4.bmp')
        (picks in this instance is the output of organise_templates())
        """

        template_count_per_slot = (self.duplicate_count * 2) + 1

        new_templates = [[desired_label for label in slot] for slot in templates]
        new_templates = np.array(new_templates)
        new_templates.shape = 10, template_count_per_slot

        return new_templates


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

    def print_results(self, results_array, bans=False):
        """ Print results to console. """

        if bans:
            print('\n -------------------------  Bans  ------------------------- ')
        else:
            print('\n -------------------------  Picks  ------------------------- ')

        # calculates string lengths for printing
        max_label_len = 7
        max_champ_name_len = len(max([champ_name for _, champ_name, _ in results_array if champ_name is not None], key=len))
        max_accuracy_len = 2

        team_zip = zip(results_array[:5], results_array[5:])

        for result in team_zip:
            b_label, b_champ, b_match = result[0]
            r_label, r_champ, r_match = result[1]

            if b_champ is None:
                b_champ = ''
            if r_champ is None:
                r_champ = ''

            print(
                f'{b_label.ljust(max_label_len)}   '
                f'{b_champ.ljust(max_champ_name_len)}   '
                f'{str(b_match).zfill(max_accuracy_len).ljust(max_accuracy_len)}'
                f'   |   '
                f'{str(r_match).zfill(max_accuracy_len).rjust(max_accuracy_len)}   '
                f'{r_champ.rjust(max_champ_name_len)}   '
                f'{r_label.rjust(max_label_len)}'
            )


    """ CHAMPLIST """

    def import_champlist(self):
        """ Imports champlist from file. """

        with open(self.champlist_path, 'r') as f:
            return [name.strip() for name in f]