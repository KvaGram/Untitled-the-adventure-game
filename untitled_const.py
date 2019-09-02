#sonstants for Untitled! The adventure game and text editor

ENTRY_NAME_PATTERN = r'^[A-Z]+(?:[0-9]|_|[A-Z])*$'
ITEM_NAME_PATTERN = r'^[A-Z]+(?:[0-9]|_|[A-Z])*$'
SEPERATOR = "_"

FALLBACK_ICON = "empty.gif"
IMAGE_DIR = "images/"

DATATERM_ITEM = "ITEM"

DATATERM_NAME = "_NAME"
DATATERM_DESCRIPTION = "_DESC"
DATATERM_ICON = "_ICON"

class ReturnToMain(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class ReturnToTitle(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)