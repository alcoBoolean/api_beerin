# import unittest
# import requests
#
# BASE_URL = "http://127.0.0.1:8000"  # Адрес вашего API
#
# class TestAPI(unittest.TestCase):
#     def test_get_items(self):
#         """Тест получения всех элементов"""
#         response = requests.get(f"{BASE_URL}/items/")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("items", response.json())
#
#     def test_get_item(self):
#         """Тест получения элемента по ID"""
#         response = requests.get(f"{BASE_URL}/items/1")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"name": "item1", "price": 100})
#
#         response = requests.get(f"{BASE_URL}/items/999")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"error": "Item not found"})
#
#     def test_add_item(self):
#         """Тест добавления нового элемента"""
#         payload = {"item_id": "3", "name": "item3", "price": 300}
#         response = requests.post(f"{BASE_URL}/items/", params=payload)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["message"], "Item added")
#
#         # Проверяем, что элемент действительно добавлен
#         response = requests.get(f"{BASE_URL}/items/3")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"name": "item3", "price": 300})
#
#     def test_delete_item(self):
#         """Тест удаления элемента"""
#         response = requests.delete(f"{BASE_URL}/items/3")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["message"], "Item deleted")
#
#         # Проверяем, что элемент действительно удален
#         response = requests.get(f"{BASE_URL}/items/3")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"error": "Item not found"})
#
#
# if __name__ == "__main__":
#     # unittest.main()
#
import DbWorker

db = DbWorker.DbWorker()
# print(db.get_list_of_posts())
# print(db.add_user_like("admin", "admin", "favorites", "item_id", 2))
# print(db.__add_user_like("admin", "admin", "post_likes", "post_id", 2))
print(db.get_user_friend_info("admin", "admin", 4))
