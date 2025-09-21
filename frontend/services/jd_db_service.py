
import json
import os

class JsonDbService:
    def __init__(self, db_path='db.json'):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path)
        self.initialize_db()

    def initialize_db(self):
        """Initialize JSON DB if it doesn't exist"""
        if not os.path.exists(self.db_path):
            initial_data = {
                "classes": [],
                "classworks": [],
                "stream_posts": []
            }
            with open(self.db_path, 'w') as f:
                json.dump(initial_data, f, indent=2)

    def read_db(self):
        """Read data from JSON DB"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.initialize_db()
            return self.read_db()

    def write_db(self, data):
        """Write data to JSON DB"""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
