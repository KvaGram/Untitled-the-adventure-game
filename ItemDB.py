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

#wrapper for _ItemDB.__new__
def SET(name:str, displayname:str, desc:str, image:str)->_ItemDB:
    return _ItemDB(name, displayname, desc, image)
#wrapper for _ItemDB.GET
def GET(name:str):
    return _ItemDB.GET(name)
#wrapper for _itemDB.DEL
def DEL(name:str):
    return _ItemDB.DEL(name)