-- ── QUERY 1: All-time team win count ──────────────────────────
SELECT winner                                   AS team,
       COUNT(*)                                 AS matches_won,
       ROUND(COUNT(*) * 100.0 /
           SUM(COUNT(*)) OVER (), 1)            AS win_pct
FROM   matches
GROUP  BY winner
ORDER  BY matches_won DESC;

-- ── QUERY 2: Toss impact — does winning toss help? ─────────────
SELECT toss_decision,
       COUNT(*)                                          AS matches,
       SUM(toss_winner_won_match)                        AS toss_winner_also_won,
       ROUND(AVG(toss_winner_won_match) * 100, 1)        AS win_pct
FROM   matches
GROUP  BY toss_decision
ORDER  BY toss_decision;

-- ── QUERY 3: Top 20 run scorers all time ───────────────────────
SELECT batter,
       SUM(batsman_runs)                        AS total_runs,
       COUNT(DISTINCT match_id)                 AS innings,
       ROUND(SUM(batsman_runs) * 100.0 /
           NULLIF(SUM(is_legal), 0), 2)         AS strike_rate,
       SUM(is_four)                             AS fours,
       SUM(is_six)                              AS sixes,
       ROUND(AVG(batsman_runs), 2)              AS avg_runs_per_ball
FROM   deliveries
WHERE  is_legal = 1
GROUP  BY batter
HAVING COUNT(DISTINCT match_id) >= 20
ORDER  BY total_runs DESC
LIMIT  20;

-- ── QUERY 4: Batting by phase (powerplay / middle / death) ─────
SELECT batter,
       phase,
       SUM(batsman_runs)                        AS runs,
       ROUND(SUM(batsman_runs)*100.0/
           NULLIF(SUM(is_legal),0),2)           AS strike_rate,
       SUM(is_six)                              AS sixes
FROM   deliveries
WHERE  is_legal = 1
GROUP  BY batter, phase
HAVING COUNT(DISTINCT match_id) >= 15
ORDER  BY batter, phase;

-- ── QUERY 5: Top 20 wicket takers all time ─────────────────────
SELECT bowler,
       COUNT(*) FILTER (WHERE is_wicket=1
           AND dismissal_kind NOT IN
               ('run out','retired hurt','obstructing the field'))
                                               AS wickets,
       COUNT(DISTINCT match_id)               AS matches,
       ROUND(SUM(total_runs)*1.0/
           NULLIF(SUM(CASE WHEN is_legal=1 THEN 1 END)/6.0, 0), 2)
                                               AS economy,
       ROUND(SUM(is_dot)*100.0/
           NULLIF(SUM(is_legal),0), 1)         AS dot_ball_pct
FROM   deliveries
GROUP  BY bowler
HAVING COUNT(DISTINCT match_id) >= 20
ORDER  BY wickets DESC
LIMIT  20;

-- ── QUERY 6: Death over specialists (overs 16-20) ──────────────
SELECT bowler,
       COUNT(*) FILTER (WHERE is_wicket=1)     AS death_wickets,
       ROUND(SUM(total_runs)*6.0/
           NULLIF(SUM(is_legal),0), 2)         AS death_economy,
       SUM(is_dot)                             AS dot_balls,
       COUNT(DISTINCT match_id)               AS matches
FROM   deliveries
WHERE  phase = 'Death (16-20)'
GROUP  BY bowler
HAVING COUNT(DISTINCT match_id) >= 10
ORDER  BY death_economy ASC
LIMIT  15;

-- ── QUERY 7: Season-wise run totals + boundary counts ──────────
SELECT season,
       COUNT(DISTINCT match_id)               AS matches,
       SUM(total_runs)                        AS total_runs,
       SUM(is_six)                            AS total_sixes,
       SUM(is_four)                           AS total_fours,
       ROUND(SUM(total_runs)*1.0/
           NULLIF(COUNT(DISTINCT match_id),0),1) AS avg_runs_per_match
FROM   deliveries
GROUP  BY season
ORDER  BY season;

-- ── QUERY 8: Head-to-head team record ──────────────────────────
SELECT team1, team2, winner, COUNT(*) AS times
FROM   matches
GROUP  BY team1, team2, winner
ORDER  BY team1, team2;

-- ── QUERY 9: Player of the Match frequency ─────────────────────
SELECT player_of_match,
       COUNT(*)                               AS potm_awards,
       COUNT(DISTINCT season)                AS seasons_active
FROM   matches
WHERE  player_of_match IS NOT NULL
GROUP  BY player_of_match
HAVING COUNT(*) >= 3
ORDER  BY potm_awards DESC
LIMIT  20;

-- ── QUERY 10: Dismissal type breakdown ─────────────────────────
SELECT dismissal_kind,
       COUNT(*)                               AS count,
       ROUND(COUNT(*)*100.0/
           SUM(COUNT(*)) OVER (), 1)          AS pct
FROM   deliveries
WHERE  is_wicket = 1
  AND  dismissal_kind != ''
GROUP  BY dismissal_kind
ORDER  BY count DESC;
