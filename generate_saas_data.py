import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_saas_dataset(seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    
    # Параметры симуляции: 24 месяца (2025-01-01 - 2026-12-01)
    months = pd.date_range(start="2025-01-01", end="2026-12-01", freq="MS")
    segments = ["SMB", "Mid-Market", "Enterprise"]
    segment_weights = [0.60, 0.30, 0.10]
    base_prices = {"SMB": 99.0, "Mid-Market": 499.0, "Enterprise": 2499.0}
    churn_probs = {"SMB": 0.055, "Mid-Market": 0.025, "Enterprise": 0.010}
    expansion_probs = {"SMB": 0.04, "Mid-Market": 0.09, "Enterprise": 0.15}
    regions = ["North America", "Europe", "APAC", "LATAM"]
    channels = ["Organic Search", "Outbound Sales", "Partner Referral", "Paid Ads"]

    records = []
    customer_counter = 1000

    for cohort_idx, cohort_month in enumerate(months):
        # Количество новых клиентов в когорте растёт со временем
        new_customers_count = int(45 + cohort_idx * 2.5 + np.random.randint(-5, 8))
        
        for _ in range(new_customers_count):
            customer_counter += 1
            cust_id = f"CUST-{customer_counter}"
            segment = np.random.choice(segments, p=segment_weights)
            region = np.random.choice(regions, p=[0.45, 0.30, 0.15, 0.10])
            channel = np.random.choice(channels)
            current_mrr = base_prices[segment]
            
            # Симуляция жизни клиента от месяца привлечения до конца периода
            for active_month in months[cohort_idx:]:
                months_since_signup = (active_month.year - cohort_month.year) * 12 + (active_month.month - cohort_month.month)
                
                if months_since_signup == 0:
                    mrr_type = "New"
                    prev_mrr = 0.0
                else:
                    prev_mrr = current_mrr
                    # Проверка на отток (Churn)
                    if np.random.rand() < churn_probs[segment]:
                        records.append({
                            "customer_id": cust_id,
                            "segment": segment,
                            "region": region,
                            "acquisition_channel": channel,
                            "cohort_month": cohort_month.strftime("%Y-%m-%d"),
                            "billing_month": active_month.strftime("%Y-%m-%d"),
                            "months_since_signup": months_since_signup,
                            "mrr_amount": 0.0,
                            "previous_mrr": round(prev_mrr, 2),
                            "mrr_change": round(-prev_mrr, 2),
                            "mrr_movement_type": "Churn",
                            "is_active": 0
                        })
                        break
                    
                    # Проверка на апсейл (Expansion) или даунгрейд (Contraction)
                    roll = np.random.rand()
                    if roll < expansion_probs[segment]:
                        upgrade_factor = np.random.choice([1.20, 1.35, 1.50])
                        current_mrr = round(current_mrr * upgrade_factor, 2)
                        mrr_type = "Expansion"
                    elif roll < expansion_probs[segment] + 0.02:
                        current_mrr = round(current_mrr * 0.80, 2)
                        mrr_type = "Contraction"
                    else:
                        mrr_type = "Retained"

                records.append({
                    "customer_id": cust_id,
                    "segment": segment,
                    "region": region,
                    "acquisition_channel": channel,
                    "cohort_month": cohort_month.strftime("%Y-%m-%d"),
                    "billing_month": active_month.strftime("%Y-%m-%d"),
                    "months_since_signup": months_since_signup,
                    "mrr_amount": round(current_mrr, 2),
                    "previous_mrr": round(prev_mrr, 2),
                    "mrr_change": round(current_mrr - prev_mrr, 2),
                    "mrr_movement_type": mrr_type,
                    "is_active": 1
                })

    df = pd.DataFrame(records)
    output_file = "saas_subscriptions_mart.csv"
    df.to_csv(output_file, index=False)
    print(f"Успешно сгенерировано {len(df)} строк для {df['customer_id'].nunique()} клиентов -> {output_file}")
    return df

if __name__ == "__main__":
    generate_saas_dataset()
