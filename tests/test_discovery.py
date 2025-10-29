import unittest
from app.discovery import discover_devices

class TestDiscovery(unittest.TestCase):

    def test_discover_devices(self):
        devices = discover_devices()
        self.assertIsInstance(devices, list)
        self.assertGreater(len(devices), 0)

    def test_device_attributes(self):
        devices = discover_devices()
        for device in devices:
            self.assertIn('name', device)
            self.assertIn('ip_address', device)
            self.assertIn('mac_address', device)

    def test_empty_discovery(self):
        devices = discover_devices()
        self.assertEqual(devices, [])

if __name__ == '__main__':
    unittest.main()