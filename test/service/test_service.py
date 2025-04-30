import pytest
from src.services.service import PermitDataService
from src.models.core import PermitQueryContext


class TestPermitDataService():
    """Test cases for the PermitDataService class."""
        
    def test_search_by_applicant(self):
        """Test searching by applicant name."""

        service = PermitDataService()
        query_param = {
            "applicant": "Pipo's Grill"
        }
        
        # Test search without status filter
        results = service.search_permit(PermitQueryContext(**query_param))
        assert len(results) == 1
        assert results[0].applicant == "Pipo's Grill"
        assert results[0].status == "REQUESTED"

        # Test search with status filter
        query_param = {
            "applicant": "Pipo's Grill",
            "status": "APPROVED",
        }
        results = service.search_permit(PermitQueryContext(**query_param))
        assert len(results) == 0

    def test_search_by_street(self):
        """Test searching by street name."""
        
        service = PermitDataService()
        query_param = {
            "address": "BAY BLVD"
        }
        
        # Test partial street name search
        results = service.search_permit(PermitQueryContext(**query_param))
        assert len(results) == 1
        assert results[0].address == '535 MISSION BAY BLVD SOUTH'

        
    def test_find_nearest(self):
        """Test finding nearest facilities."""
        
        service = PermitDataService()
        
        # Test with default status filter (APPROVED)
        query_param = {
            "latitude": 37.79,
            "longitude": -122.39,
            "status": "APPROVED"
        }
        results = service.search_permit(PermitQueryContext(**query_param))
        assert len(results) == 5  # Only APPROVED facilities
        assert results[0].location_id == 1589659  # Closest facility
        
        # Test with ALL status
        query_param = {
            "latitude": 37.79,
            "longitude": -122.39
        }
        results = service.search_permit(PermitQueryContext(**query_param))
        assert len(results) == 5  # All facilities

