import requests
import datetime


from .modules import (
    classes,
    forums,
    schedules,
    resources,
    academic_period,
    user_profile,
)


class Bimay:
    def __init__(self, token: str, roleId: str = None):
        """
        Description
        ----------
        constructs bimay object

        Parameters
        ----------
        roleId : str optional
            roleId from bimay

        token : str mandatory
            Bearer token from bimay

        Returns
        -------
        None
        """
        if token.startswith("Bearer "):
            token = token[7:]
        self.token = token
        self.r = requests.Session()
        if roleId is None:
            self.roleId = user_profile.get_user_info(self)["role_id"]
        else:
            self.roleId = roleId

        self.headers = {
            "Authorization": "Bearer {}".format(token),
            "institution": "BNS01",
            "Content-Type": "application/json",
            "academicCareer": "RS1",
            # "roleId": roleId if roleId is not None else user_profile.get_user_info(self)["role_id"],
            "roleId": self.roleId,
            "Accept": "application/json, text/plain, */*",
            "roleName": "Student",
            "Origin": "https://newbinusmaya.binus.ac.id",
            "Referer": "https://newbinusmaya.binus.ac.id/",
        }
        self.base_url = "https://apim-bm7-prod.azure-api.net"
        self.schedule_base_url = "https://func-bm7-schedule-prod.azurewebsites.net"

    def get_data(self, url, json_data=None, params=None, headers=None) -> dict:
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
            try:
                return response.json()
            except:
                return response.text
        if response.status_code == 204:
            raise Exception("No Content")
        raise Exception(response.status_code, response.text)

    def post_data(self, url, json_data=None, params=None, headers=None) -> dict:
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
            try:
                return response.json()
            except:
                return response.text
        if response.status_code == 204:
            raise Exception("No Content")
        raise Exception(response.status_code, response.text)

    def get_latest_academicPeriod(self) -> dict:
        """
        Description
        ----------
        fetches latest academicPeriod from BinusMaya

        Parameters
        ----------
        None

        Returns
        -------
        academicPeriod : dict
            academicPeriod from BinusMaya
        """
        return academic_period.get_latest_academicPeriod(self)

    def get_latest_academic_start_end_date(self) -> tuple:
        """
        Description
        ----------
        fetches latest academicPeriod from BinusMaya

        Parameters
        ----------
        None

        Returns
        -------
        start_date : datetime.datetime
            academicPeriod start date from BinusMaya
        end_date : datetime.datetime
            academicPeriod end date from BinusMaya
        """
        return academic_period.get_latest_academic_start_end_date(self)

    def get_schedule(
        self, date_start: datetime.datetime, end_date: datetime.datetime = None
    ) -> dict:
        """
        Description
        ----------
        fetches schedule from BinusMaya

        Parameters
        ----------
        date_start : datetime.datetime mandatory
            start date of schedule

        end_date : datetime.datetime mandatory
            end date of schedule

        Returns
        -------
        schedule : dict
            schedule from BinusMaya
        """
        if end_date is not None:
            if (end_date - date_start).days > 30:
                return self.get_schedule_month(date_start, end_date)
            else:
                return self.get_schedule_date(date_start, end_date)
        else:
            return self.get_schedule_date(date_start)

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
        return schedules.get_schedule_date(self, date_start, date_end)

    def get_schedule_month(
        self, month_start: datetime.datetime, month_end: datetime.datetime = None
    ) -> dict:
        """
        Description
        ----------
        fetches schedule month from BinusMaya

        Parameters
        ----------
        month_start : datetime.datetime mandatory
            month_start to get schedule from

        month_end : datetime.datetime optional
            month_end to get schedule from

        Returns
        -------
        schedule : dict
            schedule from BinusMaya
        """
        return schedules.get_schedule_month(self, month_start, month_end)

    # --ClassComponent-- #
    def get_class_component_list(self, period: int = None) -> list:
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
        return classes.get_class_component_list(self, period)

    # --classes-- #
    def get_class_from_component(
        self, period: int = None, classComponentId: str = None
    ) -> list:
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
        return classes.get_class_from_component(self, period, classComponentId)

    def get_class_active(self) -> list:
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
        return classes.get_class_active(self)

    # --classSessions-- #
    def default_classSessionId(self) -> str:
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
        return classes.default_classSessionId(self)

    def default_classId(self) -> str:
        """
        Description
        ----------
        an internal function to get default classId

        Parameters
        ----------
        None

        Returns
        -------
        classId : str
            default classId from ongoing(if any) class or upcoming(if any) class
        """
        return classes.default_classId(self)

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
        return classes.get_class_sessions_from_class_id(self, classId)

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
        return classes.get_class_session_detail(self, classSessionId)

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
        return resources.get_resource_from_resource_id(self, resourceId)

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

        return resources.get_ppt_from_session_id(self, classSessionId)

    def post_student_progress(self, resourceId: str) -> dict:
        """
        Description
        ----------
        post resource student progress to BinusMaya

        Parameters
        ----------
        resourceId : str
            resourceId to post student progress to

        Returns
        -------
        progress : dict
            progress information from BinusMaya
        """
        return resources.post_student_progress(self, resourceId)

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
        return forums.get_forum_latest(self, classId)

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
        return forums.get_forum_from_class_id(self, classId)

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
        return forums.get_forum_thread(self, classId, sessionId)

    def get_forum_thread_content(
        self, classId: str = None, threadId: str = None
    ) -> dict:
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
        return forums.get_forum_thread_content(self, classId, threadId)

    def get_forum_thread_comment(
        self, classId: str = None, threadId: str = None
    ) -> dict:
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
        return forums.get_forum_thread_comment(self, classId, threadId)

    def get_user_profile(self) -> dict:
        """
        Description
        ----------
        fetches user profile from BinusMaya

        Parameters
        ----------
        None

        Returns
        -------
        userProfile : dict
            user profile information from BinusMaya
        """
        return user_profile.get_user_info(self)
