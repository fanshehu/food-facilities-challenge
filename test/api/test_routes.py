from fastapi.testclient import TestClient
from src.api.routes import router, get_data_service

class TestRoutes:

    def test_search_permit_empty_query(self):
        """
        Test search_permit with an empty query context.
        This tests the edge case where all query parameters are empty or None.
        """
        client = TestClient(router)
        response = client.get("/api/v1/permit")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_search_permit_by_applicant(self):
        """
        Test search_permit with query parameter applicant and status
        """
        client = TestClient(router)
        response = client.get("/api/v1/permit?applicant=Quan&status=EXPIRED")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_search_permit_by_address(self):
        """
        Test search_permit with query parameter address
        """
        client = TestClient(router)
        response = client.get("/api/v1/permit?address=bay")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_search_permit_by_location(self):
        """
        Test search_permit with query parameter latitude, longitude and status
        """
        client = TestClient(router)
        response = client.get("/api/v1/permit?latitude=37.7749&longitude=-122.4194&status=APPROVED")
        assert response.status_code == 200
        assert len(response.json()) == 5