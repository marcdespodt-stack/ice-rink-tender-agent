import os
from typing import Any, Dict

import yaml
from agents import Agent, Runner, WebSearchTool

from .models import TenderScan


SYSTEM_PROMPT = """
You are the Worldwide Ice Rink Tender Scout.

Your job is to find PUBLIC procurement opportunities anywhere in the world
that could be relevant to an ice-rink company.

Look for opportunities involving:

- mobile ice rinks
- temporary ice rinks
- portable ice rinks
- outdoor seasonal ice rinks
- skating rinks
- ice rink refrigeration systems
- ice resurfacing machines
- ice groomers
- Rolba machines
- rink boards
- skates
- skating aids
- purchase, rental or lease of ice-rink equipment

SEARCH STRATEGY

Search internationally, not only in Europe.

Use:
1. English terminology
2. Local-language terminology
3. CPV codes
4. Government procurement portals
5. Municipal procurement portals
6. National tender databases
7. Official buyer websites

The search should cover Europe, North America, Latin America,
Middle East, Africa, Asia and Oceania.

IMPORTANT

Never invent information.

If a tender number, value, deadline, dimension or technical requirement
cannot be verified, leave the field empty.

Prefer official procurement sources.

Secondary tender aggregators may be used to discover opportunities,
but the official source should be identified whenever possible.

For every opportunity, provide evidence URLs whenever available.

DEDUPLICATION

The same tender may appear on several websites.

Try to identify duplicate notices using:
- buyer
- tender title
- notice/reference number
- country
- deadline

Return each distinct tender only once.

RELEVANCE

Prioritize actual procurement opportunities rather than:
- news articles
- general information pages
- completed historical projects
- private advertisements
- synthetic/plastic ice products when the requirement is for real ice
- permanent indoor arena construction unless ice-rink equipment is
  explicitly being procured.

The final output must contain structured tender opportunities only.
"""


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_agent() -> Agent:
    model = os.getenv("OPENAI_MODEL", "gpt-5.6")

    return Agent(
        name="Worldwide Ice Rink Tender Scout",
        instructions=SYSTEM_PROMPT,
        tools=[
            WebSearchTool()
        ],
        output_type=TenderScan,
        model=model,
    )


def build_search_context(query: str, config: Dict[str, Any]) -> str:
    company = config.get("company", {})
    search = config.get("search", {})

    return f"""
COMPANY PROFILE

{company}

SEARCH CONFIGURATION

{search}

PRIMARY SEARCH REQUEST

{query}

TASK

Find current and recently published public procurement opportunities
matching the company profile.

Search across all geographic regions.

Use multiple searches and languages.

Search both:
- broad keyword combinations
- exact CPV codes
- local-language equivalents
- buyer/municipality procurement pages

Return up to 30 distinct opportunities.

Only include opportunities for which there is reasonable evidence
that a real procurement process exists.
"""


def scan_tenders(
    query: str,
    config: Dict[str, Any]
) -> TenderScan:

    agent = build_agent()

    context = build_search_context(
        query=query,
        config=config
    )

    result = Runner.run_sync(
        agent,
        context
    )

    return result.final_output
