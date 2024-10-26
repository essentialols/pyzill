from typing import Any, List

from requests import put # type: ignore

def for_sale(
    pagination: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    custom_region_id: Optional[str] = None,
    proxy_url: str | None = None,
) -> dict[str, Any]:
    """get results of the listing that are for sale, you will get a dictionary with the keywords
    mapResults and listResults, use mapResults which contains all the listings from all paginations
    listResults is more for the right side bar that you see when searching on zillow. 
    Be aware the the maximum size of mapResults is 500 so if you get results with size 500, so if you want 
    to get the whole result frm a particular area, you need to play with the zoom, or the coordinates.
    Even if you try to paginate over all results, it won't work even if you use mapResults or listResults
    I would recomend not use pagination because you have all results(with 500 maximum) on mapResults
    Args:
        pagination (int): number of page in pagination
        ne_lat (float): ne latitude value
        ne_long (float): ne longitude value
        sw_lat (float): sw latitude value
        sw_long (float): sw longitude value
        sw_long (float): sw longitude value
        proxy_url (str | None, optional): proxy URL for masking the request. Defaults to None.

    Returns:
        dict[str, Any]: listing of properties in JSON format
    """
    rent = {
		"sortSelection":  {"value": "globalrelevanceex"},
		"isAllHomes":  {"value": True},
	}
    return search(pagination,ne_lat,ne_long,sw_lat,sw_long,zoom_value,rent,proxy_url)

def for_rent(
    pagination: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    proxy_url: Optional[str] = None,
    polygon: Optional[List[Dict[str, float]]] = None  # Add polygon parameter here
) -> dict[str, Any]:
    rent = {
        "sortSelection": {"value": "priorityscore"},
        "isNewConstruction": {"value": False},
        "isForSaleForeclosure": {"value": False},
        "isForSaleByOwner": {"value": False},
        "isForSaleByAgent": {"value": False},
        "isForRent": {"value": True},
        "isComingSoon": {"value": False},
        "isAuction": {"value": False},
        "isAllHomes": {"value": True},
    }
    return search(pagination, ne_lat, ne_long, sw_lat, sw_long, zoom_value, rent, proxy_url, polygon=polygon)

def sold(
    pagination: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    proxy_url: str | None = None,
) -> dict[str, Any]:
    """get results of the listing that were sold, you will get a dictionary with the keywords
    mapResults and listResults, use mapResults which contains all the listings from all paginations
    listResults is more for the right side bar that you see when searching on zillow. 
    Be aware the the maximum size of mapResults is 500 so if you get results with size 500, so if you want 
    to get the whole result frm a particular area, you need to play with the zoom, or the coordinates.
    Even if you try to paginate over all results, it won't work even if you use mapResults or listResults
    I would recomend not use pagination because you have all results(with 500 maximum) on mapResults
    Args:
        pagination (int): number of page in pagination
        ne_lat (float): ne latitude value
        ne_long (float): ne longitude value
        sw_lat (float): sw latitude value
        sw_long (float): sw longitude value
        sw_long (float): sw longitude value
        proxy_url (str | None, optional): proxy URL for masking the request. Defaults to None.

    Returns:
        dict[str, Any]: listing of properties in JSON format
    """
    rent = {
		"sortSelection":  {"value": "globalrelevanceex"},
		"isNewConstruction":  {"value": False},
		"isForSaleForeclosure":  {"value": False},
		"isForSaleByOwner":  {"value": False},
		"isForSaleByAgent":  {"value": False},
		"isForRent":  {"value": False},
		"isComingSoon":  {"value": False},
		"isAuction":  {"value": False},
		"isAllHomes":  {"value": True},
		"isRecentlySold":  {"value": True},
	}
    return search(pagination,ne_lat,ne_long,sw_lat,sw_long,zoom_value,rent,proxy_url)



def search(
    pagination: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    filter_state: dict[str, Any],
    proxy_url: Optional[str] = None,
    polygon: Optional[List[Dict[str, float]]] = None  # Add polygon parameter here
) -> dict[str, Any]:
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    # Create searchQueryState, using polygon if provided
    search_query_state = {
        "isMapVisible": True,
        "isListVisible": True,
        "mapZoom": zoom_value,
        "filterState": filter_state,
        "pagination": {"currentPage": pagination},
        "category": "cat1"
    }

    if polygon:
        # Use polygon as mapBounds
        search_query_state["mapBounds"] = {"polygon": polygon}
    else:
        # Fallback to bounding box
        search_query_state["mapBounds"] = {
            "north": ne_lat,
            "east": ne_long,
            "south": sw_lat,
            "west": sw_long,
        }

    inputData = {
        "searchQueryState": search_query_state,
        "wants": {"cat1": ["listResults", "mapResults"], "cat2": ["total"]},
        "requestId": 10,
        "isDebugRequest": False,
    }

    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    response = requests.put(
        url="https://www.zillow.com/async-create-search-page-state",
        json=inputData,
        headers=headers,
        proxies=proxies,
    )
    data = response.json()
    return data.get("cat1", {}).get("searchResults", {})
