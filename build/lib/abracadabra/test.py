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
#print("compare function")

#db_manager.insert({'name': 'test_cpy.wav', 'hash': fp.fingerprint_file("../../../Samples/test.wav")})

fingerprint_ = fp.fingerprint_file("../../../Samples/test.wav")


matches = db_manager.get_all() ## braucht man das ???
        #return_data = Recogniser.score_match(matches)
return_data = recogniser_class_.recognise_song("../../../Samples/test.wav")
#data = recogniser_class_.compare()
#print(data)