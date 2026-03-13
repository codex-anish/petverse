from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


# ── Shared ──────────────────────────────────────────
class PetProfile(BaseModel):
    pet_id:    str
    name:      str
    species:   str
    breed:     str
    age_years: float
    weight_kg: float


# ── Feature 1: Triage ───────────────────────────────
class UrgencyLevel(str, Enum):
    CRITICAL = "CRITICAL"
    URGENT   = "URGENT"
    MODERATE = "MODERATE"
    MILD     = "MILD"
    NORMAL   = "NORMAL"

class TriageRequest(BaseModel):
    pet:          PetProfile
    symptom_text: str = Field(..., min_length=5, max_length=1000)

class TriageResponse(BaseModel):
    pet_id:             str
    urgency_level:      UrgencyLevel
    summary:            str
    explanation:        str
    recommended_action: str
    trigger_sos:        bool
    home_care_tips:     list[str]
    disclaimer: str = "AI triage only. Always consult a licensed vet."


# ── Feature 2: Adoption ─────────────────────────────
class ShelterPet(BaseModel):
    pet_id:             str
    name:               str
    species:            str
    breed:              str
    age_years:          float
    size:               str
    energy_level:       str
    bio:                str
    good_with_kids:     bool = True
    good_with_pets:     bool = True
    apartment_friendly: bool = True

class AdoptionMatchRequest(BaseModel):
    adopter_lifestyle_text: str = Field(..., min_length=10, max_length=2000)
    available_pets:         list[ShelterPet]

class PetMatchResult(BaseModel):
    pet_id:              str
    name:                str
    compatibility_score: int = Field(..., ge=0, le=100)
    match_reason:        str
    potential_concerns:  str

class AdoptionMatchResponse(BaseModel):
    ranked_matches: list[PetMatchResult]
    top_pick_id:    str
    summary:        str


# ── Feature 3: Medical OCR ──────────────────────────
class MedicalSummaryResponse(BaseModel):
    pet_id:              str
    known_allergies:     list[str]
    past_surgeries:      list[str]
    current_medications: list[str]
    vaccination_history: list[str]
    vet_notes:           str
    raw_extracted_text:  str
    disclaimer: str = "Always verify extracted data against original documents."


# ── Feature 4: Lost & Found ─────────────────────────
class ExtractedVisualFeatures(BaseModel):
    species:              str
    likely_breeds:        list[str]
    primary_color:        str
    markings:             str
    size_estimate:        str
    coat_type:            str
    distinctive_features: str
    confidence_score:     float = Field(..., ge=0.0, le=1.0)

class LostFoundResponse(BaseModel):
    extracted_features: ExtractedVisualFeatures
    suggested_db_query: dict
    search_tags:        list[str]


# ── Feature 5: Reminders ────────────────────────────
class ReminderRequest(BaseModel):
    pet:                 PetProfile
    current_month:       int   = Field(..., ge=1, le=12)
    current_season:      str   = "summer"
    known_conditions:    list[str] = []
    last_vet_visit_days: int   = 30

class ReminderItem(BaseModel):
    title:    str
    detail:   str
    priority: str
    category: str

class ReminderResponse(BaseModel):
    pet_id:    str
    pet_name:  str
    reminders: list[ReminderItem]
    fun_fact:  str
