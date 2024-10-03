from django.test import TestCase
from django.urls import reverse
from io import StringIO

sample_yaml = """
unit testing:
  dates:
  - 2024-09-15
  - 2024-07-26
  period: 6w
integration testing:
  dates:
  - 2024-09-17
  - 2024-08-14
  - 2024-07-14
  period: 4w
tinkering with vim config:
  dates:
  - 2023-09-13
  - 2023-02-05
  - 2022-05-18
  - 2020-12-28
  period: 1d
"""

sample_yaml_with_mismatch = """
unit testing:
  dates:
  - 2024-09-15
  - 2024-07-26
  period: 6w
integration testing:
  dates:
  - 2024-09-17
  - 2024-08-14
  - 2024-07-14
  period: 4w
tinkering with vim config:
  dates:
  - 2023-09-13
  - 2023-02-05
  - 2022-05-18
  - 2020-12-28
  period: 2d
"""
sample_yaml_with_bad_period = """
tinkering with vim config:
  dates:
  - 2020-12-28
  period: 20Hz
"""


class TestUploadYaml(TestCase):
    def setUp(self):
        self.client.login(username="testuser", password="2137")

    def post_a_string(self, s):
        self.client.post(reverse("dashboard:upload_yaml"), {"file": StringIO(s)})

    def test_yaml_upload(self):
        self.post_a_string(sample_yaml)

    def test_yaml_upload_twice(self):
        self.post_a_string(sample_yaml)

    def test_yaml_upload_with_mismatch(self):
        with self.assertRaises(ValueError):
            for string in [sample_yaml, sample_yaml_with_mismatch]:
                self.post_a_string(string)

    def test_yaml_upload_with_malformed_input(self):
        with self.assertRaises(AttributeError):
            self.post_a_string("But every test crashed when the Fire Nation attacked.")

    def test_yaml_upload_with_bad_period(self):
        with self.assertRaises(ValueError):
            self.post_a_string(sample_yaml_with_bad_period)

    def test_yaml_upload_without_file(self):
        self.client.post(reverse("dashboard:upload_yaml"))

    def test_yaml_upload_get(self):
        self.client.get(reverse("dashboard:upload_yaml"))
