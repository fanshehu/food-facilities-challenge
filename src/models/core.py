from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Permit(BaseModel):
    """
    Represents a Mobile Food Facility Permit,
    including name of vendor, location, type of food sold and status of permit.
    """

    location_id: int = Field(..., alias="locationid", description="Location id of facility")
    permit: str = Field(..., description="Permit number")
    status: str = Field(..., alias="Status", description="Status of permit: Approved or Requested")
    food_items: Optional[str] = Field(None, alias="FoodItems", description="A description of food items sold")
    x: Optional[float] = Field(None, alias="X", description="CA State Plane III")
    y: Optional[float] = Field(None, alias="Y", description="CA State Plane III")
    latitude: Optional[float] = Field(None, alias="Latitude", description="WGS84, latitude")
    longitude: Optional[float] = Field(None, alias="Longitude", description="WGS84, longitude")
    schedule: Optional[str] = Field(None, alias="Schedule", description="URL link to Schedule for facility")
    days_hours: Optional[str] = Field(None, alias="dayshours", description="abbreviated text of schedule")
    noi_sent: Optional[datetime] = Field(None, alias="NOISent", description="Date notice of intent sent")
    applicant: Optional[str] = Field(None, alias="Applicant", description="Name of permit holder")
    approved: Optional[str] = Field(None, alias="Approved", description="Date permit approved by DPW")
    received: Optional[str] = Field(None, alias="Received", description="Date permit application received from applicant")
    prior_permit: Optional[int] = Field(None, alias="PriorPermit", description="prior existing permit with SFFD")
    expiration_date: Optional[str] = Field(None, alias="ExpirationDate", description="Date permit expires")
    location: Optional[str] = Field(None, alias="Location", description="Location formatted for mapping")
    facility_type: Optional[str] = Field(None, alias="FacilityType", description="Type of facilty permitted: truck or push cart")
    cnn: Optional[int] = Field(None, alias="cnn", description="CNN of street segment or intersection location")
    location_description: Optional[str] = Field(None, alias="LocationDescription", description="Description of street segment or intersection location")
    address: Optional[str] = Field(None, alias="Address", description="Address")
    blocklot: Optional[str] = Field(None, alias="blocklot", description="Block lot (parcel) number")
    block: Optional[str] = Field(None, alias="block", description="Block number")
    lot: Optional[str] = Field(None, alias="lot", description="Lot number")

    class Config:
        allow_population_by_field_name = True
        extra = 'ignore'

class PermitQueryContext(BaseModel):
    """
    Represents the query parameters and values for a permit search request.
    """

    applicant: Optional[str] = Field(default=None, description="Name or partial name of the applicant")
    address: Optional[str] = Field(default=None, description="Address name or partial address name")
    status: Optional[str] = Field(default=None, description="Status filter (e.g., APPROVED, EXPIRED)")
    latitude: Optional[float] = Field(default=None, description="Latitude coordinate")
    longitude: Optional[float] = Field(default=None, description="Longitude coordinate")