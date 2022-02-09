from errors import DBError, ParamError
import json
class DB:
    def __init__(self, params: dict):
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
        file = open(self.filename, "w+")
        file.write(json.dumps(self.db, indent=4))
        return True

    def get(self):
        return self.db[self.name]

    def search(self, params: dict):
        if params == None:
            raise ParamError("No params!")

        database = DB.get(self)

        for i in params.keys():
            database = [d for d in database if d[i] is params[i]]

        return database

    def new(self, json: dict):
        if type(json) is not dict:
            raise ParamError("No JSON introduced!")

        self.db[self.name].append(json)
        return json

    def remove(self, params):
        if params == None:
            raise ParamError("No params!")
        
        result = DB.search(self, params)

        if len(result) == 0:
            raise DBError("Not found!")
        
        self.db[self.name] = [d for d in self.db[self.name] if d not in result]
        return True

    def clear(self):
        self.db[self.name] = []
        return True
    
    def include(self, values: dict):
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
