from typing import Optional
from pydantic import BaseModel, field_validator
import pytest


class BookingDates(BaseModel):
    checkin: str
    checkout: str


class Booking(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


class BookingModelResponse(BaseModel):
    bookingid: int
    booking: Booking


class GetBookings(BaseModel):
    bookingid: int
