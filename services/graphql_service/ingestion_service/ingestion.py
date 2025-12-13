from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import os
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Country
from app.db.database import SessionLocal

load_dotenv()


class CountryIngestionService:
    """Service to fetch and store/ update country information."""

    COUNTRIES_API_URL = os.getenv("ingestion_api_url")

    async def fetch_countries(self) -> List[Dict[str, Any]]:
        """Fetch country data from the external API."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.COUNTRIES_API_URL)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching countries: {e}")
            return []

    def transform(self, raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform API response into SQLAlchemy model structure."""
        try:
            name = raw.get("name", "")
            latlng = raw.get("latlng", [])
            flags = raw.get("flags", {})
            currencies = raw.get("currencies", {})
            languages = raw.get("languages", {})
            borders = raw.get("borders", [])

            return {
                "name": name,
                "calling_codes": raw.get("callingCodes", []),
                "alpha2_code": raw.get("alpha2Code", None),
                "alpha3_code": raw.get("alpha3Code", None),
                "capital": raw.get("capital", ""),
                "region": raw.get("region", None),
                "subregion": raw.get("subregion", None),
                "population": raw.get("population", 0),
                "area": raw.get("area", 0),
                "latitude": latlng[0] if len(latlng) > 0 else None,
                "longitude": latlng[1] if len(latlng) > 1 else None,
                "timezones": raw.get("timezones", []),
                "borders": borders,
                "currencies": currencies,
                "languages": languages,
                "flag_svg": flags.get("svg", ""),
                "flag_png": flags.get("png", ""),
                "independent": raw.get("independent", False),
            }
        except Exception as e:
            print(f"Error transforming country: {e}")
            return None

    async def ingest(
        self, db: AsyncSession, raw_countries: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Optimized bulk insert/update of countries."""
        stats = {"added": 0, "updated": 0, "failed": 0}

        try:
            existing_stmt = await db.execute(select(Country))
            existing_countries = existing_stmt.scalars().all()
            existing_countries_map = {c.alpha2_code: c for c in existing_countries}
            new_objects = []

            for raw in raw_countries:
                data = self.transform(raw)
                if not data or not data["alpha2_code"]:
                    stats["failed"] += 1
                    continue

                alpha2 = data["alpha2_code"]
                existing = existing_countries_map.get(alpha2)

                if existing:
                    for field, value in data.items():
                        setattr(existing, field, value)
                    existing.updated_at = datetime.utcnow()
                    stats["updated"] += 1

                else:
                    new_objects.append(Country(**data))
                    stats["added"] += 1

            if new_objects:
                db.add_all(new_objects)
            await db.commit()

        except Exception as e:
            print(f"Bulk ingestion error: {e}")
            await db.rollback()
            stats["failed"] += 1

        return stats

    async def run_ingestion(self):
        """Execute ingestion process once."""
        print(f"Starting ingestion @ {datetime.utcnow()}")

        raw_data = await self.fetch_countries()
        print(f"Fetched {len(raw_data)} countries")

        if not raw_data:
            print("No country data fetched")
            return

        db = SessionLocal()
        try:
            stats = await self.ingest(db, raw_data)
            print(f"Ingestion Completed -> {stats}")
        finally:
            await db.close()

        return stats


async def run_periodic_ingestion() -> dict[str, Any]:
    stats: Dict = {}
    service = CountryIngestionService()
    try:
        stats = await service.run_ingestion()
        print("Cron Ingestion Result:", stats)
    except Exception as e:
        print(f"Periodic ingestion error: {e}")
    return {"stats": stats}
