import calendar
import datetime


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
            "Schedule": schedule_formater(self, schedules),
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
            "Schedule": schedule_formater(self, schedules),
        }
        return data


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_schedule_month(
    self, month_start: datetime.datetime, month_end: datetime.datetime = None
) -> dict:
    def fetch_schedule(month):
        rawschedules = self.post_data(
            "{}/api/schedule/Month-v1/{}".format(
                self.schedule_base_url, month.strftime("%Y-%-m-1")
            ),
            json_data={},
        )
        first_date_start = min(rawschedules, key=lambda x: x["dateStart"])["dateStart"]
        schedules = []

        for i in range(len(rawschedules)):
            for j in range(len(rawschedules[i]["Schedule"])):
                schedules.append(rawschedules[i]["Schedule"][j])
        data = {"dateStart": first_date_start, "Schedule": schedules}
        return data

    if month_end is None:
        schedules = fetch_schedule(month=month_start)["Schedule"]
        first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
        data = {
            "dateStart": first_date_start,
            "Schedule": schedule_formater(self, schedules),
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
            month = add_months(month_start, i)
            for j in range(len(fetch_schedule(month)["Schedule"])):
                schedules.append(fetch_schedule(month)["Schedule"][j])

        first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
        data = {
            "dateStart": first_date_start,
            "Schedule": schedule_formater(self, schedules),
        }
        return data


def resource_url_reformat(resource_type: str, url: str):
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
                    "resource_url": resource_url_reformat(
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
