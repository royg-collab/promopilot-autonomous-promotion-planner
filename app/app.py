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

if plans.empty:
    st.warning('No promotion candidate satisfies the current constraints.')
else:
    p = plans.iloc[0]

    # ---------------------------------------------------------
    # PROMOTION DECISION SUMMARY
    # ---------------------------------------------------------
    st.subheader('🎯 Promotion Decision Summary')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            'Top Product',
            f"{p.product_name}",
            f"{p.region}"
        )

    with col2:
        st.metric(
            'Recommended Discount',
            f"{p.discount_pct:.0f}%",
            f"{p.duration_days} days"
        )

    with col3:
        st.metric(
            'Expected Margin',
            f"{p.margin_pct:.2f}%",
            f"Min: {min_margin:.1f}%"
        )

    with col4:
        st.metric(
            'Expected Revenue',
            f"${p.expected_revenue:,.0f}",
            '14-day simulation'
        )

    # Constraint status
    if p.margin_pct >= min_margin:
        st.success(
            f"✓ CONSTRAINTS PASS — margin {p.margin_pct:.2f}% "
            f"is above the {min_margin:.1f}% minimum."
        )
    else:
        st.error(
            f"✗ CONSTRAINT FAILED — margin {p.margin_pct:.2f}% "
            f"is below the {min_margin:.1f}% minimum."
        )

    # ---------------------------------------------------------
    # RECOMMENDED PROMOTIONS TABLE
    # ---------------------------------------------------------
    st.subheader('📊 Recommended Promotions')

    display_cols = [
        'product_name', 'region', 'score', 'mechanism',
        'discount_pct', 'duration_days', 'target_segment',
        'expected_units', 'expected_revenue',
        'margin_pct', 'constraints'
    ]

    st.dataframe(
        plans[display_cols],
        use_container_width=True
    )

    # ---------------------------------------------------------
    # AUTONOMOUS DECISION TRACE
    # ---------------------------------------------------------
    st.subheader('🤖 Autonomous Decision Trace')

    for step in result['trace']:
        st.write('→', step)

    st.write(
        f"**Selected:** {p.product_name} — {p.region}"
    )

    for reason in str(p.reasons).split('; '):
        st.write('•', reason)

    st.write(
        f"**Strategy:** {p.mechanism}, "
        f"{p.discount_pct}% for {p.duration_days} days, "
        f"targeting **{p.target_segment}**."
    )

    st.write(
        f"**Simulation:** {p.expected_units} units / 14 days, "
        f"revenue ${p.expected_revenue:,.0f}, "
        f"margin {p.margin_pct:.2f}%."
    )
st.caption(
    'Agentic loop: Select → Strategize → Simulate → Validate → '
    'Re-plan when constraints fail → Approve'
)
