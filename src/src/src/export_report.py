import csv
import os
import sqlite3

from dotenv import load_dotenv


load_dotenv()


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/tenders.db"
)

OUTPUT_FILE = (
    "data/tender_report.csv"
)


def main():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    rows = connection.execute(
        """
        SELECT
            title,
            buyer,
            country,
            region,
            deadline,
            estimated_value,
            currency,
            score,
            recommendation,
            url,
            notice_id
        FROM tenders
        ORDER BY
            score DESC,
            deadline ASC
        """
    ).fetchall()

    connection.close()

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "Title",
                "Buyer",
                "Country",
                "Region",
                "Deadline",
                "Estimated Value",
                "Currency",
                "Score",
                "Recommendation",
                "URL",
                "Notice ID",
            ]
        )

        writer.writerows(
            rows
        )

    print(
        f"Exported {len(rows)} tenders "
        f"to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
