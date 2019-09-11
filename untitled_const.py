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

DEFAULT_MAP_SIZE = (200, 200)
DEFAULT_DOT_SIZE = (10, 10)

TAU = math.pi * 2

NAV_LIT_CORE     = os.path.join(IMAGE_DIR, "Core.png")
NAV_LIT_INNER_A  = os.path.join(IMAGE_DIR, "InnerA.png")
NAV_LIT_INNER_B  = os.path.join(IMAGE_DIR, "InnerB.png")
NAV_LIT_MIDDLE_A = os.path.join(IMAGE_DIR, "MiddleA.png")
NAV_LIT_MIDDLE_B = os.path.join(IMAGE_DIR, "MiddleB.png")
NAV_LIT_OUTER_A  = os.path.join(IMAGE_DIR, "OuterA.png")
NAV_LIT_OUTER_B  = os.path.join(IMAGE_DIR, "OuterB.png")

NAV_BACK_UNKNOWN = os.path.join(IMAGE_DIR, "mapA.png") 
NAV_BACK_INTACT  = os.path.join(IMAGE_DIR, "mapB.png") 
NAV_BACK_BROKEN  = os.path.join(IMAGE_DIR, "mapC.png")

NAV_DOT          = os.path.join(IMAGE_DIR, "dot.png")



class ReturnToMain(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class ReturnToTitle(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)