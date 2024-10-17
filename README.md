# Champ-Select-Analyser

A command line tool (CLI) designed to parse LCK champion select / draft screenshots into human-readable draft tables.

i.e. converts this:

<img src='READMEImages\DraftMarkup.jpg' height=200> 

into this:

<img src='READMEImages\OutputExample.jpg' height=200>


## Functionality
- Web scraper that:
    1. Scrapes the current `champion list` (i.e. automatically handles new champion releases)
    2. Scrapes champion `splash arts` and `icons` to match against broadcast graphics
- Transforms scraped images to optimise for match time
- Parses draft screenshots and outputs to either `console` or a `google sheets`


## Usage:

Default usage `python ./main.py`:
- Will not run the scraper
- Will not edit local splash art or icons
- Will run the parser over the latest (by timestamp) screenshot in the directory


| Argument | Description |
| ------------- | ------------- |
| `-s` or `-scrape`  | - Runs the web scraper for champion names, splashes, and icons <br> - Only downloads missing data  |
| `-fs` or `-force_scrape`  | - Force run the scraper for champion names, splash arts and icons <br> - Overrides all local data |
| `-o` or `-optimise`  | - Edits scraped images to improve parse speed and accuracy |
| `-np` or `-no_parse`  | - Does not run the parser |
| `-a` or `-all`  | - Parses all screenshots in the directory, rather than the latest |
