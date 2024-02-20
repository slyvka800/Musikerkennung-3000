from tinydb import Query
import fingerprint as fp
from classes.db_manager import DataBaseManager
import storage 

# print(fp.fingerprint_file("../../../Samples/test.wav"))

query = Query()

db_manager = DataBaseManager()

fingerprint = fp.fingerprint_file("../../../Samples/test.wav")
# db_manager.store_song('test.wav', fingerprint)
print(db_manager.get_matches(fingerprint))
