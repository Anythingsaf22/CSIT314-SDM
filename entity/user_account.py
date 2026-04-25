from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
import sqlite3

@dataclass
class UserAccount:
    """
    Entity class representing a user account that contains
    individual information
    """
    accountId: Optional[int]
    fullName: str
    userName: str
    passWord: str
    birthday: Optional[str]
    address: Optional[str]
    contact_number: str
    profileId: int
    accountStatus: str

    @classmethod
    def fromRow(cls, row) -> "UserAccount":
        """
        create a UserAccount instance from a database row
        """
        return cls(
            accountId = row["account_id"],
            fullName = row["full_name"],
            userName = row["username"],
            passWord = row["password"],
            birthday = row["DOB"],
            address = row["address"],
            contact_number = row["contact_num"],
            profileId = row["profile_id"],
            accountStatus = row["account_status"]
            )

    @classmethod
    def usernameExists(cls, userName: str) -> bool:
        """
        Checks if an account with the same username exists
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT 1
            FROM user_account
            WHERE LOWER(username) = LOWER(?)
            """,
            (userName.strip(),)
        )
        row = cursor.fetchone()
        connection.close()
        return row is not None

    @classmethod
    def createAccount(cls, fullName: str, userName: str, passWord: str, birthday: str,
                      address: str, contact_number: str, profileId: int, accountStatus: str = "ACTIVE"):
        """
        Create and store a User Account into database
        """
        fullName = fullName.strip()
        userName = userName.strip()
        passWord = passWord.strip()
        birthday = birthday.strip()
        address = address.strip()
        contact_number = contact_number.strip()
        accountStatus = accountStatus.strip().upper()

        if not fullName:
            raise ValueError("Full name is required.")

        if not userName:
            raise ValueError("Username is required.")

        if not passWord:
            raise ValueError("Password is required.")

        if not contact_number:
            raise ValueError("Contact number is required.")

        valid_statuses = ["ACTIVE", "SUSPENDED", "EXPIRED"]
        if accountStatus not in valid_statuses:
            raise ValueError("Invalid account status.")

        if cls.usernameExists(userName):
            raise ValueError(f"User {userName} already exists.")
        else:
            connection = get_connection()
            cursor = connection.execute(
                """
                INSERT INTO user_account (full_name, username, password, 
                                          DOB, address, contact_num, profile_id, account_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (fullName, userName, passWord,
                 birthday, address, contact_number, profileId, accountStatus)

            )
            connection.commit()
            new_account = cls(
                accountId = cursor.lastrowid,
                fullName = fullName,
                userName = userName,
                passWord = passWord,
                birthday = birthday,
                address = address,
                contact_number = contact_number,
                profileId = profileId,
                accountStatus = accountStatus
            )
            connection.close()
            return new_account

    @classmethod
    def getAllAccounts(cls) -> List["UserAccount"]:
        """
        Return all user accounts from the database
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT account_id, full_name, username, password, DOB, 
            address, contact_num, profile_id, account_status
            FROM user_account
            ORDER BY account_id
            """
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def searchAccounts(clscls, searchTerm: str) -> List["UserAccount"]:
        """
        Search user accounts by name, username, contact number, or status
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"

        cursor = connection.execute(
            """
            SELECT account_id, full_name, username, password, DOB, 
            address, contact_num, profile_id, account_status
            FROM user_account
            WHERE LOWER(full_name) LIKE LOWER(?)
                OR LOWER(username) LIKE LOWER(?)
                OR LOWER(contact_num) LIKE LOWER(?)
                OR LOWER(account_status) LIKE LOWER(?)
            ORDER BY account_id
            """,
            (keyword, keyword, keyword, keyword)
            )
        rows = cursor.fetchall()
        connection.close()
        return [cls.fromRow(row) for row in rows]