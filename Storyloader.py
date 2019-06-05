import xml
from xml.etree import cElementTree as ElementTree
import os
import sys

__defaultLang__ = "english"

def load(language:str = __defaultLang__):
    cwd = os.getcwd()
    try: #if True:
        tree = ElementTree.parse(cwd+"/nerrative/" + language + ".xml")
    except Exception as e: #if False:
        if(language == __defaultLang__):
            raise e #If this IS the fallback, well shit, best raise the bug after all then.
        print ("Error loading language file {0}: {1}".format(language, e), file=sys.stderr)
        print ("Attempting to load default languge {0} instead.".format(__defaultLang__), file=sys.stderr)
        return load(__defaultLang__)
    story = Story()
    for element in tree.iter():
        story[element.tag] = element.text.strip()
    return story
class Story(dict):
    def __missing__(self, key):
        return "(("+key+"))"

if __name__ == "__main__":
    story = load()
    print(story)