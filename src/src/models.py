from typing import List, Optional

from pydantic import BaseModel, Field


class TenderOpportunity(BaseModel):
    title: str

    buyer: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None

    procurement_portal: Optional[str] = None
    notice_id: Optional[str] = None

    publication_date: Optional[str] = None
    deadline: Optional[str] = None

    estimated_value: Optional[str] = None
    currency: Optional[str] = None

    purchase_or_rental: Optional[str] = None

    url: Optional[str] = None
    source_url: Optional[str] = None

    rink_dimensions: Optional[str] = None
    rink_area_m2: Optional[float] = None

    resurfacer_required: Optional[bool] = None
    refrigeration_required: Optional[bool] = None

    skates_required: Optional[str] = None

    cpv_codes: List[str] = Field(default_factory=list)

    technical_requirements: List[str] = Field(default_factory=list)

    qualification_requirements: List[str] = Field(default_factory=list)

    red_flags: List[str] = Field(default_factory=list)

    relevance_score: int = Field(
        default=0,
        ge=0,
        le=100
    )

    recommendation: str = "investigate"

    evidence: List[str] = Field(default_factory=list)


class TenderScan(BaseModel):
    opportunities: List[TenderOpportunity]
