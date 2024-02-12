from tinydb import Query
import fingerprint as fp
from classes.db_manager import DataBaseManager

print(fp.fingerprint_file("../../../Samples/test.wav"))

query = Query()

db_manager = DataBaseManager()
db_manager.insert({'name': 'test.wav', 'hash': fp.fingerprint_file("../../../Samples/test.wav")})
db_manager.table.remove()