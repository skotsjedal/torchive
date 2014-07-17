Tool for managing downloaded archives
* extract/copy to ready directory
* move to a done directory
* delete from download directory

Error handling responses and respective js isn't entirely correct atm

Legend:
* Blue - extracted/copied
* Purple - moved to done folder
* Green - Command succeeded (copy/extract etc)
* Orange - Command in progress, waiting for response
* Red - Command failed

Install:
copy localsettings.py.bak to localsettings.py and edit

Dependencies:
* flask
* enzyme
* rarfile
* reparse
* python-yaml
* pytest
