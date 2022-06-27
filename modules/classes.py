def get_class_component_list(self, period: int = None) -> dict:
    if period is None:
        period = self.get_latest_academicPeriod()["academicPeriod"]
    else:
        period = str(period)
    return self.get_data(
        f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/ClassComponentList/Student"
    )


# --classes-- #


def get_class_from_component(
    self, period: int = None, classComponentId: str = None
) -> dict:
    if period is None:
        period = self.get_latest_academicPeriod()["academicPeriod"]
    else:
        period = str(period)
    return self.get_data(
        f"{self.base_url}/func-bm7-course-prod/Course/Period/{period}/Component/{classComponentId}/Student"
    )


def get_class_active(self) -> dict:
    return self.get_data(f"{self.base_url}/func-bm7-course-prod/Class/Active/Student")


def default_classSessionId(self) -> str:
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
    return self.get_data(
        f"{self.base_url}/func-bm7-course-prod/ClassSession/Class/{classId}/Student"
    )


def get_class_session_detail(self, classSessionId: str = None) -> dict:
    if classSessionId is None:
        classSessionId = default_classSessionId()
    return self.get_data(
        f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/{classSessionId}/Resource/Student"
    )
