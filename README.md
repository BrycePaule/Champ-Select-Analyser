# Champ-Select-Analyser

Champ-Select-Analyser is a command line tool used to turn LCK Champion select screenshots into digestable draft tables with respect to pick and ban order.

<br>

CSA has 3 major functions:
- Web scraping and updating most recent champion list + champion splash arts
- Slightly edits and optmises the raw splashes to be more usable, both for accuracy and speed
- Template matching champ selects against those criteria for data collection

<br>

<b> Usage: </b> 
<br>
Default usage (no arguments) runs all 3 major functions (scrape, edit and match)

`-d` or `-download` downloads champlist + splash arts <br>
`-e` or `-edit` edits splashes for usability <br>
`-nm` or `-nomatch` omits template matching (just downloads champlist and/or edits splashes) <br>
`-a` or `-all` allows matching of multiple champselects (all in given directory) as opposed to a single screenshot <br>

You will be prompted to provide google sheet information on launch, if left blank it still run without trying to output results externally.
