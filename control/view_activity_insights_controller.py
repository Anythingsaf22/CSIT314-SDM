from typing import List
from entity.fundraising_activity import FundraisingActivity


class view_activity_insights_controller:
    """
    Control class responsible for retrieving fundraising activity insights.
    """

    def viewInsights(self, account_id: int) -> List["FundraisingActivity"]:
        """
        Retrieve fundraising activities with view and favourite counts.
        """
        return FundraisingActivity.getActivitiesWithInterestCounts(account_id)
