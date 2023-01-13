import requests
import datetime

from .modules.classes import ClassesAPI
from .modules.schedules import SchedulesAPI
from .modules.forums import ForumsAPI
from .modules.resources import ResourcesAPI
from .modules.academic_period import AcademicPeriodAPI
from .modules.user_profile import UserProfileAPI


class Bimay(
    ClassesAPI, SchedulesAPI, ForumsAPI, ResourcesAPI, AcademicPeriodAPI, UserProfileAPI
):
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
            self.roleId = self.get_user_info()["role_id"]
        else:
            self.roleId = roleId

        self.headers = {
            "Authorization": "Bearer {}".format(token),
            "institution": "BNS01",
            "Content-Type": "application/json",
            "academicCareer": "RS1",
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
