from typing import Tuple, Optional
from entity.user_profile import UserProfile


class create_user_profile_controller:
    """
    Control class responsible for creating user profiles.
    """

    def createUserProfile(self, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        """
        Returns:
            (success(Boolean), message)
        """
        try:
            """
            Validate input(Check duplicate) and create a new user profile.
            """
            UserProfile.createProfile(profileName, profileDescription)
            return True, "Profile created successfully"

        except ValueError as e:
            return False, str(e)
    