#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import unittest
from models.engine import db_storage
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os

DBStorage = db_storage.DBStorage

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Remove test environment"""
        del self.db

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        all_objs = self.db.all()
        self.assertEqual(type(all_objs), dict)

    def test_all_with_cls(self):
        """Test that all returns a dictionary for a specific class"""
        obj = State(name="California")
        storage.new(obj)
        storage.save()
        all_states = storage.all(State)
        self.assertEqual(type(all_states), dict)
        self.assertIn(obj, all_states.values())

    def test_get(self):
        """Test the get method"""
        obj = State(name="New York")
        storage.new(obj)
        storage.save()
        state_id = obj.id
        retrieved_state = storage.get(State, state_id)
        self.assertEqual(retrieved_state, obj)

    def test_get_nonexistent_object(self):
        """Test get method with nonexistent object"""
        non_existent_id = "non_existent_id"
        retrieved_obj = storage.get(State, non_existent_id)
        self.assertIsNone(retrieved_obj)

    def test_count(self):
        """Test the count method"""
        initial_count = storage.count()
        obj = State(name="Texas")
        storage.new(obj)
        storage.save()
        new_count = storage.count()
        self.assertEqual(new_count, initial_count + 1)

    def test_count_with_cls(self):
        """Test count method with specific class"""
        initial_count = storage.count(State)
        obj = State(name="Florida")
        storage.new(obj)
        storage.save()
        new_count = storage.count(State)
        self.assertEqual(new_count, initial_count + 1)

    def test_count_nonexistent_class(self):
        """Test count method with nonexistent class"""
        with self.assertRaises(NameError):
            storage.count(NonExistentClass)

if __name__ == '__main__':
    unittest.main()
