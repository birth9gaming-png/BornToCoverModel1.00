# Born to Cover — Prototype 16

Your weekly list now shows up to **four distinct games per league**. It ranks usable, current projections by the displayed win estimate; historical support and sensitivity remain visible checks. Negative EV does not automatically exclude a pick. Both spread and total remain visible, with the preferred market highlighted.

This build changes the main forecasting algorithms. CFB spreads use a median/histogram-boosting stack, CFB totals use Extra Trees instead of the fixed 10% statistical blend, and NFL spreads use a random forest. NFL totals retain the prior recipe because replacements did not qualify. Current-year data is captured automatically and qualifying updates are checked on later weeks. The model has not demonstrated a 65–70% live win rate; confidence is not inflated to fill a quota.

## Install

1. Extract `football_dashboard_prototype16.zip`.
2. Replace your app files with **every file inside `football_dashboard/`**, including new Python modules, requirements, config and all preloaded artifacts.
3. Keep existing Streamlit Secrets, the app entry path and private cloud data. Reboot.
4. Confirm **Prototype 16** in the sidebar. Allow the background current-season refresh to finish before treating NFL projections, scorer data or odds as current.

Your new trained main recipe and historical datasets are preloaded. Existing cloud saves are upgraded automatically; there is no manual Apply Model step or ten-season download. `v16` is the active main recipe. Earlier artifacts remain for audit/reproducibility; they are not selected ahead of it.

## Review a game

Click **Review assumptions** or **View game and inputs** directly under its game card. The weekly list also has a **Review game** button for each pick.

The panel shows current and sensitivity-tested win estimates, final forecasts with/without the listed adjustments, injury players/statuses/sources/timestamps, wind, divisional context and matchup reasons.

- **Use forecast without these adjustments** saves a reversible choice for this game. It removes the injury/wind/unlearned-spot/fixed-division effects included in the sensitivity check. It does not remove every modeling assumption or certify a wager.
- **Restore automatic inputs** reverses that choice.
- **Refresh current game inputs** runs the current-season update and retains the other league and your historical models.
- **Correct a player status from a dated report** requires an actual source and publication time. Automatic corrections preserve existing player importance/role calculations, including defensive effects on the opponent. They are scoped to the game and expire after 24 hours or a newer report. Confirming a fact does not validate its assumed point value.

## Best available weekly picks

There is no minimum EV in the new shortlist. Current prices, a usable projection, current NFL statistics and a win estimate above 50% both with/without checked live adjustments are required. Fewer than four places remain unfilled if those checks fail; the exclusions explain why.

The preferred market is the higher displayed win estimate. Reported recipe probability checks and the lower with/without estimate provide warnings and tie-breakers, rather than replacing a 54.2% choice with a 51.5% choice. There is no 60% cap or quota. These historical comparisons precede production refitting and do not establish a live betting record.

On a Monday window spanning two NFL weeks, the list uses the next substantial upcoming slate instead of trying to fill four positions from one remaining Monday game. The board still exposes the Monday game, and the shortlist caption identifies its official week.

Buying points uses actual DraftKings/FanDuel alternate offers, on the same side selected from the main lines. Default limits are **three bought points** and **−150 or better**. Setup has an optional −150/−200/−300 price choice and an on/off control. No prices are invented. Alternate lines do not alter the model's consensus market reference. Up to eight provisional weekly games receive an event-level alternate-price lookup during a normal live refresh; source access and API quota apply.

The first displayed live weekly list is frozen and tracked separately in **Results & Learning**. Its actual prices determine hypothetical unit returns. Later reruns cannot rewrite that record after a result. The current board can change as new data arrives; the recorded first list remains identifiable.

## Anytime touchdowns

The NFL loader no longer lets a pending Monday game's week cutoff exclude completed Sunday games from later matchups. Statistics and player inputs use verified completed games available at the forecast time; completed cards keep their pregame inputs.

A snap sheet without completed game play-by-play cannot manufacture zero targets or zero TDs. Missing later-game coverage disables recency rules instead of treating an older zero-TD game as a new bounce-back opportunity. Byes and confirmed inactive games still skip correctly.

Featured scorers require current player and opponent coverage, at least three recent active games, observed opportunities, recent and latest-game offensive snap shares and an eligible role. They rank by **scoring opportunities matched to the opponent**, using rushing/receiving and RB/WR/TE touchdown splits, goal-line carries and red-zone targets. Counts are adjusted for opportunities faced and field position and shrunk toward league rates. Odds are an optional displayed price and never determine the order. The relative model scorer score is not a calibrated probability. Open **Why these scorers rank** for the underlying defensive channels and usage.

The existing xTD, red-zone and recency calculations remain in an explicitly exploratory section. They have not been validated as a TD pricing model, so their formula EV cannot rank the featured list or be advertised as a +100% betting edge. Out/doubtful players remain excluded, and final availability still matters. Every loaded upcoming NFL game is searched; there is no high-total gate.

## Saved data and validation

Your saved history, models, settings and frozen cards remain. Live CFB refreshes reuse known saved historical context instead of requesting those past annual responses again; current-season statistics and prices still refresh. Incomplete saved years retain their coverage limits.

Missing CFB season metadata is supplied on loaded games. Older frozen records can resolve a season from their pregame date for matching final scores; their predictions, picks and prices are not rewritten. Weekly learning still requires the existing sample-size and later-period checks.

Current-season history is collected in the background and included in your cloud save and complete backup. **Results & Learning** shows both the historical learning track and the separately frozen live picks. **Method & Validation** shows algorithm comparisons, current-season coverage and calibration buckets. An unsuccessful update leaves the approved historical recipe active. Turning automatic learning off uses that frozen recipe and disables new weekly corrections.

See `research_notes_v16.md`, `validation_summary_v16.json` and `model_comparison_v16.json` for the new main model comparisons, rejected methods, initial 2026 checks and limitations. Initial 2026 NFL probability accuracy did not improve on the small 46-game reconstruction; that result is shown honestly.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
python -m unittest discover -s tests
```

Software tests verify behavior, data timing and model portability—not betting accuracy. The current build's completed test results are recorded in `audit_report_v16.md`.
