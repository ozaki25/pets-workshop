import unittest
from unittest.mock import patch, MagicMock
import json
from app import app  # Changed from relative import to absolute import
from models.dog import validate_dog_age

# filepath: server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    def _create_mock_dog(self, dog_id, name, breed):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_success(self, mock_query):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        dog1 = self._create_mock_dog(1, "Buddy", "Labrador")
        dog2 = self._create_mock_dog(2, "Max", "German Shepherd")
        mock_dogs = [dog1, dog2]
        
        self._setup_query_mock(mock_query, mock_dogs)
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        # Verify first dog
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['name'], "Buddy")
        self.assertEqual(data[0]['breed'], "Labrador")
        
        # Verify second dog
        self.assertEqual(data[1]['id'], 2)
        self.assertEqual(data[1]['name'], "Max")
        self.assertEqual(data[1]['breed'], "German Shepherd")
        
        # Verify query was called
        mock_query.assert_called_once()
        
    @patch('app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        # Arrange
        self._setup_query_mock(mock_query, [])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
        
    @patch('app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        # Arrange
        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        self._setup_query_mock(mock_query, [dog])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {'id', 'name', 'breed'})


class TestDogAgeValidation(unittest.TestCase):
    """犬の年齢検証関数のテストクラス"""
    
    def test_valid_age_zero(self):
        """0歳は有効であること"""
        result = validate_dog_age(0)
        self.assertEqual(result, 0)
    
    def test_valid_age_twenty(self):
        """20歳は有効であること"""
        result = validate_dog_age(20)
        self.assertEqual(result, 20)
    
    def test_valid_age_middle_range(self):
        """範囲内の年齢（5歳）は有効であること"""
        result = validate_dog_age(5)
        self.assertEqual(result, 5)
    
    def test_invalid_age_negative(self):
        """負の年齢は無効でエラーをスローすること"""
        with self.assertRaises(ValueError) as context:
            validate_dog_age(-1)
        self.assertIn("must be between 0 and 20 years", str(context.exception))
    
    def test_invalid_age_too_high(self):
        """21歳以上は無効でエラーをスローすること"""
        with self.assertRaises(ValueError) as context:
            validate_dog_age(21)
        self.assertIn("must be between 0 and 20 years", str(context.exception))
    
    def test_invalid_age_none(self):
        """None値は無効でエラーをスローすること"""
        with self.assertRaises(ValueError) as context:
            validate_dog_age(None)
        self.assertIn("Age cannot be None", str(context.exception))
    
    def test_invalid_age_string(self):
        """文字列は無効でエラーをスローすること"""
        with self.assertRaises(ValueError) as context:
            validate_dog_age("5")
        self.assertIn("Age must be an integer", str(context.exception))
    
    def test_invalid_age_float(self):
        """小数は無効でエラーをスローすること"""
        with self.assertRaises(ValueError) as context:
            validate_dog_age(5.5)
        self.assertIn("Age must be an integer", str(context.exception))


if __name__ == '__main__':
    unittest.main()