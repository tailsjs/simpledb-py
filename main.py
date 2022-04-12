from errors import DBError, ParamError
import json
class DB:
    """
    
    Attributes
    ----------
    params : dict
        DB Params.
    params.filename : str
        DB File.
    params.name : str
        DB Name.

    Methods
    -------
    write()
        Writing changes.
    get()
        Retrieving all entries.
    search(params: dict)
        Searching entry by keys.
    new(json: dict)
        Creating entry.
    remove(params: dict)
        Removing entry by key.
    clear()
        Clear DB.
    include(values: dict)
        Add some values to all entries if they don't have this value.
    includeKey(searchfilter: dict, values: dict)
        Add some values to all entries with some key if they don't have this value.
    """
    def __init__(self, params: dict):
        """ SimpleDB. Hello world! 
        
        Parameters
        ----------
        params : dict
            DB Params.
        params.filename : str
            DB File.
        params.name : str
            DB Name.
        """
        if params == None:
            raise ParamError("No params!")

        if "filename" not in params:
            raise ParamError("No param \"filename\"!")
        
        if "name" not in params: 
            raise ParamError("No param \"name\"!")

        self.filename = params["filename"]
        self.name = params["name"]
        self.db = {}
        file = open(self.filename, "r+").read()
        if file == "":
            self.db[self.name] = []
            file = json.dumps(self.db)
            DB.write(self)
        
        try:
            self.db = json.loads(file)
        except:
            raise DBError('Database broken.')


    def write(self):
        """ Writing changes. """
        file = open(self.filename, "w+")
        file.write(json.dumps(self.db, indent=4))
        return True

    def get(self):
        """ Retrieving all entries. """
        return self.db[self.name]

    def search(self, params: dict):
        """ Searching entry by dict 
        
        Parameters
        ----------
        params : dict
            Search filter.
            """
        if params == None:
            raise ParamError("No params!")

        database = DB.get(self)

        for i in params.keys():
            database = [d for d in database if d[i] is params[i]]

        return database

    def new(self, json: dict):
        """ Creating entry. 
        
        Parameters
        ----------
        json : dict
            Entry, that gonna be added."""
        if type(json) is not dict:
            raise ParamError("No JSON introduced!")

        self.db[self.name].append(json)
        return json

    def remove(self, params: dict):
        """ Removing entry by key. 
        
        Parameters
        ----------
        params : dict
            Search filter.
            """
        if params == None:
            raise ParamError("No params!")
        
        result = DB.search(self, params)

        if len(result) == 0:
            raise DBError("Not found!")
        
        self.db[self.name] = [d for d in self.db[self.name] if d not in result]
        return True

    def clear(self):
        """ Clean DB. """
        self.db[self.name] = []
        return True
    
    def include(self, values: dict):
        """ Add some values to all entries if they don't have this value. 
        
        Parameters
        ----------
        values : dict
            Values, that gonna be included to entry.
        """
        if values == None:
            raise ParamError("No values!")
        
        if type(values) != dict:
            raise ParamError("Type of values must be dict!")

        added = {}

        for entry in self.db[self.name]:
            for value_name in values.keys():
                if value_name not in entry:
                    if value_name not in added:
                        added[value_name] = 0
                    entry[value_name] = values[value_name]
                    added[value_name] += 1

        return added

    def includeKey(self, searchfilter: dict, values: dict):
        """ Add some values to all entries with some key if they don't have this value. 
        
        Parameters
        ----------
        values : dict
            Values, that gonna be included to entry.
        """
        if searchfilter == None:
            raise ParamError("No SearchFilter!")

        if values == None:
            raise ParamError("No values!")

        if type(searchfilter) != dict:
            raise ParamError("Type of searchfilter must be dict!")

        if type(values) != dict:
            raise ParamError("Type of values must be dict!")

        entries = DB.search(self, searchfilter)
        added = {}

        for entry in entries:
            for value_name in values.keys():
                if value_name not in entry:
                    if value_name not in added:
                        added[value_name] = 0
                    entry[value_name] = values[value_name]
                    added[value_name] += 1

        return added
