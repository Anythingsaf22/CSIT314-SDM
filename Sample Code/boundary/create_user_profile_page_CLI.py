from control.create_user_profile_controller import create_user_profile_controller


class create_user_profile_page:
    """
    Boundary class responsible for user interaction.
    """

    def __init__(self) -> None:
        self.controller = create_user_profile_controller()

    def displayCreateUserProfileForm(self) -> None:
        """
        Display the user profile creation interface.
        """
        print("\n=== Create User Profile ===")
        print("Please enter the details below.")

    def getUserProfileInput(self) -> tuple[str, str]:
        """
        Get profile name and description from the user.
        """
        profileName = input("Profile Name: ").strip()
        profileDescription = input("Profile Description: ").strip()
        return profileName, profileDescription

    def displaySuccessMessage(self, profileName: str) -> None:
        """
        Display success message after creating the profile.
        """
        print(f"\nSuccess: User profile '{profileName}' has been created successfully.")

    def displayErrorMessage(self, message: str) -> None:
        """
        Display error message.
        """
        print(f"\n{message}")

    def run(self) -> None:
        """
        Run the boundary flow for creating a user profile.
        """
        self.displayCreateUserProfileForm()
        profileName, profileDescription = self.getUserProfileInput()

        success, message, created_profile = self.controller.createUserProfile(
            profileName,
            profileDescription
        )

        if success and created_profile is not None:
            self.displaySuccessMessage(created_profile.profileName)
        else:
            self.displayErrorMessage(message)