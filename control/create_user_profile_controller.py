from typing import Tuple, Optional
from entity.user_profile import UserProfile


class create_user_profile_controller:
    """
    Control class responsible for validating input and creating user profiles.
    """

    def createUserProfile(self, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        """
        Main public method used by the Boundary.

        Returns:
            (success, message)
        """
        try:
            UserProfile.createProfile(profileName, profileDescription)
            return True, "Profile created successfully"

        except ValueError as e:
            return False, str(e)
    