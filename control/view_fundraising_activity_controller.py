from typing import List, Optional
from entity.fundraising_activity import FundraisingActivity

class view_fundraising_activity_controller:
    """
    Control class responsible for retrieving fundraising activity details.
    """

    def viewActivities(self) -> List["FundraisingActivity"]:
        """
        Retrieve all Fundraising Activity object.
        """
        return FundraisingActivity.getAllActivities()

    def viewActivityById(self, activity_id: int) -> Optional["FundraisingActivity"]:
        """
        Retrieve a single fundraising activity by ID.
        Also increments view count if activity exists.

        Args:
            activity_id (int)

        Returns:
            FundraisingActivity | None
        """
        activity = FundraisingActivity.getActivityById(activity_id)

        if activity:
            FundraisingActivity.incrementViewCount(activity_id)

        return activity
