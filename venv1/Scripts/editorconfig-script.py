#!D:\banruo\venv1\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'EditorConfig==0.12.2','console_scripts','editorconfig'
__requires__ = 'EditorConfig==0.12.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('EditorConfig==0.12.2', 'console_scripts', 'editorconfig')()
    )
