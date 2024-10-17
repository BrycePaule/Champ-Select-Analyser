import os
import numpy as np
import cv2 as cv
import Utils

from AccuracyManager import AccuracyManager
from TemplateCropper import TemplateCropper
from collections import namedtuple
from DRAFT_SLOTS import SLOT_COORDS


Match = namedtuple('match', ['champion', 'match_count'])


class TemplateMatcher:

    def __init__(self, attempts):
        self.champlist = Utils.read_champlist_from_file()

        self.attempts = attempts
        self.ban_accuracy_threshold = 0.70
        self.pick_accuracy_threshold = 0.90

        self.cropper = TemplateCropper()
        self.champ_select_slots = SLOT_COORDS.keys()


    """ TEMPLATE MATCHING """

    def get_draft_screenshot(self, all_templates=False):
        screenshots = [f for f in os.listdir(Utils.path_draft_screenshots) if f.endswith(".bmp")]

        if all_templates:
            return screenshots

        return screenshots[-1:]


    def parse(self, draft_filename):
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
        results = {}

        for slot in self.champ_select_slots:

            # if bans
            if len(slot) == 3:
                match_accuracy_threshold = self.ban_accuracy_threshold
                image_filepath = Utils.path_icons
            # if picks
            else:
                match_accuracy_threshold = self.pick_accuracy_threshold
                image_filepath = Utils.path_splashes


            for i in range(self.attempts * 2 + 1): # *2 for attempted resize up + down, offset to count from 1
                slot_to_parse = self.cropper.crop_draft_slot(draft_filename, slot, i)
                match_found = False

                print(f'Parsing [{slot}]: attempt {i + 1}')

                for champion in self.champlist:
                    champ_image_default = cv.imread(f'{image_filepath}{champion}.bmp', 0)
                    champ_image_invert = cv.imread(f'{image_filepath}{champion}_inverted.bmp', 0)

                    count_matches_default = self.template_match(champ_image_default, slot_to_parse, match_accuracy_threshold)
                    count_matches_invert = self.template_match(champ_image_invert, slot_to_parse, match_accuracy_threshold)

                    best_match = max(count_matches_default, count_matches_invert)

                    if best_match > 0:
                        results[slot] = Match(champion, best_match)
                        match_found = True

                        Utils.print_indented(f'Match found -- {champion} ({best_match})')
                        break

                if match_found:
                    break

            if not match_found:
                results[slot] = Match(None, 0)

        return results


    def template_match(self, champ_to_compare, img_to_parse, accuracy_threshold):
        # Attempt to match `champ_to_compare` to `img_to_parse` using Template Matching

        results = cv.matchTemplate(champ_to_compare, img_to_parse, cv.TM_CCOEFF_NORMED)

        reasonable_matches = np.where(results >= accuracy_threshold)
        match_count = np.count_nonzero(reasonable_matches) // 2 # halved as double counting both x and y coords, meaning two non-zeros = one match

        return match_count


    def clear_stored_results(self):
        previous_results = [f for f in os.listdir(Utils.path_results) if f.endswith(".bmp")]

        for f in previous_results:
            os.remove(os.path.join(Utils.path_results, f))


    def update_accuracy(self, results, bans=False):
        accuracy_manager = AccuracyManager()
        accuracy_manager.update_accuracy_file(results, bans)


    def print_results(self, results):
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
            b_pick = f'{blue_champ.ljust(max_champ_name_len)} {str(blue_accuracy).ljust(3)}'
            r_pick = f'{str(red_accuracy).ljust(3)}  {red_champ.ljust(max_champ_name_len)}'
            print(f'{b_pick}     |     {r_pick}')

        print('\n -----------  Picks  ----------- ')
        for row in picks:
            blue_champ, blue_accuracy = row[0][0], row[0][1]
            red_champ, red_accuracy = row[1][0], row[1][1]
            b_pick = f'{blue_champ.ljust(max_champ_name_len)} {str(blue_accuracy).ljust(3)}'
            r_pick = f'{str(red_accuracy).ljust(3)}  {red_champ.ljust(max_champ_name_len)}'
            print(f'{b_pick}     |     {r_pick}')
