import re
import json
from pathlib import Path
from typing import Union


doublespace_pattern = re.compile("\s+")
lineseparator_pattern = re.compile("\n+")

def normalize_text(string: str) -> str:
    string = string.replace('\t', ' ')
    string = string.replace('\r', ' ')
    string = lineseparator_pattern.sub('\n', string)
    string = doublespace_pattern.sub(' ', string)
    return string.strip()



#TODO: Add Config - yaml or json ..