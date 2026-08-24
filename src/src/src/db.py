import json
import sqlite3
from pathlib import Path

from .models import TenderOpportunity


SCHEMA = """
CREATE TABLE IF NOT EXISTS tenders (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fingerprint TEXT UNIQUE,

    title TEXT NOT NULL,

    buyer TEXT,

    country TEXT,

    region TEXT,

    procurement_portal TEXT,

    notice_id TEXT,

    publication_date TEXT,

    deadline TEXT,

    estimated_value TEXT,

    currency TEXT,

    purchase_or_rental TEXT,

    score INTEGER,

    recommendation TEXT,

    url TEXT,

    raw_json TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db(database_path: str) -> sqlite3.Connection:

    path = Path(database_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        database_path
    )

    connection.execute(
        SCHEMA
    )

    connection.commit()

    return connection


def save_tender(
    connection: sqlite3.Connection,
    tender: TenderOpportunity,
    fingerprint: str
):

    raw_json = json.dumps(
        tender.model_dump(),
        ensure_ascii=False
    )

    connection.execute(
        """
        INSERT OR REPLACE INTO tenders
        (
            fingerprint,
            title,
            buyer,
            country,
            region,
            procurement_portal,
            notice_id,
            publication_date,
            deadline,
            estimated_value,
            currency,
            purchase_or_rental,
            score,
            recommendation,
            url,
            raw_json,
            updated_at
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
        )
        """,
        (
            fingerprint,
            tender.title,
            tender.buyer,
            tender.country,
            tender.region,
            tender.procurement_portal,
            tender.notice_id,
            tender.publication_date,
            tender.deadline,
            tender.estimated_value,
            tender.currency,
            tender.purchase_or_rental,
            tender.relevance_score,
            tender.recommendation,
            tender.url or tender.source_url,
            raw_json,
        )
    )

    connection.commit()


def get_tenders(
    connection: sqlite3.Connection
):

    cursor = connection.execute(
        """
        SELECT
            title,
            buyer,
            country,
            deadline,
            estimated_value,
            currency,
            score,
            recommendation,
            url,
            notice_id
        FROM tenders
        ORDER BY score DESC
        """
    )

    return cursor.fetchall()


def close_db(
    connection: sqlite3.Connection
):

    connection.close()
