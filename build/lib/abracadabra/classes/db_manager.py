from tinydb import TinyDB, where, Query

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

    def insert_fingerprint(self, fingerprints):
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

    def insert_song_info(self, song, id):
        self.song_info.insert({'song': song, 'id': id})

    def get_song_info(self, id):
        info = self.song_info.search(Query().id == id)
        return info['song']

    def get_matches(self, hashes):
        h_dict = {}
        for h, t, _ in hashes:
            h_dict[h] = t
        in_values = f"({','.join([str(h[0]) for h in hashes])})"
        self.table.search(where('hash') )
        result_dict = defaultdict(list)
        for r in results:
            result_dict[r[2]].append((r[1], h_dict[r[0]]))
        return result_dict

