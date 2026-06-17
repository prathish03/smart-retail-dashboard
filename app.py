from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("retail_data.csv")

@app.route("/", methods=["GET", "POST"])
def dashboard():

    # ==========================
    # DASHBOARD METRICS
    # ==========================

    total_revenue = (df["Units Sold"] * df["Price"]).sum()

    total_units = df["Units Sold"].sum()

    avg_price = round(df["Price"].mean(), 2)

    avg_comp_price = round(df["Competitor Pricing"].mean(), 2)

    # ==========================
    # PRICE RECOMMENDATION
    # ==========================

    if avg_price > avg_comp_price:
        recommendation = "Reduce Price or Offer Discount"

    elif avg_price < avg_comp_price:
        recommendation = "You Can Increase Price Slightly"

    else:
        recommendation = "Maintain Current Price"

    # ==========================
    # TOP SELLING CATEGORY
    # ==========================

    top_category_data = df.groupby("Category")["Units Sold"].sum()

    top_category = top_category_data.idxmax()

    top_category_sales = int(top_category_data.max())

    # ==========================
    # AI OFFER RECOMMENDATION
    # ==========================

    avg_demand = df["Demand Forecast"].mean()

    avg_inventory = df["Inventory Level"].mean()

    if avg_demand > avg_inventory:

        offer_advice = "High Demand - Avoid Discounts"

    elif avg_comp_price < avg_price:

        offer_advice = "Competitor Cheaper - Offer 5% Discount"

    else:

        offer_advice = "Maintain Current Pricing Strategy"

    # ==========================
    # BEST SEASON
    # ==========================

    season_sales = df.groupby("Seasonality")["Units Sold"].mean()

    best_season = season_sales.idxmax()

    best_season_sales = round(season_sales.max(), 2)

    # ==========================
    # INVENTORY ALERT SYSTEM
    # ==========================

    inventory_alerts = []

    for category in df["Category"].unique():

        category_data = df[df["Category"] == category]

        avg_inventory_category = category_data["Inventory Level"].mean()

        avg_demand_category = category_data["Demand Forecast"].mean()

        if avg_inventory_category < avg_demand_category:

            inventory_alerts.append(
                f"{category} - Restock Required"
            )

    # ==========================
    # CATEGORY ENGINE
    # ==========================

    selected_category = None

    category_demand = None
    category_inventory = None

    category_price = None
    category_competitor = None

    category_advice = None

    if request.method == "POST":

        selected_category = request.form["category"]

        filtered = df[df["Category"] == selected_category]

        category_demand = round(
            filtered["Demand Forecast"].mean(), 2
        )

        category_inventory = round(
            filtered["Inventory Level"].mean(), 2
        )

        category_price = round(
            filtered["Price"].mean(), 2
        )

        category_competitor = round(
            filtered["Competitor Pricing"].mean(), 2
        )

        if category_demand > category_inventory:

            category_advice = (
                "Restock Inventory Immediately"
            )

        elif category_competitor > category_price:

            category_advice = (
                "Increase Price Slightly"
            )

        else:

            category_advice = (
                "Offer Small Discount"
            )

    return render_template(
        "dashboard.html",

        revenue=round(total_revenue, 2),

        units=total_units,

        avg_price=avg_price,

        avg_comp_price=avg_comp_price,

        recommendation=recommendation,

        top_category=top_category,

        top_category_sales=top_category_sales,

        offer_advice=offer_advice,

        best_season=best_season,

        best_season_sales=best_season_sales,

        inventory_alerts=inventory_alerts,

        categories=df["Category"].unique(),

        selected_category=selected_category,

        category_demand=category_demand,

        category_inventory=category_inventory,

        category_price=category_price,

        category_competitor=category_competitor,

        category_advice=category_advice
    )

if __name__ == "__main__":
    app.run(debug=True)