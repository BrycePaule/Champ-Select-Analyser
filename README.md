# Champ-Select-Analyser

Designed for personal use.

Champ-Select-Analyser is a personal tool used to turn LCK Champion select screenshots into google sheet draft tables with respect to pick and ban order.

<br>

Has 3 major functions:
- Scraping and updating most recent champion list + champion splash arts
- Slightly edits the raw splashes to be more usable, both for accuracy and speed
- Template matching champ selects against those criteria

<br>

<b> Use: </b> 
<br>
Default use runs all 3 major functions (scrape, edit and match)

`-d` or `-download` downloads champlist + splash arts <br>
`-e` or `-edit` edits splashes for usability <br>
`-nm` or `-nomatch` omits template matching (just downloads and/or edits) <br>
`-a` or `-all` allows matching of multiple champselects (all in given directory) <br>

You will be prompted to provide google sheet information on launch, if left blank it still run without trying to output results externally.
