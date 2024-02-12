import fingerprint as fp
from classes.db_manager import DataBaseManager

print(fp.fingerprint_file("../../../Samples/test.wav"))

db_manager = DataBaseManager()
db_manager.insert({"test.wav": fp.fingerprint_file("../../../Samples/test.wav")})