import calendar
import datetime


class SchedulesAPI:
    def get_schedule_date(
        self, date_start: datetime.datetime, date_end: datetime.datetime = None
    ) -> dict:
        def fetch_schedule(date):
            return self.post_data(
                "{}/api/schedule/Date-v1/{}".format(
                    self.schedule_base_url, date.strftime("%Y-%-m-%-d")
                ),
                json_data={},
            )

        if date_end is None:
            schedules = fetch_schedule(date=date_start)["Schedule"]
            first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
            data = {
                "dateStart": first_date_start,
                "Schedule": self.schedule_formater(schedules),
            }
            return data
        else:
            schedules = []
            for date in (
                date_start + datetime.timedelta(days=x)
                for x in range(0, (date_end - date_start).days)
            ):
                schedules_ = []
                try:
                    schedules_ = fetch_schedule(date=date)["Schedule"]
                except Exception as no_content:
                    pass
                for i in range(len(schedules_)):
                    schedules.append(schedules_[i])
            first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
            data = {
                "dateStart": first_date_start,
                "Schedule": self.schedule_formater(schedules),
            }
            return data

    def add_months(self, sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def get_schedule_month(
        self, month_start: datetime.datetime, month_end: datetime.datetime = None
    ) -> dict:
        def fetch_schedule(month):
            try:
                rawschedules = self.post_data(
                    "{}/api/schedule/Month-v1/{}".format(
                        self.schedule_base_url, month.strftime("%Y-%-m-1")
                    ),
                    json_data={},
                )
                schedules = [x for x in rawschedules if x is not None]
                first_date_start = min(rawschedules, key=lambda x: x["dateStart"])[
                    "dateStart"
                ]
                schedules = []

                for i in range(len(rawschedules)):
                    for j in range(len(rawschedules[i]["Schedule"])):
                        schedules.append(rawschedules[i]["Schedule"][j])
                data = {"dateStart": first_date_start, "Schedule": schedules}
                return data
            except Exception as no_content:
                print(no_content)
                return None

        if month_end is None:
            schedules = fetch_schedule(month=month_start)["Schedule"]
            first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
            data = {
                "dateStart": first_date_start,
                "Schedule": self.schedule_formater(schedules),
            }
            return data
        else:
            schedules = []

            months = (
                (month_end.year - month_start.year) * 12
                + month_end.month
                - month_start.month
            )
            for i in range(months + 1):
                month = self.add_months(month_start, i)
                fetch_sched = fetch_schedule(month)
                if fetch_sched is not None:
                    for j in range(len(fetch_sched["Schedule"])):
                        schedules.append(fetch_sched["Schedule"][j])
            first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
            data = {
                "dateStart": first_date_start,
                "Schedule": self.schedule_formater(schedules),
            }
            return data

    def get_schedule(
        self, date_start: datetime.datetime, end_date: datetime.datetime = None
    ) -> dict:
        """
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

    def resource_url_reformat(self, resource_type: str, url: str):
        if resource_type == "pdf" or resource_type == "ppt" or resource_type == "pptx":
            url.replace(
                "https://stbm7resourcesprod.blob.core.windows.net:443/resources/",
                "https://databinuscampussolution.blob.core.windows.net/bol/",
            ).split("?")[0]

        return url

    def schedule_formater(self, schedules: list):
        formated_schedules = []
        for schedule in schedules:
            class_session_detail = self.get_data(
                f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/{schedule['customParam']['classSessionId']}/Resource/Student"
            )
            formated_schedule = {
                "class_id": schedule["customParam"]["classId"],
                "class_session_id": schedule["customParam"]["classSessionId"],
                "course_name": schedule["content"],
                "course_class": schedule["title"],
                "session_number": schedule["customParam"]["sessionNumber"],
                "delivery_mode": schedule["deliveryMode"],
                "join_url": class_session_detail["joinUrl"],
                "location": {
                    "location": schedule["location"],
                    "location_value": schedule["locationValue"],
                },
                "date_start": schedule["dateStart"],
                "date_end": schedule["dateEnd"],
                "topic": class_session_detail["topic"],
                "subtopic": class_session_detail["courseSubTopic"],
                "resources": [
                    {
                        "resource_id": resource["id"],
                        "resource_name": resource["name"],
                        "resource_type": resource["resourceType"],
                        "resource_url": self.resource_url_reformat(
                            resource["resourceType"], resource["url"]
                        ),
                        "resource_is_open": resource["isOpen"],
                    }
                    for resource in class_session_detail["resources"]
                ],
                "is_ended": class_session_detail["isEnded"],
            }
            for resource in formated_schedule["resources"]:
                if (
                    resource["resource_type"] == "ppt"
                    or resource["resource_type"] == "pptx"
                    or resource["resource_type"] == "pdf"
                    or resource["resource_type"] == "Document"
                ):
                    resource["resource_url"] = (
                        resource["resource_url"]
                        .replace(
                            "https://stbm7resourcesprod.blob.core.windows.net:443/resources/",
                            "https://databinuscampussolution.blob.core.windows.net/bol/",
                        )
                        .split("?")[0]
                    )
            formated_schedules.append(formated_schedule)
        return formated_schedules
