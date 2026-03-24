import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

CHECKS = [
    ("Total matches loaded",
     "SELECT COUNT(*) FROM matches",
     lambda n: n > 800, "Expected 900+"),

    ("Total deliveries loaded",
     "SELECT COUNT(*) FROM deliveries",
     lambda n: n > 180000, "Expected 200K+"),

    ("Seasons covered",
     "SELECT COUNT(DISTINCT season) FROM matches",
     lambda n: n >= 15, "Expected 15+"),

    ("Unique batters",
     "SELECT COUNT(DISTINCT batter) FROM deliveries",
     lambda n: n > 400, "Expected 400+"),

    ("Unique bowlers",
     "SELECT COUNT(DISTINCT bowler) FROM deliveries",
     lambda n: n > 300, "Expected 300+"),

    ("No null winners",
     "SELECT COUNT(*) FROM matches WHERE winner IS NULL",
     lambda n: n == 0, "Should be 0 null winners"),

    ("Phase distribution",
     "SELECT phase, COUNT(*) FROM deliveries GROUP BY phase ORDER BY phase",
     None, "Info only"),

    ("Toss win rate",
     "SELECT ROUND(AVG(toss_winner_won_match)*100,1) FROM matches",
     None, "Should be around 50%"),
]


def validate():
    url = (f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
           f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    engine = create_engine(url)
    passed = 0;
    failed = 0

    print("\n" + "=" * 55)
    print("  DATA QUALITY VALIDATION REPORT")
    print("=" * 55)

    with engine.connect() as conn:
        for name, query, check_fn, note in CHECKS:
            result = conn.execute(text(query)).fetchall()
            val = result[0][0] if result and len(result) == 1 else result

            if check_fn:
                ok = check_fn(val) if not isinstance(val, list) else True
                status = "PASS" if ok else "FAIL"
                if ok:
                    passed += 1
                else:
                    failed += 1
            else:
                status = "INFO"

            print(f"  [{status}] {name}: {val}  ({note})")

    print("=" * 55)
    print(f"  Results: {passed} passed | {failed} failed")
    print("=" * 55)

    if failed > 0:
        print("  WARNING: Fix failed checks before building dashboard")
    else:
        print("  All checks passed — data ready for Power BI")

    engine.dispose()


if __name__ == "__main__":
    validate()

