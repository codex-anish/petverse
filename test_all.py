# tests/test_all.py
# Run with: pytest tests/ -v
# These tests call your REAL running server.
# Make sure server is running: uvicorn app.main:app --port 8000

import requests

BASE  = "http://localhost:8000"
KEY   = "pawzio-secret-123"   # must match APP_API_KEY in your .env
HEADS = {"X-API-Key": KEY}


def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_triage_critical():
    payload = {
        "pet": {
            "pet_id": "t1", "name": "Buddy", "species": "dog",
            "breed": "Golden Retriever", "age_years": 3, "weight_kg": 28
        },
        "symptom_text": "My dog just ate a large bar of dark chocolate and is vomiting"
    }
    r = requests.post(f"{BASE}/api/v1/triage/symptom-check", json=payload, headers=HEADS)
    print("\nTriage response:", r.json())
    assert r.status_code == 200
    data = r.json()
    assert data["urgency_level"] in ["CRITICAL", "URGENT"]
    assert "recommended_action" in data


def test_triage_mild():
    payload = {
        "pet": {
            "pet_id": "t2", "name": "Mochi", "species": "cat",
            "breed": "Persian", "age_years": 4, "weight_kg": 4
        },
        "symptom_text": "My cat has been scratching her ears more than usual today"
    }
    r = requests.post(f"{BASE}/api/v1/triage/symptom-check", json=payload, headers=HEADS)
    print("\nTriage mild:", r.json())
    assert r.status_code == 200


def test_adoption_match():
    payload = {
        "adopter_lifestyle_text": "I live in a small apartment in Mumbai. I work from home. I prefer calm pets. No kids.",
        "available_pets": [
            {
                "pet_id": "p1", "name": "Luna", "species": "dog",
                "breed": "Greyhound", "age_years": 3, "size": "large",
                "energy_level": "low", "bio": "Calm indoor companion.",
                "good_with_kids": True, "good_with_pets": True, "apartment_friendly": True
            },
            {
                "pet_id": "p2", "name": "Bruno", "species": "dog",
                "breed": "Labrador", "age_years": 1, "size": "large",
                "energy_level": "high", "bio": "Very energetic, loves running.",
                "good_with_kids": True, "good_with_pets": True, "apartment_friendly": False
            },
            {
                "pet_id": "p3", "name": "Mia", "species": "cat",
                "breed": "Persian", "age_years": 2, "size": "small",
                "energy_level": "low", "bio": "Quiet and affectionate.",
                "good_with_kids": False, "good_with_pets": False, "apartment_friendly": True
            }
        ]
    }
    r = requests.post(f"{BASE}/api/v1/adoption/match", json=payload, headers=HEADS)
    print("\nAdoption:", r.json())
    assert r.status_code == 200
    data = r.json()
    assert len(data["ranked_matches"]) == 3
    assert "top_pick_id" in data


def test_reminders():
    payload = {
        "pet": {
            "pet_id": "r1", "name": "Buddy", "species": "dog",
            "breed": "Golden Retriever", "age_years": 3, "weight_kg": 28
        },
        "current_month": 6,
        "current_season": "summer",
        "known_conditions": [],
        "last_vet_visit_days": 60
    }
    r = requests.post(f"{BASE}/api/v1/reminders/generate", json=payload, headers=HEADS)
    print("\nReminders:", r.json())
    assert r.status_code == 200
    data = r.json()
    assert len(data["reminders"]) >= 3
    assert "fun_fact" in data


def test_unauthorized():
    """API key check — should return 401"""
    payload = {
        "pet": {
            "pet_id": "x", "name": "X", "species": "dog",
            "breed": "X", "age_years": 1, "weight_kg": 5
        },
        "symptom_text": "Test symptom"
    }
    r = requests.post(
        f"{BASE}/api/v1/triage/symptom-check",
        json=payload,
        headers={"X-API-Key": "wrong-key"},
    )
    assert r.status_code == 401
