class ClassesAPI:
    def get_class_component_list(self, period: int = None) -> dict:
        """It returns a dictionary of all the classes you're taking in a given period

        Parameters
        ----------
        period : int
            The academic period you want to get the class component list for.

        Returns
        -------
            A list of all the classes you are enrolled in for the given period.

        """
        if period is None:
            period = self.get_latest_academicPeriod()["academicPeriod"]
        else:
            period = str(period)
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/ClassComponentList/Student"
        )

    def get_class_from_component(
        self, period: int = None, classComponentId: str = None
    ) -> dict:
        """This function takes in a class component ID and returns a dictionary of all the classes for that
        class component.

        Parameters
        ----------
        period : int
            The academic period of the class component.
        classComponentId : str
            The ID of the class component. ("LAB" or "LEC" or "TUT")

        Returns
        -------
            A list of dictionaries of the classes for a given class component.

        """

        if period is None:
            period = self.get_latest_academicPeriod()["academicPeriod"]
        else:
            period = str(period)
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/Component/{classComponentId}/Student"
        )

    def get_class_active(self) -> dict:
        """This function returns a dictionary of all the classes that are currently active for the student

        Returns
        -------
            A dictionary of the active classes for the student.

        """
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/Class/Active/Student"
        )

    def default_classSessionId(self) -> str:
        """It gets the ongoing class session id if there is no upcoming class, otherwise it gets the
        upcoming class session id

        Returns
        -------
            The classSessionId is being returned.

        """
        ongoing = self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Ongoing/student"
        )
        upcoming = self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Upcoming/student"
        )
        if ongoing.get("isHasUpcomingClass") is True:
            return upcoming["id"]
        return ongoing["id"]

    def default_classId(self) -> str:
        """It gets the classId of the class that is currently ongoing or upcoming

        Returns
        -------
            The classId of the current class.

        """
        ongoing = self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Ongoing/student"
        )
        upcoming = self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Upcoming/student"
        )
        if ongoing.get("isHasUpcomingClass") is True:
            return upcoming["classId"]
        return ongoing["classId"]

    def get_class_sessions_from_class_id(self, classId: str) -> dict:
        """This function takes in a class ID and returns a dictionary of all the class sessions for that
        class.

        Parameters
        ----------
        classId : str
            The ID of the class you want to get the sessions for.

        Returns
        -------
            A list of class sessions for a given class id.

        """
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Class/{classId}/Student"
        )

    def get_class_session_detail(self, classSessionId: str = None) -> dict:
        """This function returns a dictionary of the class session detail for a given class session id

        Parameters
        ----------
        classSessionId : str
            The ID of the class session.

        Returns
        -------
            A list of dictionaries of the class session detail for a given class session id.

        """
        if classSessionId is None:
            classSessionId = self.default_classSessionId()
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/{classSessionId}/Resource/Student"
        )

    def get_class_attendance_from_class_id(self, classId: str = None) -> dict:
        """This function takes in a class ID and returns a dictionary of the class attendance

        Parameters
        ----------
        classId : str
            The ID of the class you want to get the attendance for.

        Returns
        -------
            A dictionary of the class attendance for a given class.

        """
        if classId is None:
            classId = self.default_classId()
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/SessionAttendance/Class/{classId}/Student"
        )
