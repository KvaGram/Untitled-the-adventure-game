from untitled_const import DATATERM_ITEM, DATATERM_NAME, DATATERM_DESCRIPTION, DATATERM_ICON

class _ItemDB(object):
    _ITEMS = []
    def __new__(cls, name:str, dName:str, desc:str, image:str):
        #check first if item already exist.
        #if it does, update the data instead, then return.
        i:_ItemDB = cls.GET(name)
        if i:
            i.dName = dName
            i.desc = desc
            i.image = image
            return i
        i = super().__new__(cls)
        i.name = name
        i.dName = dName
        i.desc = desc
        i.image = image
        cls._ITEMS.append(i)
    #gets a type of item, if it exist
    @classmethod
    def GET(cls, name:str):
        for i in cls._ITEMS:
            if i.name == name:
                return i
        return None
    #removes a type of item, if it exist
    @classmethod
    def DEL(cls, name:str):
        i = cls.GET(name)
        if i:
            cls._ITEMS.remove(i)
            return True
        return False

def SETUP(T:callable, *itemkey:str):
    items = []
    for i in itemkey:
        n_key = f"{DATATERM_ITEM}_{i}{DATATERM_NAME}"
        d_key = f"{DATATERM_ITEM}_{i}{DATATERM_DESCRIPTION}"
        i_key = f"{DATATERM_ITEM}_{i}{DATATERM_ICON}"
        items.append(_ItemDB(i, T(n_key), T(d_key), T(i_key)))
    pass

#wrapper for _ItemDB.__new__
def SET(name:str, displayname:str, desc:str, image:str)->_ItemDB:
    return _ItemDB(name, displayname, desc, image)
#wrapper for _ItemDB.GET
def GET(name:str):
    return _ItemDB.GET(name)
#wrapper for _itemDB.DEL
def DEL(name:str):
    return _ItemDB.DEL(name)