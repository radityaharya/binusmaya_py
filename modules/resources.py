def get_resource_from_resource_id(self, resourceId: str = None) -> dict:
    return self.get_data(
        f"{self.base_url}/func-bm7-course-prod/ClassSession/Session/Resource/{resourceId}"
    )

def get_ppt_from_session_id(self, classSessionId: str = None) -> dict:
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
            return get_source_url(self, resourceId = resources[i]["id"])

def post_student_progress(self, resourceId: str) -> dict:
    data = {"resourceId": resourceId, "status": 2}
    self.post_data(
        f"{self.base_url}/func-bm7-course-prod/StudentProgress",
        json_data= data,
    )
    return data