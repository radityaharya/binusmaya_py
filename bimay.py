import string
import requests
from dateutil import parser
import time
import datetime
import json


class bimay:
    def __init__(self, roleId, token):
        """
        args:
        -roleId: roleId from bimay
        -token: Bearer token from bimay
        """
        if token.startswith("Bearer "):
            token = token[7:]
        self.headers = {
            "Authorization": "Bearer {}".format(token),
            "institution": "BNS01",
            "Content-Type": "application/json",
            "academicCareer": "RS1",
            "roleId": roleId,
            "Accept": "application/json, text/plain, */*",
            "roleName": "Student",
            "Origin": "https://newbinusmaya.binus.ac.id",
            "Referer": "https://newbinusmaya.binus.ac.id/",
        }
        self.base_url = "https://apim-bm7-prod.azure-api.net"
        self.schedule_base_url = "https://func-bm7-schedule-prod.azurewebsites.net"
        self.r = requests.Session()

    def config(self, dict):
        """
        dict = {

        """
        self.conf = dict

    def __get_data(self, url, json_data=None, params=None, headers=None):
        if headers is None:
            headers = self.headers
        response = self.r.get(url, params=params, json=json_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    def __post_data(self, url, json_data=None, params=None, headers=None):
        if headers is None:
            headers = self.headers
        response = self.r.post(url, params=params, json=json_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    def get_latest_academicPeriod(self):
        url = "{}/func-bm7-course-prod/AcademicPeriod/Student".format(self.base_url)
        response = self.r.get(url, headers=self.headers)
        if response.status_code == 200:
            for academicPeriod in response.json():
                startDate = parser.parse(academicPeriod["termBeginDate"])
                endDate = parser.parse(academicPeriod["termEndDate"])
                if startDate <= datetime.datetime.now() <= endDate:
                    break
            return academicPeriod
        raise Exception(response.text)

    def get_schedule_date(
        self, date_start: datetime.datetime, date_end: datetime.datetime = None
    ):
        """
        --get_schedule_date(date_start, date_end)
        returns: schedule date from date_start to date_end in json format

        or

        --get_schedule_date(date_start)
        returns: schedule date from date to date in json format
        """

        def fetch_schedule(date):
            return self.__post_data(
                "{}/api/schedule/Date-v1/{}".format(
                    self.schedule_base_url, date.strftime("%Y-%-m-%-d")
                ),
                json_data={},
            )

        if date_end is None:
            return fetch_schedule(date_start)
        else:
            schedules = []
            for date in (
                date_start + datetime.timedelta(days=x)
                for x in range(0, (date_end - date_start).days)
            ):
                for i in range(len(fetch_schedule(date)["Schedule"])):
                    schedules.append(fetch_schedule(date)["Schedule"][i])
            first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
            data = {"dateStart": first_date_start, "Schedule": schedules}
            return data

    # dispose this? feels redundant
    def get_schedule_month(self, date: datetime.datetime):
        """
        --get_schedule_month(date)
        returns: schedule date from date to date in json format
        """
        return self.__post_data(
            "{}/api/schedule/Month-v1/{}".format(
                self.schedule_base_url, date.strftime("%Y-%-m-1")
            ),
            json_data={},
        )

    # --ClassComponent-- #
    def get_class_component_list(self, period: int = None):
        """
        -args: period default is current academic period
        -returns: class component list in json format
        """
        if period is None:
            period = self.get_latest_academicPeriod()["academicPeriod"]
        else:
            period = str(period)
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/ClassComponentList/Student"
        )

    # --classes-- #
    def get_class_from_component(
        self, period: int = None, classComponentId: string = None
    ):
        """
        -args: period ("LEC", "LAB", "TUT", etc.) default is current academic period

        -returns: Array of class information dicts [{"classId","classCode","courseName", "courseCode", "lecturers[]", "progressClass", "ssrComponent", "classGroupId"}]
        """
        if period is None:
            period = self.get_latest_academicPeriod()["academicPeriod"]
        else:
            period = str(period)
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/Component/{classComponentId}/Student"
        )

    def get_class_active(self):
        """
        -returns: Array of active classes
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Class/Active/Student"
        )

    # --classSessions-- #
    def __default_classSessionId(self):
        ongoing = self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Ongoing/student"
        )
        upcoming = self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Upcoming/student"
        )
        if ongoing.get("isHasUpcomingClass") is True:
            return upcoming["id"]
        return ongoing["id"]

    def get_class_sessions_from_classId(self, classId: string):
        """
        -args: classId
        -returns: class sessions information from given classId
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Class/{classId}/Student"
        )

    def get_class_session_detail(self, classSessionId: string = None):
        """
        -args: classSessionId | defaults to ongoing / upcoming classSessionId
        -returns: class session detail information from given classSessionId
        """
        if classSessionId is None:
            classSessionId = self.__default_classSessionId()
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/{classSessionId}/Resource/Student"
        )

    # --resource-- #
    def get_resource_from_resource_id(self, resourceId: string = None):
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/Resource/{resourceId}"
        )

    def get_ppt_from_session_id(self, sessionId: string = None):
        """
        args: sessionId
        returns: ppt url (https://databinuscampussolution.blob.core.windows.net/bol/.....)
        """

        def get_source_url(self, resourceId: string):
            """
            -args: resourceId
            """
            url = self.get_resource_from_resource_id(resourceId)["url"]
            if not url.startswith("https://stbm7resourcesprod.blob.core.windows.net"):
                raise Exception("Invalid url")
            response = self.r.get(url)
            if response.status_code == 200:
                return response.headers["x-ms-copy-source"]
            raise Exception(response.text)

        resources = self.get_class_session_detail(sessionId)["resources"]
        for i in range(len(resources)):
            if resources[i]["resourceType"] == "Document":
                return get_source_url(resources[i]["id"])

    # --forum-- #
    def get_forum_latest(self, classId: string = None):
        """
        -args: classId defaults to all active class
        -returns: forum information from given classId
        """
        if classId is None:
            return self.__post_data(
                f"{self.base_url}/func-bm7-forum-prod/Forum/LatestPostForum",
                json_data=self.get_class_active(),
            )
        else:
            return self.__post_data(
                f"{self.base_url}/func-bm7-forum-prod/Forum/LatestPostForum",
                json_data=[{"classId": classId}],
            )

    def get_forum_from_class_id(self, classId: string = None):
        """ """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Forum/Class/{classId}/Student"
        )

    def get_forum_thread(self, classId: string = None, sessionId: string = None):
        """
        args: classId, sessionId
        returns: forum thread information including threadId from given classId and sessionId
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-forum-prod/Thread/Class/{classId}/Session/{sessionId}/Paging/1",
            json_data={"TotalDataPerPage": 100},
        )

    def get_forum_thread_content(self, classId: string = None, threadId: string = None):
        return self.__get_data(
            f"{self.base_url}/func-bm7-forum-prod/Forum/{classId}/Thread/{threadId}",
            params={"originMultiClassId": None},
        )

    def get_forum_thread_comment(self, classId: string = None, threadId: string = None):
        return self.__post_data(
            f"{self.base_url}/func-bm7-forum-prod/Comment/Paging/1",
            json_data={
                "totalDataPerPage": 100,
                "parentId": threadId,
                "sortBy": "LatestPost",
                "forumId": classId,
            },
        )
