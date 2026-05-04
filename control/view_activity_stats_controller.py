from typing import Optional, Tuple
from entity.fundraising_activity import FundraisingActivity

class view_activity_stats_controller:

    def getStats(self, activity_id: int) -> Optional[Tuple[int, int]]:
        return FundraisingActivity.getActivityStats(activity_id)
