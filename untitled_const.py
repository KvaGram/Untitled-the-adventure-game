#constants for Untitled! The adventure game and text editor
import sys
import os
import math

ENTRY_NAME_PATTERN = r'^[A-Z]+(?:[0-9]|_|[A-Z])*$'
ITEM_NAME_PATTERN = r'^[A-Z]+(?:[0-9]|_|[A-Z])*$'
SEPERATOR = "_"

FALLBACK_ICON = "empty.gif"

#bizarro windows world...
if sys.platform.startswith("win"):
    IMAGE_DIR = "images\\"
    SAVE_DIR = "saves\\"
else: # or normal?
    IMAGE_DIR = "images/"
    SAVE_DIR = "saves/"
SAVE_FILETYPE = ".uagsave"

DATATERM_ITEM = "ITEM"

DATATERM_NAME = "_NAME"
DATATERM_DESCRIPTION = "_DESC"
DATATERM_ICON = "_ICON"

DEFALT_BACK_IMG = os.path.join(IMAGE_DIR, "mapB.png")
DEFAULT_LIT_IMG  = os.path.join(IMAGE_DIR, "InnerB.png")
DEFAULT_DOT_IMG = os.path.join(IMAGE_DIR, "dot.png")
UNKNOWN_IMG = os.path.join(IMAGE_DIR, "mapc.png")
DEFAULT_MAP_SIZE = (200, 200)
DEFAULT_DOT_SIZE = (20, 20)

TAU = math.pi * 2

class ReturnToMain(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class ReturnToTitle(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)