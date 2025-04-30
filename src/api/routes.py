from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.core import (
    Permit,
    PermitQueryContext,
)
from src.services.service import PermitDataService


"""
API routes for the Permit data application.
"""


router = APIRouter(prefix="/api/v1", tags=["Permit Data API"])


def get_data_service() -> PermitDataService:
    """Dependency to get the data service instance.
    
    Returns:
        PermitDataService instance
    """
    # Path to the CSV file relative to the project root
    return PermitDataService()

@router.get("/permit", response_model=List[Permit])
async def search_permit(
    query_context: Annotated[PermitQueryContext, Query()],
    data_service: PermitDataService = Depends(get_data_service),
) -> List[Permit]:
    """
    Search permits by given query parameters
    """
    # query_context = PermitQueryContext(
    #     applicant = name,
    #     address = street,
    #     status = status,
    #     latitude = latitude,
    #     longitude = longitude,
    # )
    print(f"Receiving search permit request with query parameter: {query_context}")
    results = data_service.search_permit(query_context)
    print("Search permit request succeed!")
    return results

