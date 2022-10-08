def get_profile(self):
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
    data = get_profile(self)
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
