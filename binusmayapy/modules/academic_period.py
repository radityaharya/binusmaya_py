import datetime


class AcademicPeriodAPI:
    def get_latest_academicPeriod(self) -> dict:
        """It gets the latest academic period (semester) from the API and returns it as a dictionary

        Returns
        -------
            A dictionary of the latest academic period.

        """
        response = self.r.get(
            f"{self.base_url}/func-bm7-course-prod/AcademicPeriod/Student",
            headers=self.headers,
        )
        if response.status_code == 200:
            for academicPeriod in response.json():
                startDate = datetime.datetime.strptime(
                    academicPeriod["termBeginDate"], "%Y-%m-%dT%H:%M:%S"
                )
                endDate = datetime.datetime.strptime(
                    academicPeriod["termEndDate"], "%Y-%m-%dT%H:%M:%S"
                )
                if startDate <= datetime.datetime.now() <= endDate:
                    break
            return academicPeriod
        raise Exception(response.text)

    def get_latest_academic_start_end_date(self) -> tuple:
        """It returns a tuple of the start and end date of the latest academic period

        Returns
        -------
            A tuple of the start and end date of the latest academic period.

        """
        academic_period = self.get_latest_academicPeriod()
        start_date = datetime.datetime.strptime(
            academic_period["termBeginDate"], "%Y-%m-%dT%H:%M:%S"
        )
        end_date = datetime.datetime.strptime(
            academic_period["termEndDate"], "%Y-%m-%dT%H:%M:%S"
        )
        return start_date, end_date
