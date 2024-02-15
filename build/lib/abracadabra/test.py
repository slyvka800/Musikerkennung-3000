from tinydb import Query
import fingerprint as fp
from classes.db_manager import DataBaseManager
import storage 

# print(fp.fingerprint_file("../../../Samples/test.wav"))

query = Query()

db_manager = DataBaseManager()
# db_manager.insert({'name': 'test.wav', 'hash': fp.fingerprint_file("../../../Samples/test.wav")})
# db_manager.delete(query.name == 'test.wav')
fingerprint = fp.fingerprint_file("../../../Samples/test.wav")
db_manager.insert_fingerprint(fingerprint)
db_manager.insert_song_info('test.wav', fingerprint[0][2])
