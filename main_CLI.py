from boundary.create_user_profile_page_CLI import create_user_profile_page
from entity.user_profile import UserProfile


def insert_all_profiles() -> None:
    """
    insert all user profiles (User Admin, Fundraiser, Donor, Platform Management) into the system (for demo purposes).
    """
    if not UserProfile.profileExists("User_Admin"):
        UserProfile.saveProfile(
            "User_Admin",
            "A user who manages user accounts, profiles, and system administration tasks."
        )

    if not UserProfile.profileExists("FUNDRAISER"):
        UserProfile.saveProfile(
            "FUNDRAISER",
            "A user who creates and manages fundraising activities, tracks donor interest, and monitors campaign progress."
        )

    if not UserProfile.profileExists("DONOR"):
        UserProfile.saveProfile(
            "DONOR",
            "A user who searches, views, and saves fundraising activities, and donates to support campaigns."
        )

    if not UserProfile.profileExists("Platform_Management"):
        UserProfile.saveProfile(
            "Platform_Management",
            "A user who manages fundraising categories and generates platform reports."
        )

# Additional functions for demo
def show_all_profiles() -> None:
    profiles = UserProfile.getAllProfiles()

    print("\n=== Current User Profiles ===")
    if not profiles:
        print("No user profiles found.")
        return

    for index, profile in enumerate(profiles, start=1):
        print(f"{index}. {profile.profileName} - {profile.profileDescription}")


def main() -> None:
    insert_all_profiles()

    while True:
        print("\n=== Fundraising System Menu ===")
        print("1. Create User Profile")
        print("2. View All User Profiles (For Demo)")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            page = create_user_profile_page()
            page.run()
        elif choice == "2":
            show_all_profiles()
        elif choice == "3":
            print("Exiting system...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()