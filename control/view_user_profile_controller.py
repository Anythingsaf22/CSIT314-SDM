from typing import List, Optional
from entity.user_profile import UserProfile

class view_user_profile_controller:
    """
    Control class responsible for validating input and retrieving user profile details.
    """

    def viewUserProfile(self) -> List["UserProfile"]:
        """
        Retrieve all user profiles object.
        """
        return UserProfile.getAllProfiles()

