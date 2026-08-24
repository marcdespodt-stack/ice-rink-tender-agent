from .models import TenderOpportunity


def score_tender(
    tender: TenderOpportunity,
    config: dict
) -> TenderOpportunity:

    score = 0

    # Combine the most relevant tender information
    text = " ".join(
        [
            tender.title or "",
            tender.purchase_or_rental or "",
            " ".join(tender.technical_requirements),
            " ".join(tender.cpv_codes),
        ]
    ).lower()

    # ---------------------------------------------------------
    # STRONG POSITIVE SIGNALS
    # ---------------------------------------------------------

    mobile_terms = [
        "mobile ice rink",
        "temporary ice rink",
        "portable ice rink",
        "mobile skating rink",
        "temporary skating rink",
    ]

    if any(term in text for term in mobile_terms):
        score += 25

    # CPV 37411200 = skating equipment
    if "37411200" in tender.cpv_codes:
        score += 15

    # CPV 37481000 = ice-maintenance machines
    if "37481000" in tender.cpv_codes:
        score += 15

    # ---------------------------------------------------------
    # TECHNICAL FIT
    # ---------------------------------------------------------

    if tender.rink_area_m2:

        if tender.rink_area_m2 >= 300:
            score += 10

        if tender.rink_area_m2 >= 600:
            score += 5

    if tender.refrigeration_required:
        score += 5

    if tender.resurfacer_required:
        score += 5

    # ---------------------------------------------------------
    # COMMERCIAL MODEL
    # ---------------------------------------------------------

    if tender.purchase_or_rental:

        model = tender.purchase_or_rental.lower()

        if model in {
            "purchase",
            "rental",
            "lease",
            "purchase and installation",
            "rental and installation",
        }:
            score += 5

    # ---------------------------------------------------------
    # PROCUREMENT INFORMATION QUALITY
    # ---------------------------------------------------------

    if tender.deadline:
        score += 5

    if tender.buyer:
        score += 2

    if tender.url or tender.source_url:
        score += 3

    # ---------------------------------------------------------
    # RED FLAGS
    # ---------------------------------------------------------

    score -= min(
        20,
        len(tender.red_flags) * 5
    )

    # Keep score between 0 and 100
    tender.relevance_score = max(
        0,
        min(100, score)
    )

    # ---------------------------------------------------------
    # RECOMMENDATION
    # ---------------------------------------------------------

    high_threshold = config.get(
        "scoring",
        {}
    ).get(
        "high_threshold",
        75
    )

    medium_threshold = config.get(
        "scoring",
        {}
    ).get(
        "medium_threshold",
        55
    )

    if tender.relevance_score >= high_threshold:

        tender.recommendation = "bid-review"

    elif tender.relevance_score >= medium_threshold:

        tender.recommendation = "investigate"

    else:

        tender.recommendation = "low-priority"

    return tender
