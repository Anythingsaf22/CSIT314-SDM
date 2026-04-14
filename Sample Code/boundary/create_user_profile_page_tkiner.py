import tkinter as tk
from tkinter import messagebox

from control.create_user_profile_controller import create_user_profile_controller
from entity.user_profile import UserProfile


class create_user_profile_page:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.controller = create_user_profile_controller()

        self.root.title("Create User Profile")
        self.root.geometry("500x400")

        self.title_label = tk.Label(root, text="Create User Profile", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.name_label = tk.Label(root, text="Profile Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack(pady=5)

        self.description_label = tk.Label(root, text="Profile Description")
        self.description_label.pack()
        self.description_entry = tk.Entry(root, width=40)
        self.description_entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="Create", command=self.submitProfile)
        self.submit_button.pack(pady=10)

        self.view_button = tk.Button(root, text="View All Profiles (for Demo)", command=self.displayProfiles)
        self.view_button.pack(pady=5)

        self.result_label = tk.Label(root, text="", fg="blue", wraplength=420, justify="left")
        self.result_label.pack(pady=10)

        self.profile_listbox = tk.Listbox(root, width=60, height=8)
        self.profile_listbox.pack(pady=10)

    # Reset the form and clear previous results when displaying the form again.
    def displayCreateUserProfileForm(self) -> None:
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.profile_listbox.delete(0, tk.END)

    def getUserProfileInput(self):
        profileName = self.name_entry.get()
        profileDescription = self.description_entry.get()
        return profileName, profileDescription

    def displaySuccessMessage(self, message: str) -> None:
        self.result_label.config(text=message)
        messagebox.showinfo("Success", message)

    def displayErrorMessage(self, message: str) -> None:
        self.result_label.config(text=message)
        messagebox.showerror("Error", message)

    def submitProfile(self) -> None:
        profileName, profileDescription = self.getUserProfileInput()

        success, message, created_profile = self.controller.createUserProfile(
            profileName, profileDescription
        )

        if success:
            self.displaySuccessMessage(message)
            self.displayCreateUserProfileForm()
        else:
            self.displayErrorMessage(message)

    # For demo purposes: Display all profiles in the listbox.
    def displayProfiles(self) -> None:
        self.profile_listbox.delete(0, tk.END)
        profiles = UserProfile.getAllProfiles()

        if not profiles:
            self.profile_listbox.insert(tk.END, "No user profiles found.")
            return

        for index, profile in enumerate(profiles, start=1):
            self.profile_listbox.insert(
                tk.END,
                f"{index}. {profile.profileName} - {profile.profileDescription}"
            )