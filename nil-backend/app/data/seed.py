from typing import List
from ..models.schemas import Player, Position, ConferenceLevel, PlayerStats

DATA: List[Player] = []

TIER_FOR_GROUP5_HIGH = "Group5_High"


def _add(p: Player):
    DATA.append(p)


def load_seed():
    DATA.clear()
    _add(Player(
        athlete_id="baron-hopson-like",
        name="Baron Hopson Like",
        position=Position.LB,
        conference_level=ConferenceLevel.FCS,
        school="KSU",
        transfer_from="FCS",
        stats=PlayerStats(total_tackles=11, solo_tackles=6, assisted_tackles=5, games_played=1, conference="FCS"),
        market_value=15000.0,
    ))
    _add(Player(
        athlete_id="sec-comp-lb-1",
        name="SEC Comp LB 1",
        position=Position.LB,
        conference_level=ConferenceLevel.POWER4,
        school="SEC U",
        transfer_from="SEC",
        stats=PlayerStats(total_tackles=10, solo_tackles=5, assisted_tackles=5, games_played=1, conference="SEC"),
        market_value=165000.0,
    ))
    for i in range(1, 20):
        _add(Player(
            athlete_id=f"wr-{i}",
            name=f"WR Prospect {i}",
            position=Position.WR,
            conference_level=ConferenceLevel.GROUP5 if i % 2 == 0 else ConferenceLevel.FCS,
            school="Group5 U" if i % 2 == 0 else "FCS U",
            transfer_from="FCS" if i % 3 == 0 else "Group5",
            stats=PlayerStats(total_tackles=0, solo_tackles=0, assisted_tackles=0, games_played=12, conference="Sun Belt"),
            market_value=20000.0 + 1000 * i,
        ))
    for i in range(1, 10):
        _add(Player(
            athlete_id=f"dl-{i}",
            name=f"DL Prospect {i}",
            position=Position.DL,
            conference_level=ConferenceLevel.GROUP5,
            school="CUSA U",
            transfer_from="FCS" if i % 2 == 1 else "Group5",
            stats=PlayerStats(total_tackles=30 + i, solo_tackles=15 + i, assisted_tackles=15, games_played=12, conference="CUSA"),
            market_value=35000.0 + 1500 * i,
        ))
