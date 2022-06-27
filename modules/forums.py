def get_forum_latest(self, classId: str = None) -> dict:
    if classId is None:
        return self.post_data(
            f"{self.base_url}/func-bm7-forum-prod/Forum/LatestPostForum",
            json_data=self.get_class_active(),
        )
    else:
        return self.post_data(
            f"{self.base_url}/func-bm7-for um-prod/Forum/LatestPostForum",
            json_data=[{"classId": classId}],
        )


def get_forum_from_class_id(self, classId: str = None) -> dict:
    return self.get_data(
        f"{self.base_url}/func-bm7-course-prod/Forum/Class/{classId}/Student"
    )


def get_forum_thread(self, classId: str = None, sessionId: str = None) -> dict:
    if classId is None:
        classId = self.default_classId()
    return self.post_data(
        f"{self.base_url}/func-bm7-forum-prod/Thread/Class/{classId}/Session/{sessionId}/Paging/1",
        json_data={"TotalDataPerPage": 100},
    )


def get_forum_thread_content(self, classId: str = None, threadId: str = None) -> dict:
    if classId is None and threadId is None:
        classId = self.get_forum_latest()["latestPost"][0]["classId"]
        threadId = self.get_forum_latest()["latestPost"][0]["threadId"]
    return self.get_data(
        f"{self.base_url}/func-bm7-forum-prod/Forum/{classId}/Thread/{threadId}",
        params={"originMultiClassId": None},
    )


def get_forum_thread_comment(self, classId: str = None, threadId: str = None) -> dict:
    if classId is None and threadId is None:
        classId = self.get_forum_latest()["latestPost"][0]["classId"]
        threadId = self.get_forum_latest()["latestPost"][0]["threadId"]
    return self.post_data(
        f"{self.base_url}/func-bm7-forum-prod/Comment/Paging/1",
        json_data={
            "totalDataPerPage": 100,
            "parentId": threadId,
            "sortBy": "LatestPost",
            "forumId": classId,
        },
    )
