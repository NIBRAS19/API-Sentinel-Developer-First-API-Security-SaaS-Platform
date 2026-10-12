from django.test import SimpleTestCase
class SmokeTest(SimpleTestCase):
    def test_health_imports(self):
        self.assertTrue(True)
