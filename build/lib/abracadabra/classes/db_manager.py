from tinydb import TinyDB, where, Query
from collections import defaultdict

class DataBaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataBaseManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, 'db'):
            self.db = TinyDB("music_hashes.json")
        if not hasattr(self, 'hashes'):
            self.hashes = self.db.table("hashes")
        if not hasattr(self, 'song_info'):
            self.song_info = self.db.table('song_info')

    def store_song(self, new_song_name, new_song_hashes):
        # check if song doesn't exist in db and store it
        id = new_song_hashes[0][2]
        result = self.song_info.search(Query().id == id)
        if len(result) == 0:
            self.__insert_fingerprint(new_song_hashes)
            self.__insert_song_info(new_song_name, id)

    def __insert_fingerprint(self, fingerprints):
        for fingerprint in fingerprints:
            data = {'hash': fingerprint[0], 'timeoffset': fingerprint[1], 'id': fingerprint[2]}
            self.hashes.insert(data)
    
    def get_hash(self, query):
        return self.hashes.search(query)
    
    def get_all_hashes(self):
        return self.hashes.all()
    
    def update_hash(self, query, data):
        self.hashes.update(data, query)

    def delete_hash(self, query):
        self.hashes.remove(query)

    def __insert_song_info(self, song, id):
        self.song_info.insert({'song': song, 'id': id})

    def get_song_info(self, id):
        info = self.song_info.search(Query().id == id)
        return info['song']
    
    def delete_song_id(self, id):
        self.song_info.remove(doc_ids=[id])

    def get_matches(self, new_hashes_data):
        h_dict = {}
        new_hashes = []
        for h, t, _ in new_hashes_data:
            h_dict[h] = t
            new_hashes.append(h)
        
        results = self.hashes.search(Query().hash.one_of(new_hashes))
        result_dict = defaultdict(list)
        for r in results:
            result_dict[r['id']].append((r['timeoffset'], h_dict[r['hash']]))
        return result_dict

