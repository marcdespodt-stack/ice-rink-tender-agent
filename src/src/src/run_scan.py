import argparse
import hashlib
import os

from dotenv import load_dotenv

from src.agent import load_config, scan_tenders
from src.db import init_db, save_tender
from src.scoring import score_tender


load_dotenv()


def create_fingerprint(tender) -> str:

    identity = "|".join(
        [
            (tender.notice_id or "").strip().lower(),
            (tender.buyer or "").strip().lower(),
            (tender.title or "").strip().lower(),
            (tender.country or "").strip().lower(),
        ]
    )

    return hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()


def main():

    parser = argparse.ArgumentParser(
        description="Worldwide Ice Rink Tender Agent"
    )

    parser.add_argument(
        "--query",
        default=(
            "worldwide public procurement "
            "mobile ice rink temporary ice rink "
            "ice resurfacing machine"
        ),
        help="Main tender search query"
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # LOAD CONFIGURATION
    # ---------------------------------------------------------

    config = load_config()

    database_path = os.getenv(
        "DATABASE_PATH",
        "data/tenders.db"
    )

    # ---------------------------------------------------------
    # DATABASE
    # ---------------------------------------------------------

    connection = init_db(
        database_path
    )

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    print()
    print("=" * 80)
    print("WORLDWIDE ICE RINK TENDER AGENT")
    print("=" * 80)
    print()

    print("Searching worldwide procurement opportunities...")
    print()

    result = scan_tenders(
        query=args.query,
        config=config
    )

    # ---------------------------------------------------------
    # SCORE + STORE
    # ---------------------------------------------------------

    ranked_tenders = []

    for tender in result.opportunities:

        tender = score_tender(
            tender,
            config
        )

        fingerprint = create_fingerprint(
            tender
        )

        save_tender(
            connection,
            tender,
            fingerprint
        )

        ranked_tenders.append(
            tender
        )

    # Highest relevance first
    ranked_tenders.sort(
        key=lambda tender: tender.relevance_score,
        reverse=True
    )

    # ---------------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------------

    print()
    print(
        f"Found {len(ranked_tenders)} opportunities"
    )
    print()

    print("=" * 80)

    for number, tender in enumerate(
        ranked_tenders,
        start=1
    ):

        print(
            f"{number:02d}. "
            f"[{tender.relevance_score:03d}/100] "
            f"{tender.title}"
        )

        print(
            f"    Buyer: "
            f"{tender.buyer or 'Unknown'}"
        )

        print(
            f"    Country: "
            f"{tender.country or 'Unknown'}"
        )

        print(
            f"    Deadline: "
            f"{tender.deadline or 'Unknown'}"
        )

        print(
            f"    Value: "
            f"{tender.estimated_value or 'Unknown'} "
            f"{tender.currency or ''}"
        )

        print(
            f"    Recommendation: "
            f"{tender.recommendation}"
        )

        print(
            f"    URL: "
            f"{tender.url or tender.source_url or 'Unknown'}"
        )

        print()

    print("=" * 80)

    print(
        f"Database: {database_path}"
    )


if __name__ == "__main__":
    main()
