from dataclasses import dataclass
from typing import ClassVar, List, Optional


@dataclass
class UserProfile:
    """
    Entity class representing a user profile (role).
    Example profiles: User Admin, Fundraiser, Donor, Platform Management.
    """
    profileName: str
    profileDescription: str

    # Simple in-memory storage for demo purposes
    _profiles: ClassVar[List["UserProfile"]] = []

    @classmethod
    def profileExists(cls, profileName: str) -> bool:
        """
        Check whether a profile with the given name already exists.
        """
        normalized_name = profileName.strip().lower()
        return any(profile.profileName.strip().lower() == normalized_name for profile in cls._profiles)

    @classmethod
    def saveProfile(cls, profileName: str, profileDescription: str) -> "UserProfile":
        """
        Create and store a new user profile in memory.
        """
        new_profile = cls(
            profileName=profileName.strip(),
            profileDescription=profileDescription.strip()
        )
        cls._profiles.append(new_profile)
        return new_profile

    # A method to retrieve all profiles for demo purposes.
    @classmethod
    def getAllProfiles(cls) -> List["UserProfile"]:
        """
        Return all stored profiles.
        """
        return cls._profiles.copy()
    
    
    """
    @classmethod
    def findProfileByName(cls, profileName: str) -> Optional["UserProfile"]:
    """
        # Find (Search) a profile by name for later use.
    """
        normalized_name = profileName.strip().lower()
        for profile in cls._profiles:
            if profile.profileName.strip().lower() == normalized_name:
                return profile
        return None
    """