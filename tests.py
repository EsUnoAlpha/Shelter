import unittest
from flask_testing import TestCase
from main import app, db, create_pet, get_all_pets, delete_pet


class MyAppTests(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_pet(self):
        create_pet(name='TestPet', image='test.jpg', description='Test Description', age=2, pet_type='Кошечка')
        pets = get_all_pets()
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].name, 'TestPet')

    def test_delete_pet(self):
        create_pet(name='TestPet', image='test.jpg', description='Test Description', age=2, pet_type='Собачка')
        pets_before = get_all_pets()
        delete_pet(pets_before[0].id)
        pets_after = get_all_pets()
        self.assertEqual(len(pets_after), 0)

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
