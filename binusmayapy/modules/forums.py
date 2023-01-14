class ForumsAPI:
    def get_forum_latest(self, classId: str = None) -> dict:
        """It gets the latest forum posts for a class

        Parameters
        ----------
        classId : str
            The class ID of the class you want to get the latest forum posts from. (Defaults to ongoing/upcoming class)

        Returns
        -------
            A list of dicts.

        """
        if classId is None:
            return self.post_data(
                f"{self.base_url}/func-bm7-forum-prod/Forum/LatestPostForum",
                json_data=self.get_class_active(),
            )
        else:
            return self.post_data(
                f"{self.base_url}/func-bm7-forum-prod/Forum/LatestPostForum",
                json_data=[{"classId": classId}],
            )

    def get_forum_from_class_id(self, classId: str = None) -> dict:
        """It returns a dictionary of the forum for a given class ID

        Parameters
        ----------
        classId : str
            The class ID of the class you want to get the forum from.

        Returns
        -------
            A list of dicts containing the forum data.

        """
        return self.get_data(
            f"{self.base_url}/func-bm7-course-prod/Forum/Class/{classId}/Student"
        )

    def get_forum_thread(self, classId: str = None, sessionId: str = None) -> dict:
        """This function gets the forum thread of a class

        Parameters
        ----------
        classId : str
            The class ID of the class you want to get the forum threads from. (Defaults to ongoing/upcoming class)
        sessionId : str
            The session ID of the class. You can get this from the class list.

        Returns
        -------
            A list of dictionaries.

        """
        if classId is None:
            classId = self.default_classId()
        return self.post_data(
            f"{self.base_url}/func-bm7-forum-prod/Thread/Class/{classId}/Session/{sessionId}/Paging/1",
            json_data={"TotalDataPerPage": 100},
        )

    def get_forum_thread_content(
        self, classId: str = None, threadId: str = None
    ) -> dict:
        """This function gets the content of a forum thread

        Parameters
        ----------
        classId : str
            The class ID of the class you want to get the forum threads from. (Defaults to ongoing/upcoming class)
        threadId : str
            The thread ID of the thread you want to get the content from.

        Returns
        -------
            A dictionary of the thread content.

        """
        if classId is None and threadId is None:
            classId = self.get_forum_latest()["latestPost"][0]["classId"]
            threadId = self.get_forum_latest()["latestPost"][0]["threadId"]
        return self.get_data(
            f"{self.base_url}/func-bm7-forum-prod/Forum/{classId}/Thread/{threadId}",
            params={"originMultiClassId": None},
        )

    def get_forum_thread_comment(
        self, classId: str = None, threadId: str = None
    ) -> dict:
        """This function gets the comments of a forum thread

        Parameters
        ----------
        classId : str
            The class ID of the class you want to get the forum threads from. (Defaults to ongoing/upcoming class)
        threadId : str
            The thread ID of the thread you want to get the content from.

        Returns
        -------
            A dictionary of the thread content.

        """

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
