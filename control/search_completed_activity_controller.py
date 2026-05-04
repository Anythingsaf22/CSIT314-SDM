from typing import Tuple, Optional
from entity.fundraising_activity import FundraisingActivity


class search_completed_activity_controller:
    """
    Control class responsible for searching completed fundraising activities.
    """
    def searchCompletedActivities(self, searchTerm: str) -> Optional["FundraisingActivity"]:
        return FundraisingActivity.searchCompletedActivities(searchTerm)