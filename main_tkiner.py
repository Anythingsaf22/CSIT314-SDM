import tkinter as tk

from boundary.create_user_profile_page_tkiner import create_user_profile_page
from entity.user_profile import UserProfile


def insert_all_profiles() -> None:
    """
    insert all user profiles (User Admin, Fundraiser, Donor, Platform Management) into the system (for demo purposes).
    """
    if not UserProfile.profileExists("User Admin"):
        UserProfile.saveProfile(
            "User Admin",
            "A user who manages user accounts, profiles, and system administration tasks."
        )

    if not UserProfile.profileExists("Fundraiser"):
        UserProfile.saveProfile(
            "Fundraiser",
            "A user who creates and manages fundraising activities, tracks donor interest, and monitors campaign progress."
        )

    if not UserProfile.profileExists("Donor"):
        UserProfile.saveProfile(
            "Donor",
            "A user who searches, views, and saves fundraising activities, and donates to support campaigns."
        )

    if not UserProfile.profileExists("Platform Management"):
        UserProfile.saveProfile(
            "Platform Management",
            "A user who manages fundraising categories and generates platform reports."
        )


def main() -> None:
    insert_all_profiles()
    root = tk.Tk()
    app = create_user_profile_page(root)
    root.mainloop()


if __name__ == "__main__":
    main()