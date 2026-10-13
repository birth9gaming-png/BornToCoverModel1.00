"""Readable evidence for the actual spread/total forecasting changes."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st


def panel(data):
    st.write('The main forecasts now use dated efficiency and matchup features to learn where the market reference may be wrong. Different algorithms are chosen for each league and market; no game-specific fixes, confidence floor, or weekly weight sliders.')
    st.caption('Active recipes: CFB spreads — median/histogram boosting; CFB totals — Extra Trees; NFL spreads — random forest; NFL totals — previous fitted residual model retained.')
    rows=[]
    for league,policy in data.get('forecast_policies',{}).items():
        for target,item in policy['targets'].items():
            dev=item.get('main_development',{})
            for part,year in (('audit',2024),('test',2025)):
                old=dev.get('previous',{}).get(part,{});new=dev.get('selected',{}).get(part,{})
                if not old or not new:continue
                rows.append({'League':league,'Market':'Spread' if target=='margin' else 'Total','Forecast method':item.get('main_algorithm'),
                    'Development season':year,'Old Brier':old.get('brier'),'Revised Brier':new.get('brier'),
                    'Old log loss':old.get('log_loss'),'Revised log loss':new.get('log_loss'),
                    'Forecasts ≥60%':new.get('at_least_60_count',new.get('probability_buckets',{}).get('60–70%',{}).get('games',0))})
    if rows:st.dataframe(pd.DataFrame(rows),hide_index=True,width='stretch')
    st.caption('Lower Brier and log loss are better. Train through 2022, choose parameters on 2023, require checks on 2024 and 2025, then refit the approved recipe through 2025. Because acceptance considered both later seasons, these are development checks—not untouched final tests or verified betting returns. NFL totals retain the previous forecast because the replacements did not qualify.')
    st.info('There is no 57% ceiling or 60% quota. A 60–70% estimate needs sufficient point advantage or an actual offered alternate line. A higher displayed number is not evidence of a 65–70% long-term hit rate; small high-confidence samples remain uncertain.')
    st.subheader('2026 learning and data coverage')
    coverage=[]
    for league,report in data.get('season_learning',{}).get('leagues',{}).items():
        coverage.append({'League':league,'Season':report.get('season'),'Completed outcomes saved':report.get('completed_schedule_games'),
                        'Eligible prior-week games':report.get('eligible_prior_week_games'),'Status':report.get('status')})
    if coverage:st.dataframe(pd.DataFrame(coverage),hide_index=True,width='stretch')
    st.caption('Current-year game statistics are collected during the background refresh and saved with your old seasons. Weekly refits and shrunk seasonal-bias candidates are compared on earlier and later weeks; only a qualifying update is applied. This reconstruction is separate from the first-shown live pick ledger. Missing statistics are withheld, not treated as zero.')
    with st.expander('Current-season probability checks and calibration buckets'):
        for league,report in data.get('season_learning',{}).get('leagues',{}).items():
            st.write(league+' · '+report.get('status','Waiting for history'))
            for target,check in report.get('targets',{}).items():
                st.caption(('Spread' if target=='margin' else 'Total')+' · '+check.get('status','Collecting evidence'))
                st.json(check)
    summary=Path(__file__).with_name('validation_summary_v16.json')
    if summary.exists():
        current=json.loads(summary.read_text()).get('current_NFL_2026',{})
        with st.expander('Initial 2026 NFL reconstruction: previous versus revised'):
            rows=[]
            for target,pair in current.get('comparisons',{}).items():
                rows.append({'Market':'Spread' if target=='margin' else 'Total','Eligible games':pair['new']['games'],
                             'Previous Brier':pair['old']['brier'],'Revised Brier':pair['new']['brier'],
                             'Previous log loss':pair['old']['log_loss'],'Revised log loss':pair['new']['log_loss']})
            if rows:st.dataframe(pd.DataFrame(rows),hide_index=True,width='stretch')
            st.caption('This 46-game initial check did not improve probability accuracy for the revised NFL spread recipe. It is displayed, not concealed or used to inflate confidence. Seventy-eight completed outcomes were captured through the stated cutoff; first-two-week/incomplete histories leave 46 eligible games. Historical closing references are not your earlier live prices.')
    with st.expander('2026 online research: sources, tested methods, and limits'):
        st.markdown('[2026 NFL tracker](https://www.thepredictiontracker.com/nflresults.php) · [2026 CFB tracker](https://www.thepredictiontracker.com/ncaaresults.php) · [nfelo market regression](https://www.nfeloapp.com/analysis/using-market-regression-to-improve-prediction-accuracy-in-the-nfl/) · [nfelo key numbers](https://www.nfeloapp.com/analysis/margin-probabilities-from-nfl-spreads/) · [Ensemble algorithms](https://scikit-learn.org/stable/modules/ensemble.html)')
        st.write('Eight forecasting families were tested, followed by two-component stacks, error-weighted market blends and shrunk empirical integer-score distributions. The nonlinear spread/CFB-total recipes that passed both later-season proper-score checks are active. The last two experimental methods did not qualify and are not active. This is our own fitted implementation, not a copy of nfelo or a transfer of another service’s advertised win rate.')
        st.caption('As checked October 12, the tracker lists nfelo at 26–15 NFL ATS, but Pi-Ratings Mean at 177–143 CFB ATS—not 78% ATS; that larger percentage is straight-up winner accuracy. Different pick sets and reference times are not directly comparable to this app or proof of future performance.')
        path=Path(__file__).with_name('research_notes_v16.md')
        if path.exists():st.download_button('Download research and validation notes',path.read_text(),file_name=path.name,mime='text/markdown')
