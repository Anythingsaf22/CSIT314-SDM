from typing import Tuple, Optional
from entity.fundraising_activity import FundraisingActivity


class class search_fundraising_activity_controller:
    """
    Control class responsible for searching fundraising activity.
    """
    def searchActivities(self, keyword: str) -> List["FundraisingActivity"]:
        return FundraisingActivity.searchActivities(keyword)
