from typing import Tuple, Optional
from entity.user_profile import UserProfile


class create_user_profile_controller:
    """
    Control class responsible for validating input and creating user profiles.
    """

    def createUserProfile(self, profileName: str, profileDescription: str) -> Tuple[bool, str, Optional[UserProfile]]:
        """
        Main public method used by the Boundary.

        Returns:
            (success, message, created_profile)
        """

        is_valid, error_message = self.validateProfileInput(profileName, profileDescription)
        if not is_valid:
            return False, error_message, None

        if self.checkDuplicateProfile(profileName):
            return False, "Error: The user profile already exists.", None

        created_profile = UserProfile.saveProfile(profileName, profileDescription)
        return True, "User profile created successfully.", created_profile

    def validateProfileInput(self, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        """
        Validate required fields for user profile creation.
        """
        if not profileName or not profileName.strip():
            return False, "Error: Profile name is required."

        if not profileDescription or not profileDescription.strip():
            return False, "Error: Profile description is required."

        return True, ""

    def checkDuplicateProfile(self, profileName: str) -> bool:
        """
        Check whether the profile already exists.
        """
        return UserProfile.profileExists(profileName)