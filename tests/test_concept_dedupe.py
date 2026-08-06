from psn.library_utils import (
    alias_context_by_siblings,
    build_concept_siblings,
    dedupe_library_by_concept,
    enrich_purchased_concept_ids,
)


def test_build_concept_siblings():
    played = [
        {
            "titleId": "CUSA37191_00",
            "concept": {"id": 123, "titleIds": ["CUSA37191_00", "PPSA10609_00"]},
        }
    ]
    siblings = build_concept_siblings(played)
    assert siblings["CUSA37191_00"] == ["PPSA10609_00"]
    assert siblings["PPSA10609_00"] == ["CUSA37191_00"]


def test_dedupe_library_by_concept_prefers_ppsa():
    entries = [
        {"titleId": "CUSA37191_00", "name": "Pursuit Force", "conceptId": 123},
        {"titleId": "PPSA10609_00", "name": "Pursuit Force", "conceptId": 123},
    ]
    deduped = dedupe_library_by_concept(entries)
    assert len(deduped) == 1
    assert deduped[0]["titleId"] == "PPSA10609_00"


def test_dedupe_library_by_concept_collapses_regional_skus():
    # Issue #48: a game owned in many regions (16 SKUs for FF XV) must
    # produce exactly one library entry, since Galaxy 2.1 shows every
    # game_id as a separate game.
    entries = [
        {"titleId": f"CUSA{10000 + i:05d}_00", "name": "Final Fantasy XV", "conceptId": 777}
        for i in range(16)
    ]
    deduped = dedupe_library_by_concept(entries)
    assert len(deduped) == 1
    assert deduped[0]["name"] == "Final Fantasy XV"


def test_enrich_purchased_concept_ids():
    purchased = [{"titleId": "CUSA36463_00", "name": "Bluey", "source": "purchased"}]
    played = [
        {
            "titleId": "PPSA09955_00",
            "concept": {"id": 999, "titleIds": ["PPSA09955_00", "CUSA36463_00"]},
        }
    ]
    enrich_purchased_concept_ids(purchased, played)
    assert purchased[0]["conceptId"] == "999"


def test_alias_context_by_siblings():
    context = {"PPSA01325_00": ["trophy-a"]}
    siblings = {"PPSA99999_00": ["PPSA01325_00"]}
    alias_context_by_siblings(context, ["PPSA99999_00"], siblings)
    assert context["PPSA99999_00"] == ["trophy-a"]
