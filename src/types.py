from pydantic import BaseModel, field_validator
from datetime import datetime
import re


class DriversLicense(BaseModel):
    state: str
    license_number: str
    expr: str  # Date in form (mm/dd/yyyy)
    license_class: str  # Should be single char
    address: str  # number street, town, state, zip
    dob: str  # Date in form (mm/dd/yyyy)
    isVeteran: bool
    isOrganDonor: str
    isMale: bool
    heightFeet: int
    heightInches: int
    hair: str
    weight: int
    eyes: str
    issues_date: str  # Date in form (mm/dd/yyyy)
    dd: str
    signature_name: str
    end: str

    @field_validator('expr', 'dob', 'issues_date')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%m/%d/%Y')
            return v
        except ValueError:
            raise ValueError('Date must be in format mm/dd/yyyy')

    @field_validator('address')
    def validate_address(cls, v):
        # Basic address format validation
        address_pattern = r'^\d+\s+[A-Za-z0-9\s\.]+(,\s*[A-Za-z\s]+){2},\s*[A-Z]{2}\s+\d{5}(-\d{4})?$'
        if not re.match(address_pattern, v):
            raise ValueError('Invalid address format. Must be: number street, town, state, zip')

        # Verify street name contains valid characters
        street_part = v.split(',')[0]
        street_name = ' '.join(street_part.split()[1:])  # Remove house number
        if not re.match(r'^[A-Za-z0-9\s\.]+$', street_name):
            raise ValueError('Street name contains invalid characters')

        return v

    @field_validator('license_class')
    def validate_license_class(cls, v):
        if len(v) != 1:
            raise ValueError('License class must be a single character')
        return v


class Passport(BaseModel):
    first_name: str
    last_name: str
    nationality: str
    date_of_birth: str  # dd MMM YYYYY (ie 15 MAR 1996)
    place_of_birth: str
    date_of_issue: str  # dd MMM YYYYY (ie 15 MAR 1996)
    isMale: bool
    authority: str
    number_at_bottom: str

    @field_validator('date_of_birth', 'date_of_issue')
    def validate_passport_date(cls, v):
        try:
            datetime.strptime(v, '%d %b %Y')
            return v
        except ValueError:
            raise ValueError('Date must be in format dd MMM YYYY (e.g., 15 MAR 1996)')

    @field_validator('place_of_birth')
    def validate_place_name(cls, v):
        if not re.match(r'^[A-Za-z\s\.,\'-]+$', v):
            raise ValueError('Place of birth contains invalid characters')
        return v
