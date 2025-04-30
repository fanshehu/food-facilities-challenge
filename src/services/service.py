import os
from typing import Dict, List, Optional
import pandas as pd
from geopy.distance import geodesic
from src.models.core import Permit, PermitQueryContext


class PermitDataService:
    """
    Core service which:
    1: manage mobile food facility permit data
    2: supports read and search operations on mobile food facility permit data
    """

    DATA_PATH = "./src/data/Mobile_Food_Facility_Permit.csv"
    MAX_RESULTS_LIMIT = 5
    VALID_STATUS = ["APPROVED", "EXPIRED"]

    def __init__(self):
        """
        Initialize the data service with mobil food facility permit data.
        """
        self.df = self._load_data()
        
    def _load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file to pandas DataFrame
        """
        df = pd.read_csv(self.DATA_PATH)
        df['Received'] = df['Received'].apply(str)
        # print(df)
        return df

    def _read_permit(
        self,
        limit: Optional[int] = MAX_RESULTS_LIMIT
    ):
        """
        Read permits. By default, it will return 5 permits
        """
        results = self.df.sample(n=limit)
        return self._to_permit(results)

    def search_permit(
        self,
        query_context: PermitQueryContext
    ) -> List[Permit]:
        """
        Search permit based on given query parameters.
        If no parameter provided, it will return random permits. (Same as read permit operation.)
        It supports 3 types of queries:
        1. Query by applicant name, with status as optional
        2. Query by full or partial address.
        3. Query by geo location (latitude, longitude), with status as optional
        """
        if query_context.applicant:
            applicant = query_context.applicant.strip()
            status = query_context.status
            return self._search_by_applicant(applicant, status)
        if query_context.address:
            address = query_context.address.strip()
            return self._search_by_address(address)
        if query_context.latitude and query_context.longitude:
            return self._search_nearest_location(
                query_context.latitude,
                query_context.longitude,
                query_context.status
            )
        return self._read_permit()

    def _search_by_applicant(
        self,
        applicant: str,
        status: Optional[str] = None):
        """
        Search permit by applicant name and status.
        It supports partial matching for applicant name.
        The search on status is exact match. It's optional.
        """
        filter = self.df['Applicant'].str.contains(applicant, case=False)
        if status:
            filter = filter & (self.df['Status'] == status)
        results = self.df[filter].head(self.MAX_RESULTS_LIMIT)
        return self._to_permit(results)
    
    def _search_by_address(
        self,
        address: str
    ):
        """
        Search permit by street name of address, it supports partial matching.
        """
        filter = self.df['Address'].str.contains(address, case=False)
        results = self.df[filter].head(self.MAX_RESULTS_LIMIT)
        return self._to_permit(results)
    
    def _search_nearest_location(
        self,
        latitude: float, 
        longitude: float, 
        status: Optional[str] = None
    ):
        """
        Find the food facilities permit whose location is nearest to a given location.
        By default, it will return 5 nearest permits.
        It supports filter on permit status.
        """
        if status:
            filtered_df = self.df[self.df['Status'] == status].copy()
        else:
            filtered_df = self.df.copy()
        filtered_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
        
        if filtered_df.empty:
            return []
        
        target_location = (latitude, longitude)
        filtered_df['distance'] = filtered_df.apply(
            lambda row: self._get_geo_distance(
                (row['Latitude'], row['Longitude']), target_location),
            axis = 1)
        nearest = filtered_df.sort_values('distance').head(self.MAX_RESULTS_LIMIT)
        results = self.df.iloc[nearest.index]

        return self._to_permit(results)

    def _get_geo_distance(
        self,
        location1: tuple[float, float],
        location2: tuple[float, float]
    ) -> float:
        return geodesic(location1, location2).miles

    def _to_permit(
        self,
        data_frame: pd.DataFrame
    ) -> List:
        data_dicts = data_frame.replace({float('nan'): None}).to_dict('records')
        permits = [Permit(**data_dicts) for data_dicts in data_dicts]
        return permits



if __name__ == '__main__':
    query_param = {
        # "applicant": "Quan",
        # "status": "EXPIRED",
        # "address": "BAY",
        "Latitude": 37.744178447375724,
        "Longitude": -122.38671592975922,
        "status": "APPROVED"
    }
    service = PermitDataService()
    result = service.search_permit(PermitQueryContext(**query_param))
    print(result[0])