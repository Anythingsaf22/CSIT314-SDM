from dataclasses import dataclass
from typing import List, Optional
from db import get_connection


@dataclass
class UserProfile:
    """
    Entity class representing a user profile (role).
    Example profiles: User Admin, Fundraiser, Donor, Platform Management.
    """
    profileId: Optional[int]
    profileName: str
    profileDescription: str

    @classmethod
    def fromRow(cls, row) -> "UserProfile":
        """
        Create a UserProfile instance from a database row.
        """
        return cls(
            profileId = row["profile_id"],
            profileName = row["profile_name"],
            profileDescription= row["profile_desc"]
        )

    @classmethod
    def profileExists(cls, profileName: str) -> bool:
        """
        checks if a user profile with the given name exists.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT 1
            FROM user_profile
            WHERE LOWER(profile_name) = LOWER(?)
            """, #checks if matching profile exists, lower() allows case-insensitive
            (profileName.strip(),)
        )
        row = cursor.fetchone() #gets first matching results if there is any
        connection.close()
        return row is not None #return true if matching profile found if not return false


    @classmethod
    def createProfile(cls, profileName: str, profileDescription: str):
        """
        Create and store a new user profile to databse.
        """
        #Check for duplicate profile name before creating a new profile.
        if cls.profileExists(profileName):
            raise ValueError(f"Profile '{profileName}' already exists")
        else:
            connection = get_connection()
            cursor = connection.execute(
                """
                INSERT INTO user_profile (profile_name, profile_desc)
                Values (?, ?)
                """,
                (profileName.strip(), profileDescription.strip())
            )
            connection.commit()
            cls(
                profileId = cursor.lastrowid,
                profileName=profileName.strip(),
                profileDescription=profileDescription.strip()
            )
            connection.close()

    # A method to retrieve all profiles for demo purposes.
    @classmethod
    def getAllProfiles(cls) -> List["UserProfile"]:
        """
        Return all stored profiles.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT profile_id, profile_name, profile_desc
            FROM user_profile
            ORDER BY profile_id
            """
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def searchProfiles(cls, searchTerm: str) -> List["UserProfile"]:
        """
        Search user profiles by name or description
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"
        cursor = connection.execute(
            """
            SELECT profile_id, profile_name, profile_desc
            FROM user_profile
            WHERE LOWER(profile_name) LIKE LOWER(?)
                or LOWER(profile_desc) LIKE LOWER(?)
            ORDER BY profile_id
            """, #LIKE used for partial matching
            (keyword, keyword)
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]