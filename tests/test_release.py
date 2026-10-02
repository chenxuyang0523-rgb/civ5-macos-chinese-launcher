import unittest

from tools.check_release import audit_file


class ReleaseAuditTests(unittest.TestCase):
    def test_reject_game_database_even_if_text(self):
        self.assertTrue(audit_file("cache/Localization.db", b"fixture"))

    def test_reject_binary_in_allowlisted_file(self):
        self.assertTrue(audit_file("README.md", bytes([255, 254, 0])))

    def test_detect_personal_path_and_account_id(self):
        private = ("/Users/" + "example/Library/ " + "7656119" + "1234567890").encode()
        self.assertEqual(len(audit_file("README.md", private)), 2)

    def test_clean_source(self):
        self.assertEqual(audit_file("README.md", b"Public project description."), [])


if __name__ == "__main__":
    unittest.main()
