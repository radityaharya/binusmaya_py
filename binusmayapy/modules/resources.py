class ResourcesAPI:
    def get_resource_from_resource_id(self, resourceId: str = None) -> dict:
        """This function takes in a resourceId and returns a dictionary of the resource information

        Parameters
        ----------
        resourceId : str
            The resource ID of the resource you want to get.

        Returns
        -------
            A dictionary of the resource information.

        """
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/Resource/{resourceId}"
        )

    def get_ppt_from_session_id(self, classSessionId: str = None) -> str:
        """It takes a classSessionId as an argument and returns the url of the ppt file

        Parameters
        ----------
        classSessionId : str
            The id of the class session.

        Returns
        -------
            A string of the url of the ppt

        """

        def get_source_url(self, resourceId: str) -> str:
            """
            -args: resourceId
            """
            url = self.get_resource_from_resource_id(resourceId)["url"]
            if not url.startswith("https://stbm7resourcesprod.blob.core.windows.net"):
                raise Exception("Invalid url")
            return url.replace(
                "https://stbm7resourcesprod.blob.core.windows.net:443/resources/",
                "https://databinuscampussolution.blob.core.windows.net/bol/",
            ).split("?")[0]

        resources = self.get_class_session_detail(classSessionId)["resources"]
        for i in range(len(resources)):
            if (
                resources[i]["resourceType"] == "Document"
                or resources[i]["resourceType"] == "ppt"
                or resources[i]["resourceType"] == "pptx"
            ):
                return get_source_url(self, resourceId=resources[i]["id"])
        return "no content"

    def post_student_progress(self, resourceId: str) -> dict:
        """This function posts the student progress to the server

        Parameters
        ----------
        resourceId : str
            The resource ID to be posted.

        Returns
        -------
        dict
            The data that was posted.

        """
        data = {"resourceId": resourceId, "status": 2}
        self.post_data(
            f"{self.base_url}/func-bm7-course-prod/StudentProgress",
            json_data=data,
        )
        return data
