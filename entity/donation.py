from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
import sqlite3

@dataclass
class donation:
    """
    Entity class representing a donation.
    """
    donationId: Optional[int]
    accountId: int
    activityId: int
    donationAmount: float
    donationDate: str
    activityName: str
    activityCategory: str

    @classmethod
    def fromRow(cls, row) -> "donation":
        """
        Create a donation instance from a database row
        """
        return cls(
            donationId=row["donation_id"],
            accountId=row["account_id"],
            activityId=row["activity_id"],
            activityName=row["activity_name"],
            activityCategory=row["category_name"],
            donationAmount=row["donation_amount"],
            donationDate=row["donation_date"]
        )
    
    @classmethod
    def viewMyDonations(cls, accountId: int) -> List["donation"]:
        """
        Retrieve all donations from the database and return them as a list of donation instances.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT d.donation_id, d.account_id, d.activity_id, fra.activity_name, c.category_name, d.donation_amount, d.donation_date
            FROM donation d
            JOIN fundraising_activity fra ON d.activity_id = fra.activity_id
            JOIN category c ON fra.category_id = c.category_id
            WHERE d.account_id = ?
            """
        , (accountId,))

        rows = cursor.fetchall()
        connection.close()
        return [cls.fromRow(row) for row in rows]
    
    @classmethod
    def searchMyDonations(cls, accountId: int, searchTerm: str) -> List["donation"]:
        """
        Search for donations based on the search term and return them as a list of donation instances.
        The search term is matched against the activity name and category name.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT d.donation_id, d.account_id, d.activity_id, fra.activity_name, c.category_name, d.donation_amount, d.donation_date
            FROM donation d
            JOIN fundraising_activity fra ON d.activity_id = fra.activity_id
            JOIN category c ON fra.category_id = c.category_id
            WHERE d.account_id = ?
            AND (LOWER(fra.activity_name) LIKE LOWER(?) OR LOWER(c.category_name) LIKE LOWER(?))
            """, (accountId, f"%{searchTerm}%", f"%{searchTerm}%")
        )

        rows = cursor.fetchall()
        connection.close()
        return [cls.fromRow(row) for row in rows]