import datetime
import warnings

from binusmayapy.bimay import Bimay
import unittest
import os
from dotenv import load_dotenv

load_dotenv()


SAMPLE_CLASS_ID = os.getenv("SAMPLE_CLASS_ID")
SAMPLE_CLASS_SESSION_ID = os.getenv("SAMPLE_CLASS_SESSION_ID")
SAMPLE_RESOURCE_ID = os.getenv("SAMPLE_RESOURCE_ID")

bm = Bimay(token=os.getenv("BIMAY_TOKEN"))


class testBimay(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def test_get_latest_academicPeriod(self):
        self.assertEqual(type(bm.get_latest_academicPeriod()), dict)

    def test_get_latest_academic_start_end_date(self):
        self.assertEqual(type(bm.get_latest_academic_start_end_date()), tuple)

    def test_get_schedule_date(self):
        self.assertEqual(
            type(
                bm.get_schedule_date(
                    date_start=datetime.datetime.now(),
                    date_end=datetime.datetime.now() + datetime.timedelta(days=14),
                )
            ),
            dict,
        )

    def test_get_schedule_month(self):
        self.assertEqual(
            type(
                bm.get_schedule_month(
                    datetime.datetime.now(),
                    datetime.datetime.now() + datetime.timedelta(days=30),
                )
            ),
            dict,
        )

    def test_get_class_component_list(self):
        self.assertEqual(type(bm.get_class_component_list(2120)), list)

    def test_get_class_from_component(self):
        self.assertEqual(type(bm.get_class_from_component()), list)

    def test_get_class_active(self):
        self.assertEqual(type(bm.get_class_active()), list)

    def test_get_class_sessions_from_class_id(self):
        self.assertEqual(
            type(bm.get_class_sessions_from_class_id(SAMPLE_CLASS_ID)), dict
        )

    def test_get_class_session_detail(self):
        self.assertEqual(
            type(bm.get_class_session_detail(SAMPLE_CLASS_SESSION_ID)), dict
        )

    def test_get_resource_from_resource_id(self):
        self.assertEqual(
            type(bm.get_resource_from_resource_id(SAMPLE_RESOURCE_ID)), dict
        )

    def test_get_ppt_from_session_id(self):
        self.assertIn("https://", bm.get_ppt_from_session_id(SAMPLE_CLASS_SESSION_ID))

    def test_get_forum_latest(self):
        self.assertEqual(type(bm.get_forum_latest(SAMPLE_CLASS_ID)), dict)

    def test_get_forum_from_class_id(self):
        self.assertEqual(type(bm.get_forum_from_class_id(SAMPLE_CLASS_ID)), dict)

    def test_get_forum_thread(self):
        self.assertEqual(type(bm.get_forum_thread()), dict)

    def get_forum_thread_content(self):
        self.assertEqual(type(bm.get_forum_thread_content()), dict)

    def test_get_forum_thread_comment(self):
        self.assertEqual(type(bm.get_forum_thread_comment()), dict)


if __name__ == "__main__":
    unittest.main()
