"""
Photoshoot-related Pydantic schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class GarmentUploadType(str, Enum):
    """Garment upload type enum"""
    UPPER_GARMENT = "upper_garment"
    LOWER_GARMENT = "lower_garment"
    ONE_PIECE_GARMENT = "one_piece_garment"


class PoseInputMethod(str, Enum):
    """Pose input method enum"""
    PREDEFINED = "predefined"
    UPLOAD = "upload"
    PROMPTS = "prompts"


class Gender(str, Enum):
    """Gender enum"""
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"


class AgeGroup(str, Enum):
    """Age group enum"""
    CHILD = "child"
    TEEN = "teen"
    ADULT = "adult"
    SENIOR = "senior"


class Ethnicity(str, Enum):
    """Ethnicity enum"""
    ASIAN = "asian"
    CAUCASIAN = "caucasian"
    AFRICAN = "african"
    HISPANIC = "hispanic"
    MIDDLE_EASTERN = "middle_eastern"
    MIXED = "mixed"


class Fitting(str, Enum):
    """Fitting enum"""
    SLIM = "slim"
    REGULAR = "regular"
    LOOSE = "loose"
    OVERSIZED = "oversized"


class PhotoshootStatus(str, Enum):
    """Photoshoot status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class PhotoshootCreate(BaseModel):
    """Photoshoot creation schema"""
    garment_upload_type: GarmentUploadType
    age_group: AgeGroup
    gender: Gender
    ethnicity: Ethnicity
    height: int = Field(..., ge=100, le=250)
    width: int = Field(..., ge=100, le=250)
    fitting: Fitting
    background_description: Optional[str] = None
    selected_background: Optional[str] = None
    age: int = Field(default=25, ge=1, le=100)
    upper_garment_type: Optional[str] = None
    upper_garment_specs: Optional[str] = None
    lower_garment_type: Optional[str] = None
    lower_garment_specs: Optional[str] = None
    pose_input_method: PoseInputMethod = PoseInputMethod.PREDEFINED
    selected_poses: List[str] = Field(default_factory=list)
    pose_descriptions: List[str] = Field(default_factory=list)


class PhotoshootResponse(BaseModel):
    """Photoshoot response schema"""
    id: str
    photoshoot_id: str
    upload_garment_type: str
    age_group: str
    gender: str
    ethnicity: str
    height: int
    width: int
    fitting: str
    background_description: Optional[str] = None
    selected_background: Optional[str] = None
    age: int
    upper_garment_type: Optional[str] = None
    upper_garment_specs: Optional[str] = None
    lower_garment_type: Optional[str] = None
    lower_garment_specs: Optional[str] = None
    pose_input_method: str
    selected_poses: List[str]
    pose_descriptions: List[str]
    all_images: List[str] = Field(default_factory=list)
    total_credit: int = 0
    is_credit_debited: bool = False
    is_completed: bool = False
    status: str = "pending"
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PhotoshootListResponse(BaseModel):
    """Photoshoot list response schema"""
    success: bool = True
    data: List[PhotoshootResponse]
    total: int


class PhotoshootDetailResponse(BaseModel):
    """Photoshoot detail response schema"""
    success: bool = True
    data: PhotoshootResponse


class PhotoshootFilter(BaseModel):
    """Photoshoot filter schema"""
    status: Optional[str] = "all"
    garment_type: Optional[str] = "all"
    gender: Optional[str] = "all"
    age_group: Optional[str] = "all"

