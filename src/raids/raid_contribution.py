import pandas as pd
import requests

def parse_pastebin(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df

def get_total_damage_by_titan(url: str) -> pd.DataFrame:
    df = parse_pastebin(url=url)
    df = df[["PlayerName", "PlayerCode", "TotalRaidAttacks", "TitanNumber", "TitanDamage"]]
    return df

def get_total_damage_by_player(url: str) -> pd.DataFrame:
    titan_df = get_total_damage_by_titan(url=url)
    player_df = pd.DataFrame(columns=["PlayerName", "PlayerCode", "TotalDamage", "TotalRaidAttacks", "AvgDamagePerRaid"])
    for playerCode in titan_df.PlayerCode.unique():
        raid_attacks = int(titan_df.loc[titan_df.PlayerCode == playerCode].TotalRaidAttacks.iloc[-1])
        total_dmg =  int(titan_df.loc[titan_df.PlayerCode == playerCode].TitanDamage.sum())
        player_df = player_df.append({
            "PlayerName": titan_df.loc[titan_df.PlayerCode == playerCode].PlayerName.iloc[-1],
            "PlayerCode": playerCode,
            "TotalRaidAttacks": raid_attacks,
            "TotalDamage": total_dmg,
            "AvgDamagePerRaid": int(total_dmg/raid_attacks) if raid_attacks else 0 
        }, ignore_index=True)
    return player_df