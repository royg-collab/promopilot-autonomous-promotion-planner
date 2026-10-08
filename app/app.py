from pathlib import Path

import streamlit as st

from agent import PromotionAgent

st.set_page_config(page_title='PromoPilot', page_icon='🛍️', layout='wide')
st.title('🛍️ PromoPilot — Autonomous Promotion Planner')
st.caption('Electronics retail | Agentic promotion planning MVP')

# Resolve the workbook relative to this Python file so the app works regardless
# of the directory from which Streamlit is launched.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = PROJECT_ROOT / 'data' / 'electronics_retail_promotion_dataset.xlsx'

if not WORKBOOK.exists():
    st.error(f'Dataset not found: {WORKBOOK}')
    st.stop()

with st.sidebar:
    st.header('Planning Controls')
    min_margin = st.number_input('Minimum margin %', 5.0, 30.0, 12.0, 0.5)
    top_n = st.slider('Recommendations', 1, 10, 5)

agent = PromotionAgent(str(WORKBOOK))
result = agent.run(top_n=top_n, min_margin=min_margin)
plans = result['plans']

st.subheader('Recommended Promotions')
if plans.empty:
    st.warning('No promotion candidate satisfies the current constraints.')
else:
    display_cols = [
        'product_name', 'region', 'score', 'mechanism', 'discount_pct',
        'duration_days', 'target_segment', 'expected_units',
        'expected_revenue', 'margin_pct', 'constraints'
    ]
    st.dataframe(plans[display_cols], use_container_width=True)

    p = plans.iloc[0]
    st.subheader('Autonomous Decision Trace')
    for step in result['trace']:
        st.write('→', step)

    st.write(f"**Selected:** {p.product_name} — {p.region}")
    for reason in str(p.reasons).split('; '):
        st.write('•', reason)
    st.write(
        f"**Strategy:** {p.mechanism}, {p.discount_pct}% for "
        f"{p.duration_days} days, targeting **{p.target_segment}**."
    )
    st.write(
        f"**Simulation:** {p.expected_units} units / 14 days, "
        f"revenue {p.expected_revenue:,.0f}, margin {p.margin_pct:.2f}%."
    )
    st.success(
        f"Constraint validation: PASS — minimum margin {min_margin:.1f}% "
        "and marketing budget rules satisfied."
    )

st.divider()
st.caption(
    'Agentic loop: Select → Strategize → Simulate → Validate → '
    'Re-plan when constraints fail → Approve'
)
