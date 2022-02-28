import string
import requests
import time
import datetime
import json


class bimay:
    """
    Attributes
    ----------
    roleId : str
        roleId from bimay
    token : str
        Bearer token from bimay

    Methods
    -------

    --schedule--

    get_latest_academicPeriod()
        returns: latest academic period

    get_schedule_date(date_start, date_end)
        returns: schedule date from date_start to date_end

    get_schedule_month(date)
        returns: schedule date from date to date

    get_class_component_list(period)
        returns: class component list

    get_class_from_component(period, classComponentId)
        returns: Array of class information dicts [{"classId","classCode","courseName", "courseCode", "lecturers[]", "progressClass", "ssrComponent", "classGroupId"}]

    get_class_active()
        returns: Array of active classes

    --classSessions--

    get_class_session_from_class_id(classId)
        returns: class session information from given classId

    get_class_session_detail(classSessionId)
        returns: class session detail information from given classSessionId (defaults to ongoing/upcoming class session)

    --resources--

    get_resource_from_resource_id(resourceId)
        returns: resource information from given resourceId

    get_ppt_from_session_id(classSessionId)
        returns: ppt direct link from given classSessionId

    --forum--

    get_forum_latest(classId)
        returns: latest forum information from given classId (defaults to all active classId)

    get_forum_from_class_id(classId)
        returns: forum informations from given classId

    get_forum_thread(classId, sessionId)
        returns: forum thread information including threadId from given classId and sessionId

    get_forum_thread_content(classId, threadId)
        returns: forum thread content information from given classId and threadId (defaults to latest thread)

    get_forum_thread_comment(classId, threadId)
        returns: forum thread comment information from given classId and threadId (defaults to latest thread)
    """

    def __init__(self, roleId, token):
        """
        Description
        ----------
        constructs bimay object

        Parameters
        ----------
        roleId : str mandatory
            roleId from bimay

        token : str mandatory
            Bearer token from bimay

        Returns
        -------
        None
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

    def __get_data(self, url, json_data=None, params=None, headers=None) -> dict:
        """
        Description
        ----------
        creates a get request to given url with given json_data and headers

        Parameters
        ----------
        url : str mandatory
            url to get data from

        json_data : dict optional
            json data to be sent to url

        params : dict optional
            params to be sent to url

        Returns
        -------
        response.json()
        """
        if headers is None:
            headers = self.headers
        response = self.r.get(url, params=params, json=json_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 204:
            raise Exception("No Content")
        raise Exception(response.status_code, response.text)

    def __post_data(self, url, json_data=None, params=None, headers=None) -> dict:
        """
        Description
        ----------
        creates a post request to given url with given json_data and headers

        Parameters
        ----------
        url : str mandatory
            url to get data from

        json_data : dict optional
            json data to be sent to url

        params : dict optional
            params to be sent to url

        Returns
        -------
        response.json()
        """
        if headers is None:
            headers = self.headers
        response = self.r.post(url, params=params, json=json_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 204:
            raise Exception("No Content")
        raise Exception(response.status_code, response.text)

    def get_latest_academicPeriod(self) -> str:
        """
        Description
        ----------
        fetches latest academicPeriod from BinusMaya

        Parameters
        ----------
        None

        Returns
        -------
        academicPeriod : str
            academicPeriod from BinusMaya
        """
        response = self.r.get(f"{self.base_url}/func-bm7-course-prod/AcademicPeriod/Student", headers=self.headers)
        if response.status_code == 200:
            for academicPeriod in response.json():
                startDate = datetime.datetime.strptime(academicPeriod["termStartDate"], "%Y-%m-%dT%H:%M:%S")
                endDate = datetime.datetime.strptime(academicPeriod["termEndDate"], "%Y-%m-%dT%H:%M:%S")
                if startDate <= datetime.datetime.now() <= endDate:
                    break
            return academicPeriod
        raise Exception(response.text)

    def get_schedule_date(
        self, date_start: datetime.datetime, date_end: datetime.datetime = None
    ) -> dict:
        """
        Description
        ----------
        fetches schedule date from BinusMaya

        Parameters
        ----------
        date_start : datetime.datetime mandatory
            date_start to get schedule from

        date_end : datetime.datetime optional
            date_end to get schedule from

        Returns
        -------
        schedule : dict
            schedule from BinusMaya
        """

        def fetch_schedule(date):
            return self.__post_data(
                "{}/api/schedule/Date-v1/{}".format(
                    self.schedule_base_url, date.strftime("%Y-%-m-%-d")
                ),
                json_data={},
            )

        if date_end is None:
            return fetch_schedule(date= date_start)["Schedule"]
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
    def get_schedule_month(self, date: datetime.datetime) -> dict:
        """
        Description
        ----------
        fetches schedule month from BinusMaya

        Parameters
        ----------
        date : datetime.datetime mandatory
            date to get schedule from

        Returns
        -------
        schedule : dict
            schedule from BinusMaya
        """
        return self.__post_data(
            "{}/api/schedule/Month-v1/{}".format(
                self.schedule_base_url, date.strftime("%Y-%-m-1")
            ),
            json_data={},
        )

    # --ClassComponent-- #
    def get_class_component_list(self, period: int = None) -> dict:
        """
        Description
        ----------
        fetches class component list ["LEC", "LAB", "TUT", etc.] from BinusMaya

        Parameters
        ----------
        period : int optional
            period to get class component list from (default: latest academicPeriod)

        Returns
        -------
        classComponentList : list
            class component list from BinusMaya
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
        self, period: int = None, classComponentId: str = None
    ) -> dict:
        """
        Description
        ----------
        fetches class from BinusMaya by classComponentId and period

        Parameters
        ----------
        period : int optional
            period to get class from (default: latest academicPeriod)

        classComponentId : str mandatory
            classComponentId to get class from

        Returns
        -------
        class : dict
            class from BinusMaya
        """
        if period is None:
            period = self.get_latest_academicPeriod()["academicPeriod"]
        else:
            period = str(period)
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/Component/{classComponentId}/Student"
        )

    def get_class_active(self) -> dict:
        """
        Description
        ----------
        fetches current attended classes from BinusMaya

        Parameters
        ----------
        None

        Returns
        -------
        class : dict
            current attended classes from BinusMaya
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Class/Active/Student"
        )

    # --classSessions-- #
    def __default_classSessionId(self) -> str:
        """
        Description
        ----------
        an internal function to get default classSessionId

        Parameters
        ----------
        None

        Returns
        -------
        classSessionId : str
            default classSessionId from ongoing(if any) class or upcoming(if any) class
        """
        ongoing = self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Ongoing/student"
        )
        upcoming = self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Upcoming/student"
        )
        if ongoing.get("isHasUpcomingClass") is True:
            return upcoming["id"]
        return ongoing["id"]

    def get_class_sessions_from_class_id(self, classId: str) -> dict:
        """
        Description
        ----------
        fetches class sessions from BinusMaya by classId

        Parameters
        ----------
        classId : str mandatory
            classId to get class sessions from

        Returns
        -------
        classSessions : dict
            class sessions from BinusMaya
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Class/{classId}/Student"
        )

    def get_class_session_detail(self, classSessionId: str = None) -> dict:
        """
        Description
        ----------
        fetches class session detail from BinusMaya by classSessionId

        Parameters
        ----------
        classSessionId : str optional
            classSessionId to get class session detail from (default: classSessionId from ongoing(if any) class or upcoming(if any) class)

        Returns
        -------
        classSessionDetail : dict
            class session detail from BinusMaya
        """
        if classSessionId is None:
            classSessionId = self.__default_classSessionId()
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/{classSessionId}/Resource/Student"
        )

    # --resource-- #
    def get_resource_from_resource_id(self, resourceId: str = None) -> dict:
        """
        Description
        ----------
        fetches resource from BinusMaya by resourceId

        Parameters
        ----------
        resourceId : str mandatory
            resourceId to get resource from

        Returns
        -------
        resource : dict
            resource from BinusMaya (if any)
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/Resource/{resourceId}"
        )

    def get_ppt_from_session_id(self, classSessionId: str = None) -> dict:
        """
        Description
        ----------
        fetches ppt from BinusMaya by classSessionId (if any)
        the url obtained differs from the one in get_resource_from_resource_id, this url appears to be from the object storage

        Parameters
        ----------
        classSessionId : str optional
            classSessionId to get ppt from (default: classSessionId from ongoing(if any) class or upcoming(if any) class)

        Returns
        -------
        ppt_link: str
            ppt link from BinusMaya (if any)
        """

        def get_source_url(self, resourceId: str) -> str:
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

        resources = self.get_class_session_detail(classSessionId)["resources"]
        for i in range(len(resources)):
            if resources[i]["resourceType"] == "Document":
                return get_source_url(resources[i]["id"])

    # --forum-- #
    def get_forum_latest(self, classId: str = None) -> dict:
        """
        Description
        ----------
        fetches forum from BinusMaya by classId (default: ongoing(if any) class or upcoming(if any) class)

        Parameters
        ----------
        classId : str optional
            classId to get forum from (default: ongoing(if any) class or upcoming(if any) class)

        Returns
        -------
        forum : dict
            forum information from BinusMaya (if any)
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

    def get_forum_from_class_id(self, classId: str = None) -> dict:
        """
        Description
        ----------
        fetches forum from BinusMaya by classId (default: ongoing(if any) class or upcoming(if any) class)

        Parameters
        ----------
        classId : str optional
            classId to get forum from (default: ongoing(if any) class or upcoming(if any) class)

        Returns
        -------
        forum : dict
            forum information from BinusMaya (if any)
        """
        return self.__get_data(
            f"{self.base_url}/func-bm7-course-prod/Forum/Class/{classId}/Student"
        )

    def get_forum_thread(self, classId: str = None, sessionId: str = None) -> dict:
        """
        Description
        ----------
        fetches forum thread from BinusMaya by classId and sessionId (default: ongoing(if any) class or upcoming(if any) class)

        Parameters
        ----------
        classId : str optional
            classId to get forum thread from (default: ongoing(if any) class or upcoming(if any) class)

        Returns
        -------
        forum : dict
            forum information from BinusMaya (if any)
        """
        if classId is None:
            classId = self.__default_classId()
        return self.__post_data(
            f"{self.base_url}/func-bm7-forum-prod/Thread/Class/{classId}/Session/{sessionId}/Paging/1",
            json_data={"TotalDataPerPage": 100},
        )

    def get_forum_thread_content(self, classId: str = None, threadId: str = None) -> dict:
        """
        Description
        ----------
        fetches forum thread content from BinusMaya by classId and threadId (default: latest thread)

        Parameters
        ----------
        classId : str optional
            classId to get forum thread content from (default: latest thread)
        
        threadId : str optional
            threadId to get forum thread content from (default: latest thread)
            
        Returns
        -------
        forum : dict
            forum information from BinusMaya
        """
        if classId is None and threadId is None:
            classId = self.get_forum_latest()["latestPost"][0]["classId"]
            threadId = self.get_forum_latest()["latestPost"][0]["threadId"]
        return self.__get_data(
            f"{self.base_url}/func-bm7-forum-prod/Forum/{classId}/Thread/{threadId}",
            params={"originMultiClassId": None},
        )

    def get_forum_thread_comment(self, classId: str = None, threadId: str = None) -> dict:
        """
        Description
        ----------
        fetches forum thread comment from BinusMaya by classId and threadId (default: latest thread)

        Parameters
        ----------
        classId : str optional
            classId to get forum thread comment from (default: latest thread)
        
        threadId : str optional
            threadId to get forum thread comment from (default: latest thread)
        
        Returns
        -------
        forum : dict
            forum information from BinusMaya
        """
        if classId is None and threadId is None:
            classId = self.get_forum_latest()["latestPost"][0]["classId"]
            threadId = self.get_forum_latest()["latestPost"][0]["threadId"]
        return self.__post_data(
            f"{self.base_url}/func-bm7-forum-prod/Comment/Paging/1",
            json_data={
                "totalDataPerPage": 100,
                "parentId": threadId,
                "sortBy": "LatestPost",
                "forumId": classId,
            },
        )
