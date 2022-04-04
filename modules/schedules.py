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
        return fetch_schedule(date=date_start)["Schedule"]
    else:
        schedules = []
        for date in (
            date_start + datetime.timedelta(days=x)
            for x in range(0, (date_end - date_start).days)
        ):
            try:
                schedules_ = fetch_schedule(date=date)["Schedule"]
            except:
                pass
            for i in range(len(schedules_)):
                schedules.append(schedules_[i])
        first_date_start = min(schedules, key=lambda x: x["dateStart"])["dateStart"]
        data = {"dateStart": first_date_start, "Schedule": schedules}
        return data

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
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
        first_date_start = min(rawschedules, key=lambda x: x["dateStart"])[
            "dateStart"
        ]
        schedules = []

        for i in range(len(rawschedules)):
            for j in range(len(rawschedules[i]["Schedule"])):
                schedules.append(rawschedules[i]["Schedule"][j])
        data = {"dateStart": first_date_start, "Schedule": schedules}
        return data

    if month_end is None:
        return fetch_schedule(month=month_start)
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
        data = {"dateStart": first_date_start, "Schedule": schedules}
        return data