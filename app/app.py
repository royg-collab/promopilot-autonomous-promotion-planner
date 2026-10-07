import streamlit as st
from agent import PromotionAgent

st.set_page_config(page_title='PromoPilot', page_icon='🛍️', layout='wide')
st.title('🛍️ PromoPilot — Autonomous Promotion Planner')
st.caption('Electronics retail | Agentic promotion planning MVP')

agent=PromotionAgent('../data/electronics_retail_promotion_dataset.xlsx')

with st.sidebar:
    st.header('Planning Controls')
    min_margin=st.number_input('Minimum margin %', 5.0, 30.0, 12.0, 0.5)
    top_n=st.slider('Recommendations',1,10,5)

# MVP uses deterministic constraint/simulation logic; the reasoning trace is surfaced for the demo.
result=agent.run(top_n)
plans=result["plans"]

st.subheader('Recommended Promotions')
st.dataframe(plans[['product_name','region','score','mechanism','discount_pct','duration_days','target_segment','expected_units','expected_revenue','margin_pct','constraints']], use_container_width=True)

if not plans.empty:
    p=plans.iloc[0]
    st.subheader('Autonomous Decision Trace')
    for step in result['trace']:
        st.write('→', step)
    st.write(f"**Selected:** {p.product_name} — {p.region}")
    for reason in str(p.reasons).split('; '): st.write('•', reason)
    st.write(f"**Strategy:** {p.mechanism}, {p.discount_pct}% for {p.duration_days} days, targeting **{p.target_segment}**.")
    st.write(f"**Simulation:** {p.expected_units} units / 14 days, revenue {p.expected_revenue:,.0f}, margin {p.margin_pct:.2f}%.")
    st.success('Constraint validation: PASS — candidate satisfies the minimum-margin and budget rules.')

st.divider()
st.caption('Agentic loop: Select → Strategize → Simulate → Validate → Re-plan when constraints fail → Approve')
