# SimpleDB [Python]
Simple JSON database.

## Example
```py
from main import DB
db = DB({
    "filename": "db.json",
    "name": "users"
})
user = {}
if len(db.search({ "id": 1 })) == 0:
    user = db.new({
        "id": 1,
        "name": "Denis",
        "lastname": "Stasov",
        "phonenumber": "89275714852",
        "activated": True
    })
    db.write()

user["name"] = "Vlad";
db.write()
```
## Need to work:
* ``json`` module only.

## Functions
* Retrieving all entrys.
```py
db.get() # [{...}]
```
* Searching entry by JSON or function
```py
db.search({ "name": "Vlad", "lastname": "Stasov" }) # Example of searching. [{ "id": 1, "name": "Vlad", "lastname": "Stasov" ... }]
```
* Writing any changes. (Must be used after every post DB request, like as db.new() or db.clear())
```py
user["password"] = "secretPass<3"
db.write() # True
```
* Adding entry.
```py
db.new({
    "id": 2,
    "name": "Ivan",
    "lastname": "Ivanov",
    "phonenumber": "89276518535",
    "activated": False
}) # { "id": 2, "name": "Ivan", "lastname": "Ivanov" }
```
* Removing entry by key.
```py
db.remove({ "id": 2 }) # True
```
* Add some values to all entries if they don't have this value.
```py
db.include({
    "discord": "",
    "minecraft": ""
}) # { "discord": 2, "minecraft": 2 }
```
* Clear DB.
```py
db.clear() # True
```
* Add some values to all entries with some key if they don't have this value.
```py
db.includeKey({
    "activated": True
}, {
    "twitch": ""
}) # { "twitch": 1 }
```

## Some author words
### I do not recommend this database for large projects. Better use MySQL, MongoDB, etc.