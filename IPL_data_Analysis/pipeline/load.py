import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    url = (f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
           f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    return create_engine(url)


def create_database_if_missing():
    """Connect to default postgres DB and create ipl_db if it doesn't exist."""
    import psycopg2
    conn = psycopg2.connect(
        dbname='postgres',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    conn.autocommit = True
    cur = conn.cursor()
    db_name = os.getenv('DB_NAME', 'ipl_db')
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"[LOAD] Created database: {db_name}")
    else:
        print(f"[LOAD] Database {db_name} already exists")
    cur.close();
    conn.close()


def load_data(matches_df, deliveries_df):
    create_database_if_missing()
    engine = get_engine()

    # Select and order columns cleanly before loading
    match_cols = [c for c in [
        'id', 'season', 'date', 'month', 'month_name', 'city', 'venue',
        'team1', 'team2', 'toss_winner', 'toss_decision', 'winner',
        'result', 'result_margin', 'win_by_runs', 'win_by_wickets',
        'player_of_match', 'toss_winner_won_match', 'is_playoff'
    ] if c in matches_df.columns]

    delivery_cols = [c for c in [
        'match_id', 'season', 'inning', 'batting_team', 'bowling_team',
        'over', 'ball', 'phase', 'batter', 'bowler', 'non_striker',
        'batsman_runs', 'extra_runs', 'total_runs',
        'is_four', 'is_six', 'is_boundary', 'is_dot', 'is_legal',
        'is_wicket', 'player_dismissed', 'dismissal_kind'
    ] if c in deliveries_df.columns]

    print("[LOAD] Loading matches table...")
    matches_df[match_cols].to_sql(
        'matches', engine, if_exists='replace', index=False, method='multi', chunksize=500)
    print(f"[LOAD] matches: {len(matches_df):,} rows loaded")

    print("[LOAD] Loading deliveries table (large — may take 30-60 seconds)...")
    deliveries_df[delivery_cols].to_sql(
        'deliveries', engine, if_exists='replace', index=False, method='multi', chunksize=2000)
    print(f"[LOAD] deliveries: {len(deliveries_df):,} rows loaded")

    # Create indexes for fast querying
    print("[LOAD] Creating indexes...")
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_del_match   ON deliveries (match_id)",
        "CREATE INDEX IF NOT EXISTS idx_del_batter  ON deliveries (batter)",
        "CREATE INDEX IF NOT EXISTS idx_del_bowler  ON deliveries (bowler)",
        "CREATE INDEX IF NOT EXISTS idx_del_season  ON deliveries (season)",
        "CREATE INDEX IF NOT EXISTS idx_del_phase   ON deliveries (phase)",
        "CREATE INDEX IF NOT EXISTS idx_match_season ON matches (season)",
        "CREATE INDEX IF NOT EXISTS idx_match_winner ON matches (winner)",
    ]
    with engine.connect() as conn:
        for idx in indexes:
            conn.execute(text(idx))
        conn.commit()
    print("[LOAD] All indexes created")
    engine.dispose()


if __name__ == "__main__":
    from clean import clean_all

    m, d = clean_all()
    load_data(m, d)
