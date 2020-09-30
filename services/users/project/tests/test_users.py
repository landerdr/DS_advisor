# services/users/project/tests/test_users.py

import json
import unittest

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the User Service."""

    def test_users(self):
        """Ensure the /ping route behaves properly"""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])


if __name__ == "__main__":
    unittest.main()
