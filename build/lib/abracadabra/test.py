from tinydb import Query
import fingerprint as fp
from classes.db_manager import DataBaseManager
from classes.recogniser_class import Recogniser
print(fp.fingerprint_file("../../../Samples/test.wav"))

query = Query()

db_manager = DataBaseManager()
db_manager.insert({'name': 'test.wav', 'hash': fp.fingerprint_file("../../../Samples/test.wav")})
#db_manager.table.delete()

recogniser_class_ = Recogniser()
print("compare function")

#db_manager.insert({'name': 'test_cpy.wav', 'hash': fp.fingerprint_file("../../../Samples/test.wav")})

fingerprint_hash = fp.fingerprint_file("../../../Samples/test.wav")

data = recogniser_class_.compare()
print(data)