from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from zoneinfo import ZoneInfo
from apscheduler.triggers.cron import CronTrigger
from app.db.sync_database import sync_engine
from ingestion_service.ingestion import run_periodic_ingestion

jobstores = {
    "default": SQLAlchemyJobStore(
        engine=sync_engine,
        tablename="cron_schedulers",
    )
}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone=ZoneInfo("UTC"))


async def start_scheduler() -> None:
    scheduler.start()

    scheduler.add_job(
        run_periodic_ingestion,
        CronTrigger(minute="0"),  # every hour at :00
        id="country_ingestion_job",
        replace_existing=True,
    )

    print("🚀 Scheduler started with per-tenant jobs every minute")
