# Champ-Select-Analyser

A command line tool (CLI) to parse LCK champion select / draft screenshots into human-readable draft tables.

i.e. converts this:

<img src='.\ReadMe\DraftMarkup.jpg' height=200> 

into this:

<img src='.\ReadMe\OutputExample.jpg' height=200>


## Functionality
- A web scraper that:
    - scrapes the most recent `champion list` (i.e. automatically updates for new champion releases)
    - scrapes champion `splash arts` and `icons` to match against broadcast graphics
- Transforms scraped images to optimise for parse-time
- Parses draft screenshots and outputs pick/ban tables to either `console` or `google sheets`


## Usage:

Default usage `python ./main.py`:
- Don't scrape for updates
- Don't edit local splash art or icons
- Parse the latest (alphabetically by name) screenshot in the directory

| Argument | Description |
| ------------- | ------------- |
| `-s` or `-scrape`  | - Lazily run the web scraper for champion names, splashes, and icons (i.e. **only downloading missing data**)  |
| `-fs` or `-force_scrape`  | - Forcefully run the scraper for champion names, splash arts and icons (i.e. **overriding local data**) |
| `-o` or `-optimise`  | - Edit champion splash arts and icons to improve parse-speed and accuracy |
| `-np` or `-no_parse`  | - Don't run the parser |
| `-a` or `-all`  | - Parse all screenshots in the directory, rather than the latest |
