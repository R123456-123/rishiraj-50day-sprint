from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Optional, Annotated
from enum import Enum

# Section 1 — Validators (field_validator, model_validator)

class PropertyInput(BaseModel):
    address : str
    price : float
    bedrooms : int
    area_sqft : float


    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls,v):
        if v <= 0:
            raise ValueError("Price must be a positive number")
        return v

    @field_validator('address')  
    @classmethod
    def address_must_not_be_empty(cla,v):
        if not v.strip():
            raise ValueError("Address should not be empty")
        return v.strip()

    @model_validator(mode='after')
    def area_per_sqft_is_reasonable(self):
        area_per_sqft = self.price / self.area_sqft
        if area_per_sqft > 100000:
            raise ValueError("It is unreasonalbe value") 
        return self


# now we test it 

def test_validators():
    print("=== Test 1: Valid Input ===")
    p = PropertyInput(address="  Powai Mumbai  ", price=1500000, bedrooms=2, area_sqft=850)
    print(p)

    print("\n=== Test 2: Negative Price ===")
    try:
        p2 = PropertyInput(address="Delhi", price=-100, bedrooms=2, area_sqft=850)
    except Exception as e:
        print(e)

    print("\n=== Test 3: Empty Address ===")
    try:
        p3 = PropertyInput(address="   ", price=500000, bedrooms=2, area_sqft=850)
    except Exception as e:
        print(e)

    print("\n=== Test 4: Unrealistic Price Per Sqft ===")
    try:
        p4 = PropertyInput(address="Mumbai", price=999999999, bedrooms=2, area_sqft=850)
    except Exception as e:
        print(e)


# Section 2 — Computed Fields + Custom Types

PositiveFloat = Annotated[float, Field(gt=0)]
NumCount = Annotated[int, Field(gt=0,lt=20)]

class PropertyValuation(BaseModel):
    address : str
    price : PositiveFloat
    bed_room : NumCount
    area_sqft : PositiveFloat

    @computed_field
    @property
    def price_per_sqft(self) -> float:
        return round(self.price / self.area_sqft, 2)

    @computed_field
    @property
    def tier_prop(self) -> str:
        if self.price_per_sqft < 5000:
            return "Budget Friendly"
        elif self.price_per_sqft < 15000:
            return "Budgeted Luxury"
        else :
            return "Luxury"  


# now we test it 

def test_computed_fields():
    print("\n=== Section 2: Computed Fields ===")
    prop = PropertyValuation(
        address="Bandra Mumbai",
        price=25000000,
        bed_room=3,
        area_sqft=1200
    )
    print(prop)
    print(f"Price per sqft: {prop.price_per_sqft}")
    print(f"Tier: {prop.tier_prop}")
    print(prop.model_dump())  


# Section 3 — Typed LLM Response Wrapper

class SafetyStatus(Enum):
    SAFE = 'safe'
    UNSAFE = 'unsafe'
    UNCERTAIN = 'uncertain'

class ValuationResponse(BaseModel):
    property_id : str
    estimated_value : PositiveFloat
    confidence_score : float = Field(ge=0.0, le=1.0)
    safety_status : SafetyStatus
    reasoning : str
    flags: list[str] = []
    raw_model_output : Optional[str] = None

    @field_validator('confidence_score')
    @classmethod
    def round_confidence(cls,v):
        return round(v,2)

    @computed_field
    @property
    def is_safe(self) -> bool :
        return self.safety_status == SafetyStatus.SAFE

    def to_api_response(self) -> dict:
        data = self.model_dump()
        data.pop('raw_model_output', None)
        data['safety_status'] = self.safety_status.value
        return data

def test_llm_response():
    print("\n=== Section 3: LLM Response Wrapper ===")
    response = ValuationResponse(
        property_id="90210",
        estimated_value=1500000,
        confidence_score=0.8756,
        safety_status=SafetyStatus.SAFE,
        reasoning="Based on comparable sales in the area",
        flags=[],
        raw_model_output="<raw gemini response here>"
    )
    print(response)
    print(f"\nIs safe: {response.is_safe}")
    print(f"\nAPI response:")
    print(response.to_api_response())

    print("\n=== Unsafe Response ===")
    unsafe = ValuationResponse(
        property_id="99999",
        estimated_value=1000,
        confidence_score=0.1,
        safety_status=SafetyStatus.UNSAFE,
        reasoning="Prompt injection detected",
        flags=["prompt_injection", "override_attempt"]
    )
    print(unsafe.to_api_response())



if __name__ == "__main__":
    # test_validators()
    # test_computed_fields()
    test_llm_response()