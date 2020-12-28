import os

class AccuracyManager:

    """
    Handles tracking the TemplateMatchers accuracy.  Useful in determining
    whether specific splashes or icons need to be edited in any way to make
    more consistent / faster.
    """

    def __init__(self):
        self.accuracy_filepath_picks = f'{os.getcwd()}/Accuracy/accuracy_splash.txt/'
        self.accuracy_filepath_bans = f'{os.getcwd()}/Accuracy/accuracy_icons.txt/'

        self.champlist_path = f'{os.getcwd()}/champlist.txt/'
        self.champlist = self.import_champlist()

        self.low_accuracy_threshold_picks = 10
        self.low_accuracy_threshold_bans = 10


    def update_accuracy_file(self, match_results, bans=False):
        """
        Updates accuracy trackers

        Creates a dictionary of each champ accuracy from file, checks the
        most recent match results against it, updates if it's better.

        Then runs through the dictionary and printing the result back to file.
        """

        if bans:
            accuracy_filepath = self.accuracy_filepath_bans
        else:
            accuracy_filepath = self.accuracy_filepath_picks

        if not os.path.isfile(accuracy_filepath):
            self.create_default_accuracy_file(bans=bans)

        with open(accuracy_filepath, 'r') as f:
            stored_accuracy = {champ_name: int(accuracy) for (champ_name, accuracy) in [line.strip().split(' ') for line in f]}

        for _, champ_name, match_accuracy in match_results:
            if champ_name is None:
                continue
            if stored_accuracy[champ_name] < match_accuracy:
                stored_accuracy[champ_name] = match_accuracy

        with open(accuracy_filepath, 'w') as f:
            for champ_name, accuracy in stored_accuracy.items():
                f.write(f'{champ_name} {accuracy}\n')


    def create_default_accuracy_file(self, bans=False):
        """ Creates a default accuracy file """

        if bans:
            accuracy_filepath = self.accuracy_filepath_bans
        else:
            accuracy_filepath = self.accuracy_filepath_picks

        with open(accuracy_filepath, 'w') as f:
            for name in self.champlist:
                f.write(f'{name} 0\n')


    def print_unknown_accuracy(self, bans=False):
        """ Prints a list of champs with unknown accuracy to console.  """

        if bans:
            accuracy_filepath = self.accuracy_filepath_bans
        else:
            accuracy_filepath = self.accuracy_filepath_picks

        with open(accuracy_filepath, 'r') as f:
            unknowns = []
            for line in f:
                champ_name, match_count = line.strip().split(' ')
                if int(match_count) == 0:
                    unknowns.append(champ_name)

        print('List champs with unknown accuracy:')

        for champ_name in unknowns:
            print(champ_name)

        print(f'\nTotal: {len(unknowns)} champs with unknown accuracy')


    def print_low_accuracy(self, bans=False):
        """ Prints a list of champs with low accuracy to console.  """

        if bans:
            accuracy_filepath = self.accuracy_filepath_bans
            threshold = self.low_accuracy_threshold_bans
        else:
            accuracy_filepath = self.accuracy_filepath_picks
            threshold = self.low_accuracy_threshold_picks

        with open(accuracy_filepath, 'r') as f:
            lows = []
            for line in f:
                champ_name, match_count = line.strip().split(' ')
                if int(match_count) < threshold:
                    lows.append([champ_name, match_count])

        print('List of champs with low accuracy:')

        for champ_name, match_count in lows:
            print(f'{champ_name} {match_count}')

        print(f'\nTotal: {len(lows)} champs with low accuracy')


    def import_champlist(self):
        """ Imports champlist from file. """

        with open(self.champlist_path, 'r') as f:
            return [name.strip() for name in f]
