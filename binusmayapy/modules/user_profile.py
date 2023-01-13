class UserProfileAPI:
    def get_profile(self):
        """It takes the token from the class and uses it to get the user's profile data from the API

        Returns
        -------
            A dictionary of the user's profile information.

        """
        _headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }
        data = self.get_data(
            "https://apim-bm7-prod.azure-api.net/func-bm7-profile-prod/UserProfile",
            headers=_headers,
        )
        return data

    def get_user_info(self):
        """It gets the user's profile, then gets the primary role, then gets the role id, NIM, and academic
        program

        Returns
        -------
            A dictionary with the user's information. {full_name, person_code, email, user_picture_url, role_id, NIM, academic_program}

        """
        data = self.get_profile()
        primary_role = next(
            (
                role
                for role in data["roleCategories"]
                if "roles" in role
                and next(
                    (role for role in role["roles"] if role["isPrimary"]),
                    None,
                )
            ),
            None,
        )

        user_info = {
            "full_name": data["fullName"],
            "person_code": data["personCode"],
            "email": data["email"],
            "user_picture_url": data["userPictureUrl"],
            "role_id": primary_role["roles"][0]["roleId"],
            "NIM": primary_role["roles"][0]["userCode"],
            "academic_program": primary_role["roles"][0]["academicProgramDesc"],
        }
        return user_info
