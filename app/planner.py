import pandas as pd

MIN_MARGIN_PCT = 12.0
BUDGET = 25000
DISCOUNTS = [5, 8, 10, 12, 15, 18, 20]

class PromotionPlanner:
    def __init__(self, workbook, min_margin=MIN_MARGIN_PCT):
        self.min_margin = float(min_margin)
        self.inv = pd.read_excel(workbook, sheet_name='Products_Inventory')
        self.comp = pd.read_excel(workbook, sheet_name='Competitor_Prices')
        self.holidays = pd.read_excel(workbook, sheet_name='Holidays')
        self.segments = pd.read_excel(workbook, sheet_name='Customer_Segments')
        self.rel = pd.read_excel(workbook, sheet_name='Product_Relationships')

    def competitor_signal(self, row):
        x = self.comp[(self.comp.product_id == row.product_id) & (self.comp.region == row.region)]
        if x.empty: return 0.0, None
        avg = x.competitor_price.mean()
        return (row.current_price - avg) / row.current_price * 100, x.loc[x.competitor_price.idxmin(), 'competitor']

    def score(self, row):
        stock_ratio = row.inventory_units / max(row.target_inventory, 1)
        overstock = min(max((stock_ratio - 1) / 3, 0), 1)
        aging = min(row.inventory_age_days / 120, 1)
        comp_gap, _ = self.competitor_signal(row)
        competitor = min(max(comp_gap / 15, 0), 1)
        margin = min(max((row.gross_margin_pct - self.min_margin) / 20, 0), 1)
        return round(100 * (.35*overstock + .25*aging + .25*competitor + .15*margin), 2)

    def simulate(self, row, discount):
        new_price = row.current_price * (1-discount/100)
        margin = (new_price-row.cost_price)/new_price*100
        demand_lift = 1 + discount*.035
        units = min(row.inventory_units, row.avg_daily_sales*demand_lift*14)
        revenue = new_price*units
        profit = (new_price-row.cost_price)*units
        return {'discount':discount,'price':round(new_price,2),'margin':round(margin,2),
                'units':round(units,1),'revenue':round(revenue,2),'profit':round(profit,2),
                'pass': margin >= self.min_margin and revenue*.02 <= BUDGET}

    def plan(self, row):
        gap, competitor = self.competitor_signal(row)
        candidates = [self.simulate(row,d) for d in DISCOUNTS]
        valid = [x for x in candidates if x['pass']]
        if not valid: return None
        target = self.segments[((self.segments.region=='All') | (self.segments.region==row.region)) & (self.segments.preferred_category==row.category)]
        if target.empty: target = self.segments[self.segments.region=='All']
        seg = target.sort_values('price_sensitivity',ascending=False).iloc[0]
        best = max(valid, key=lambda x: x['profit'] + x['units']*20 - x['discount']*10)
        reasons=[]
        if row.inventory_units > row.target_inventory*2: reasons.append('excess inventory')
        if row.inventory_age_days > 60: reasons.append('aging inventory')
        if gap > 3: reasons.append('competitor price pressure')
        if seg.price_sensitivity >= .7: reasons.append('price-sensitive target segment')
        return {'product_id':row.product_id,'product_name':row.product_name,'region':row.region,
                'category':row.category,'score':self.score(row),'mechanism':'Clearance Discount' if best['discount']>=15 else 'Direct Discount',
                'discount_pct':best['discount'],'duration_days':14,'target_segment':seg.segment_name,
                'competitor':competitor,'competitor_gap_pct':round(gap,2),'expected_units':best['units'],
                'expected_revenue':best['revenue'],'expected_profit':best['profit'],'margin_pct':best['margin'],
                'constraints':'PASS','reasons':'; '.join(reasons) or 'balanced opportunity'}

    def run(self, top_n=10):
        self.inv['promotion_score'] = self.inv.apply(self.score, axis=1)
        rows=[]
        for _,r in self.inv.sort_values('promotion_score',ascending=False).iterrows():
            p=self.plan(r)
            if p: rows.append(p)
        return pd.DataFrame(rows).head(top_n)
