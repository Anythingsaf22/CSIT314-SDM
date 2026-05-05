from entity.favourite_list import FavouriteList


class view_favourite_controller:

    def viewFavourites(self, accountId: int):
        return FavouriteList.getFavouritesByAccountId(accountId)
