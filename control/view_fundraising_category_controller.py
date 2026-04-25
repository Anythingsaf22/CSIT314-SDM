from typing import List
from entity.fundraising_category import FundraisingCategory

class view_fundraising_category_controller:
    """
    Control class responsible for retrieving fundraising category details.
    """

    def viewFundraisingCategory(self) -> List["FundraisingCategory"]:
        """
        Retrieve all fundraising category object.
        """
        return FundraisingCategory.getAllCategories()