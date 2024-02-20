from tinydb import Query
from classes.fingerprint_class import Fingerprinting
from classes.db_manager import DataBaseManager
import storage 
from classes.recogniser_class import Recogniser

# print(fp.fingerprint_file("../../../Samples/test.wav"))

query = Query()

db_manager = DataBaseManager()

# fingerprint = Fingerprinting.fingerprint_file("../../../Samples/337146__erokia__timelift-rhodes-piano.wav")
# db_manager.store_song('337146__erokia__timelift-rhodes-piano.wav', fingerprint)

recogniser = Recogniser()
print(recogniser.recognise_song("../../../Samples/336858__mattc90__matts-emotional-ambient-synthscape-100-bpm.wav"))