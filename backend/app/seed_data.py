"""Project Vishnu — Demo Seed Data

Operation Nightfall: A fictional intelligence investigation scenario
involving a terrorist financing network spanning multiple countries.

This creates ~25 entities (persons, organisations, locations, vehicles,
events, documents) and ~45 relationships to give new users a rich demo
dataset to explore the graph workspace immediately.
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.entity import Entity
from app.models.relationship import Relationship


def _id() -> str:
    return str(uuid.uuid4())


def seed(db: Session) -> dict[str, Any]:
    """Insert the Operation Nightfall demo dataset. Idempotent — skips if data exists."""
    existing = db.query(Entity).count()
    if existing > 0:
        return {"message": "Database already contains data. Seed skipped.", "seeded": False}

    # ── Persons ──────────────────────────────────────────────────────────
    persons = {
        "Viktor Sorokin": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Russian", "date_of_birth": "1975-03-12", "threat_level": "HIGH", "aliases": ["The Architect", "V. Sorokin"]},
            "desc": "Suspected financier and orchestrator of a transnational money laundering network. Former banking executive with ties to Eastern European criminal syndicates.",
            "confidence": 0.92, "classification": "SECRET", "tags": ["HVT", "financier", "nightfall"],
        },
        "Amara Osei": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Ghanaian", "date_of_birth": "1988-07-22", "threat_level": "MEDIUM", "role": "Logistics Coordinator"},
            "desc": "Logistics coordinator suspected of arranging shipments of precursor materials through West African ports.",
            "confidence": 0.85, "classification": "CONFIDENTIAL", "tags": ["logistics", "nightfall"],
        },
        "Chen Wei": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Chinese", "date_of_birth": "1982-11-05", "threat_level": "HIGH", "role": "Technology Specialist"},
            "desc": "Cybersecurity expert believed to provide encrypted communications infrastructure for the network.",
            "confidence": 0.78, "classification": "SECRET", "tags": ["cyber", "comms", "nightfall"],
        },
        "Fatima Al-Rashid": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Jordanian", "date_of_birth": "1990-01-15", "threat_level": "MEDIUM", "role": "Courier"},
            "desc": "Suspected courier who travels frequently between Amman, Istanbul, and Dubai carrying encrypted devices.",
            "confidence": 0.70, "classification": "CONFIDENTIAL", "tags": ["courier", "nightfall"],
        },
        "Marco Bellini": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Italian", "date_of_birth": "1969-09-30", "threat_level": "LOW", "role": "Money Launderer"},
            "desc": "Italian businessman operating a chain of import/export companies used as fronts for money laundering.",
            "confidence": 0.88, "classification": "SECRET", "tags": ["finance", "fronts", "nightfall"],
        },
        "Yuki Tanaka": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Japanese", "date_of_birth": "1993-04-18", "threat_level": "LOW", "role": "Analyst"},
            "desc": "Financial analyst at Meridian Holdings suspected of creating shell company structures.",
            "confidence": 0.65, "classification": "CONFIDENTIAL", "tags": ["finance", "nightfall"],
        },
        "Dmitri Volkov": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Russian", "date_of_birth": "1980-12-01", "threat_level": "HIGH", "role": "Enforcer"},
            "desc": "Former GRU operative suspected of providing security and enforcement for Sorokin's operations.",
            "confidence": 0.91, "classification": "TOP_SECRET", "tags": ["military", "enforcement", "nightfall"],
        },
        "Priya Sharma": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Indian", "date_of_birth": "1986-06-25", "threat_level": "MEDIUM", "role": "Hawala Broker"},
            "desc": "Operates an informal hawala network transferring funds between Mumbai, Dubai, and Nairobi.",
            "confidence": 0.80, "classification": "SECRET", "tags": ["hawala", "finance", "nightfall"],
        },
        "Hassan El-Masri": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Egyptian", "date_of_birth": "1978-08-14", "threat_level": "MEDIUM"},
            "desc": "Cairo-based arms dealer with connections to multiple North African militant groups.",
            "confidence": 0.75, "classification": "SECRET", "tags": ["arms", "nightfall"],
        },
        "Elena Vasquez": {
            "id": _id(), "type": "person",
            "props": {"nationality": "Colombian", "date_of_birth": "1991-02-28", "threat_level": "LOW", "role": "Recruiter"},
            "desc": "University lecturer suspected of recruiting technical talent for cyber operations.",
            "confidence": 0.55, "classification": "RESTRICTED", "tags": ["recruitment", "nightfall"],
        },
    }

    # ── Organisations ────────────────────────────────────────────────────
    orgs = {
        "Meridian Holdings Ltd": {
            "id": _id(), "type": "organization",
            "props": {"org_type": "corporation", "country": "Cyprus", "industry": "Import/Export", "employees": 120},
            "desc": "Shell company network headquartered in Limassol, Cyprus. Primary vehicle for laundering proceeds through trade-based schemes.",
            "confidence": 0.90, "classification": "SECRET", "tags": ["shell_company", "nightfall"],
        },
        "Crescent Shipping LLC": {
            "id": _id(), "type": "organization",
            "props": {"org_type": "corporation", "country": "UAE", "industry": "Maritime Logistics"},
            "desc": "Dubai-based shipping company used to transport goods as cover for illicit financial transfers.",
            "confidence": 0.82, "classification": "CONFIDENTIAL", "tags": ["shipping", "nightfall"],
        },
        "Nova Consulting Group": {
            "id": _id(), "type": "organization",
            "props": {"org_type": "corporation", "country": "Singapore", "industry": "IT Consulting"},
            "desc": "Technology consulting firm providing encrypted communications platforms. Front for cyber operations.",
            "confidence": 0.70, "classification": "SECRET", "tags": ["cyber", "nightfall"],
        },
        "Al-Noor Foundation": {
            "id": _id(), "type": "organization",
            "props": {"org_type": "NGO", "country": "Jordan", "stated_purpose": "Humanitarian Aid"},
            "desc": "Ostensible charity suspected of diverting humanitarian aid funds to finance network operations.",
            "confidence": 0.60, "classification": "CONFIDENTIAL", "tags": ["charity_front", "nightfall"],
        },
        "Ural Mining Corp": {
            "id": _id(), "type": "organization",
            "props": {"org_type": "corporation", "country": "Russia", "industry": "Mining"},
            "desc": "Russian mining company with opaque ownership structure tied to Sorokin's business interests.",
            "confidence": 0.85, "classification": "SECRET", "tags": ["mining", "nightfall"],
        },
    }

    # ── Locations ────────────────────────────────────────────────────────
    locations = {
        "Limassol Safe House": {
            "id": _id(), "type": "location",
            "props": {"lat": 34.6823, "lon": 33.0464, "location_type": "facility", "country": "Cyprus"},
            "desc": "Residential property used for operational meetings and document storage.",
            "confidence": 0.88, "classification": "SECRET", "tags": ["safehouse", "nightfall"],
        },
        "Dubai Marina Office": {
            "id": _id(), "type": "location",
            "props": {"lat": 25.0805, "lon": 55.1403, "location_type": "office", "country": "UAE"},
            "desc": "Crescent Shipping's registered office in Dubai Marina. Meeting point for network principals.",
            "confidence": 0.92, "classification": "CONFIDENTIAL", "tags": ["office", "nightfall"],
        },
        "Mumbai Hawala Hub": {
            "id": _id(), "type": "location",
            "props": {"lat": 19.0760, "lon": 72.8777, "location_type": "facility", "country": "India"},
            "desc": "Informal money exchange hub in Mumbai's business district handling large cross-border transfers.",
            "confidence": 0.75, "classification": "SECRET", "tags": ["hawala", "nightfall"],
        },
        "Istanbul Grand Bazaar Drop": {
            "id": _id(), "type": "location",
            "props": {"lat": 41.0106, "lon": 28.9685, "location_type": "address", "country": "Turkey"},
            "desc": "Dead-drop location within the Grand Bazaar used for passing encrypted devices and documents.",
            "confidence": 0.65, "classification": "CONFIDENTIAL", "tags": ["dead_drop", "nightfall"],
        },
        "Tema Port, Ghana": {
            "id": _id(), "type": "location",
            "props": {"lat": 5.6333, "lon": -0.0167, "location_type": "port", "country": "Ghana"},
            "desc": "Major port used for routing shipments of goods used in trade-based money laundering.",
            "confidence": 0.80, "classification": "CONFIDENTIAL", "tags": ["port", "nightfall"],
        },
    }

    # ── Vehicles ─────────────────────────────────────────────────────────
    vehicles = {
        "MV Caspian Star": {
            "id": _id(), "type": "vehicle",
            "props": {"vehicle_type": "ship", "identifier": "IMO-9876543", "flag": "Panama", "tonnage": 15000},
            "desc": "Bulk carrier registered in Panama. Frequently routes between Black Sea and West African ports.",
            "confidence": 0.85, "classification": "CONFIDENTIAL", "tags": ["maritime", "nightfall"],
        },
        "Cessna Citation CJ4": {
            "id": _id(), "type": "vehicle",
            "props": {"vehicle_type": "aircraft", "identifier": "VP-CAZ", "registration": "Cayman Islands"},
            "desc": "Private jet linked to Meridian Holdings. Used for rapid transport of network principals.",
            "confidence": 0.78, "classification": "SECRET", "tags": ["aviation", "nightfall"],
        },
    }

    # ── Events ───────────────────────────────────────────────────────────
    events = {
        "Limassol Meeting - Mar 2024": {
            "id": _id(), "type": "event",
            "props": {"event_type": "meeting", "date_occurred": "2024-03-15", "severity": "HIGH"},
            "desc": "Observed gathering of 4 network principals at the Limassol safe house. Surveillance indicates discussion of new routing through West Africa.",
            "confidence": 0.90, "classification": "TOP_SECRET", "tags": ["meeting", "surveillance", "nightfall"],
        },
        "$2.3M Wire Transfer - Jan 2024": {
            "id": _id(), "type": "event",
            "props": {"event_type": "financial_transaction", "date_occurred": "2024-01-22", "severity": "HIGH", "amount": 2300000, "currency": "USD"},
            "desc": "Suspicious wire transfer from Meridian Holdings (Cyprus) to Crescent Shipping (UAE) with no corresponding trade documentation.",
            "confidence": 0.95, "classification": "SECRET", "tags": ["finance", "suspicious", "nightfall"],
        },
        "Encrypted Device Handoff - Feb 2024": {
            "id": _id(), "type": "event",
            "props": {"event_type": "handoff", "date_occurred": "2024-02-10", "severity": "MEDIUM"},
            "desc": "Fatima Al-Rashid observed at Istanbul Grand Bazaar passing a package to an unidentified contact.",
            "confidence": 0.70, "classification": "CONFIDENTIAL", "tags": ["tradecraft", "nightfall"],
        },
    }

    # ── Documents ────────────────────────────────────────────────────────
    documents = {
        "SIGINT Report NF-2024-0042": {
            "id": _id(), "type": "document",
            "props": {"doc_type": "intelligence_report", "date_published": "2024-04-01"},
            "desc": "Signals intelligence report detailing intercepted communications between Sorokin and Chen Wei discussing new encryption protocols.",
            "confidence": 0.92, "classification": "TOP_SECRET", "tags": ["SIGINT", "nightfall"],
        },
        "Financial Analysis - Meridian Network": {
            "id": _id(), "type": "document",
            "props": {"doc_type": "financial_analysis", "date_published": "2024-03-20"},
            "desc": "Detailed analysis of fund flows through the Meridian Holdings shell company network spanning 12 jurisdictions.",
            "confidence": 0.88, "classification": "SECRET", "tags": ["finance", "analysis", "nightfall"],
        },
    }

    # ── Insert all entities ──────────────────────────────────────────────
    all_entities = {}
    for collection in [persons, orgs, locations, vehicles, events, documents]:
        for name, data in collection.items():
            entity = Entity(
                id=data["id"],
                entity_type=data["type"],
                name=name,
                description=data["desc"],
                properties=json.dumps(data["props"]),
                tags=json.dumps(data["tags"]),
                confidence_score=data["confidence"],
                classification_level=data["classification"],
                source="operation_nightfall",
            )
            db.add(entity)
            all_entities[name] = data["id"]

    # ── Insert relationships ─────────────────────────────────────────────
    relationships_data = [
        # Sorokin's network
        ("Viktor Sorokin", "Meridian Holdings Ltd", "OWNS", 0.95, "Beneficial owner through nominee structure"),
        ("Viktor Sorokin", "Ural Mining Corp", "OWNS", 0.88, "Majority shareholder via offshore trust"),
        ("Viktor Sorokin", "Dmitri Volkov", "COMMANDS", 0.90, "Volkov provides security and enforcement"),
        ("Viktor Sorokin", "Marco Bellini", "ASSOCIATED_WITH", 0.85, "Long-standing business relationship"),
        ("Viktor Sorokin", "Chen Wei", "ASSOCIATED_WITH", 0.78, "Encrypted communications observed"),
        ("Viktor Sorokin", "Limassol Safe House", "LOCATED_AT", 0.92, "Primary residence when in Cyprus"),

        # Bellini's operations
        ("Marco Bellini", "Meridian Holdings Ltd", "WORKS_FOR", 0.90, "Managing Director"),
        ("Marco Bellini", "Crescent Shipping LLC", "ASSOCIATED_WITH", 0.80, "Board advisor"),
        ("Marco Bellini", "Yuki Tanaka", "COMMANDS", 0.75, "Directs shell company creation"),

        # Yuki's role
        ("Yuki Tanaka", "Meridian Holdings Ltd", "WORKS_FOR", 0.95, "Financial analyst"),
        ("Yuki Tanaka", "Nova Consulting Group", "ASSOCIATED_WITH", 0.60, "Contracted IT services"),

        # Logistics chain
        ("Amara Osei", "Crescent Shipping LLC", "WORKS_FOR", 0.82, "Logistics coordinator"),
        ("Amara Osei", "Tema Port, Ghana", "LOCATED_AT", 0.88, "Based near Tema port"),
        ("Amara Osei", "MV Caspian Star", "ASSOCIATED_WITH", 0.75, "Arranges cargo loading"),

        # Courier network
        ("Fatima Al-Rashid", "Al-Noor Foundation", "WORKS_FOR", 0.70, "Field coordinator cover"),
        ("Fatima Al-Rashid", "Istanbul Grand Bazaar Drop", "TRAVELED_TO", 0.80, "Observed at dead drop"),
        ("Fatima Al-Rashid", "Dubai Marina Office", "TRAVELED_TO", 0.85, "Frequent visitor"),
        ("Fatima Al-Rashid", "Chen Wei", "COMMUNICATED_WITH", 0.65, "Encrypted messages intercepted"),

        # Cyber operations
        ("Chen Wei", "Nova Consulting Group", "OWNS", 0.85, "Founder and CTO"),
        ("Chen Wei", "Cessna Citation CJ4", "ASSOCIATED_WITH", 0.70, "Passenger on multiple flights"),

        # Financial network
        ("Priya Sharma", "Mumbai Hawala Hub", "LOCATED_AT", 0.90, "Operates from this location"),
        ("Priya Sharma", "Crescent Shipping LLC", "FUNDED_BY", 0.75, "Receives funds for distribution"),
        ("Priya Sharma", "Viktor Sorokin", "REPORTS_TO", 0.70, "Reports financial flows"),

        # Arms connection
        ("Hassan El-Masri", "Dmitri Volkov", "ASSOCIATED_WITH", 0.72, "Arms procurement relationship"),
        ("Hassan El-Masri", "Al-Noor Foundation", "FUNDED_BY", 0.60, "Receives diverted aid funds"),

        # Recruitment
        ("Elena Vasquez", "Nova Consulting Group", "ASSOCIATED_WITH", 0.55, "Recruits talent"),
        ("Elena Vasquez", "Chen Wei", "REPORTS_TO", 0.60, "Provides recruited operatives"),

        # Organisational links
        ("Meridian Holdings Ltd", "Crescent Shipping LLC", "ASSOCIATED_WITH", 0.90, "Trade-based laundering vehicle"),
        ("Meridian Holdings Ltd", "Limassol Safe House", "LOCATED_AT", 0.88, "Registered address nearby"),
        ("Crescent Shipping LLC", "Dubai Marina Office", "LOCATED_AT", 0.95, "Registered office"),
        ("Crescent Shipping LLC", "MV Caspian Star", "OWNS", 0.92, "Vessel operator"),
        ("Crescent Shipping LLC", "Tema Port, Ghana", "ASSOCIATED_WITH", 0.80, "Regular port of call"),
        ("Al-Noor Foundation", "Priya Sharma", "FUNDED_BY", 0.55, "Fund transfers via hawala"),
        ("Ural Mining Corp", "Meridian Holdings Ltd", "SUPPLIER_OF", 0.85, "Paper trail for mining exports"),

        # Vehicle links
        ("MV Caspian Star", "Tema Port, Ghana", "TRAVELED_TO", 0.90, "AIS data confirms route"),
        ("Cessna Citation CJ4", "Dubai Marina Office", "TRAVELED_TO", 0.80, "Flight records"),
        ("Cessna Citation CJ4", "Limassol Safe House", "TRAVELED_TO", 0.78, "Flight records"),

        # Event participation
        ("Viktor Sorokin", "Limassol Meeting - Mar 2024", "PARTICIPATED_IN", 0.95, "Primary organiser"),
        ("Marco Bellini", "Limassol Meeting - Mar 2024", "PARTICIPATED_IN", 0.90, "Attended"),
        ("Dmitri Volkov", "Limassol Meeting - Mar 2024", "PARTICIPATED_IN", 0.88, "Provided security"),
        ("Chen Wei", "Limassol Meeting - Mar 2024", "PARTICIPATED_IN", 0.85, "Attended"),
        ("Meridian Holdings Ltd", "$2.3M Wire Transfer - Jan 2024", "PARTICIPATED_IN", 0.95, "Sender"),
        ("Crescent Shipping LLC", "$2.3M Wire Transfer - Jan 2024", "PARTICIPATED_IN", 0.95, "Receiver"),
        ("Fatima Al-Rashid", "Encrypted Device Handoff - Feb 2024", "PARTICIPATED_IN", 0.80, "Courier"),

        # Document links
        ("Viktor Sorokin", "SIGINT Report NF-2024-0042", "RELATED_TO", 0.92, "Subject of report"),
        ("Chen Wei", "SIGINT Report NF-2024-0042", "RELATED_TO", 0.88, "Subject of report"),
        ("Meridian Holdings Ltd", "Financial Analysis - Meridian Network", "RELATED_TO", 0.95, "Subject of analysis"),
    ]

    for src_name, tgt_name, rel_type, confidence, note in relationships_data:
        src_id = all_entities.get(src_name)
        tgt_id = all_entities.get(tgt_name)
        if not src_id or not tgt_id:
            continue

        rel = Relationship(
            id=_id(),
            source_entity_id=src_id,
            target_entity_id=tgt_id,
            relationship_type=rel_type,
            properties=json.dumps({"note": note}),
            confidence_score=confidence,
            source="operation_nightfall",
        )
        db.add(rel)

    db.commit()

    return {
        "message": "Operation Nightfall demo data loaded successfully!",
        "seeded": True,
        "entities_created": len(all_entities),
        "relationships_created": len(relationships_data),
        "scenario": "Operation Nightfall — Transnational Financing Network Investigation",
    }
