#!D:\banruo\venv1\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'html2text==2016.9.19','console_scripts','html2text'
__requires__ = 'html2text==2016.9.19'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('html2text==2016.9.19', 'console_scripts', 'html2text')()
    )
