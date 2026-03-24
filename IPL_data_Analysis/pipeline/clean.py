# pipeline/clean.py
import pandas as pd
import numpy as np
import os

RAW = "data"


def clean_matches():
    print("[CLEAN] Processing matches.csv...")
    df = pd.read_csv(os.path.join(RAW, "matches.csv"))
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    # Date handling
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['season'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%b')

    # Standardise team names (IPL franchises changed names over the years)
    name_map = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Deccan Chargers': 'Sunrisers Hyderabad',
        'Pune Warriors': 'Rising Pune Supergiant',
        'Kings XI Punjab': 'Punjab Kings',
        'Rising Pune Supergiants': 'Rising Pune Supergiant',
    }
    for col in ['team1', 'team2', 'toss_winner', 'winner']:
        if col in df.columns:
            df[col] = df[col].replace(name_map)

    # Toss decision outcome — did winning toss help?
    df['toss_winner_won_match'] = (df['toss_winner'] == df['winner']).astype(int)

    # Margin type flag
    df['win_by_runs'] = df.get('result_margin', 0).where(df.get('result', '') == 'runs', 0)
    df['win_by_wickets'] = df.get('result_margin', 0).where(df.get('result', '') == 'wickets', 0)

    # Match type
    df['is_playoff'] = df.get('match_type', '').str.contains(
        'Final|Qualifier|Eliminator', case=False, na=False).astype(int)

    # Drop rows with no winner (no result / abandoned)
    df = df.dropna(subset=['winner'])

    print(f"[CLEAN] Matches: {len(df):,} rows | Seasons: {df['season'].nunique()}")
    return df


def clean_deliveries(matches_df):
    print("[CLEAN] Processing deliveries.csv...")
    df = pd.read_csv(os.path.join(RAW, "deliveries.csv"))
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Rename common column variations
    rename_map = {
        'match_id': 'match_id',
        'batting_team': 'batting_team',
        'bowling_team': 'bowling_team',
        'batter': 'batter',
        'bowler': 'bowler',
        'batsman': 'batter',  # older dataset naming
        'non_striker': 'non_striker',
        'over': 'over',
        'ball': 'ball',
        'batsman_runs': 'batsman_runs',
        'extra_runs': 'extra_runs',
        'total_runs': 'total_runs',
        'is_wicket': 'is_wicket',
        'player_dismissed': 'player_dismissed',
        'dismissal_kind': 'dismissal_kind',
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Ensure required columns exist with defaults
    for col, default in [('batsman_runs', 0), ('extra_runs', 0), ('total_runs', 0),
                         ('is_wicket', 0), ('player_dismissed', ''), ('dismissal_kind', '')]:
        if col not in df.columns:
            df[col] = default

    # Over phase classification
    df['phase'] = pd.cut(df['over'],
                         bins=[-1, 5, 14, 19],
                         labels=['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)'])

    # Boundary flag
    df['is_four'] = (df['batsman_runs'] == 4).astype(int)
    df['is_six'] = (df['batsman_runs'] == 6).astype(int)
    df['is_dot'] = ((df['total_runs'] == 0) & (df['is_wicket'] == 0)).astype(int)
    df['is_boundary'] = ((df['is_four'] == 1) | (df['is_six'] == 1)).astype(int)

    # Legal delivery (not a wide or no-ball)
    df['is_legal'] = (~df.get('extras_type', pd.Series([''] * len(df)))
                      .isin(['wides', 'noballs'])).astype(int)

    # Merge season from matches
    if 'season' in matches_df.columns:
        season_map = matches_df.set_index('id')['season'].to_dict() if 'id' in matches_df.columns else \
        matches_df.set_index('match_id')['season'].to_dict() if 'match_id' in matches_df.columns else {}
        if season_map:
            df['season'] = df['match_id'].map(season_map)

    print(f"[CLEAN] Deliveries: {len(df):,} rows")
    return df


def clean_all():
    matches = clean_matches()
    deliveries = clean_deliveries(matches)
    return matches, deliveries


if __name__ == "__main__":
    m, d = clean_all()
    print(f"\nMatches shape:    {m.shape}")
    print(f"Deliveries shape: {d.shape}")