import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.express as px
    import plotly.graph_objects as go
    return go, mo, pl, px


@app.cell
def _(mo):
    mo.md(r"""##Importing Inital Data""")
    return


@app.cell
def _(pl):
    df = pl.read_csv("data/Coffee Shop Sales.csv")
    df
    return (df,)


@app.cell
def _(df, pl):
    df1 = df.with_columns(
        pl.col("transaction_date").str.to_date("%m/%d/%Y"),
        pl.col("transaction_time").str.to_time("%H:%M:%S"),
        (pl.col("transaction_qty")*pl.col("unit_price")).alias("profit"),
    )
    df1
    return (df1,)


@app.cell
def _(df1, pl):
    df2 = df2 = df1.with_columns(
            pl.when(pl.col("transaction_date").dt.weekday() == 7)  
            .then(pl.lit("Sunday"))
            .when(pl.col("transaction_date").dt.weekday() == 1)  
            .then(pl.lit("Monday"))
            .when(pl.col("transaction_date").dt.weekday() == 2)  
            .then(pl.lit("Tuesday"))
            .when(pl.col("transaction_date").dt.weekday() == 3)  
            .then(pl.lit("Wednesday"))
            .when(pl.col("transaction_date").dt.weekday() == 4)  
            .then(pl.lit("Thursday"))
            .when(pl.col("transaction_date").dt.weekday() == 5)  
            .then(pl.lit("Friday"))
            .when(pl.col("transaction_date").dt.weekday() == 6)  
            .then(pl.lit("Saturday"))
            .alias("weekday")
        )
    df2
    return (df2,)


@app.cell
def _(mo):
    mo.md(r"""##How have Maven Roasters sales trended over time?""")
    return


@app.cell
def _(df2, pl):
    sales = df2.group_by("transaction_date").agg(
        pl.col("transaction_id").n_unique().alias("Total_Transactions")
    )
    sales1 = sales.with_columns(
        pl.col("Total_Transactions").cast(pl.Int64)
    )
    sales1
    return sales, sales1


@app.cell
def _(px, sales):
    sales_chart = px.scatter(
        sales,
        x = "transaction_date",
        y = "Total_Transactions",
        title= "Sales Over Time"
    )
    sales_chart.update_layout(
        xaxis_title="Dates", 
        yaxis_title="Sales",
    )
    return (sales_chart,)


@app.cell
def _(mo):
    mo.md(r"""##Which days of the week tend to be busiest, and why do you think that's the case?""")
    return


@app.cell
def _(df2, pl):
    df_unique = df2.unique(subset=["transaction_id"])

    transactions_per_day = (
        df_unique
        .group_by("transaction_date")
        .agg(pl.count("transaction_id").alias("total_transactions"),
             pl.col("weekday").first().alias("weekday")
        )
        .sort("transaction_date")
    )
    transactions_per_day
    return df_unique, transactions_per_day


@app.cell
def _(pl, transactions_per_day):
    average_transactions_per_weekday = (
        transactions_per_day
        .group_by("weekday")
        .agg(pl.col("total_transactions").mean().alias("average_transactions"))
    )
    average_transactions_per_weekday
    return (average_transactions_per_weekday,)


@app.cell
def _(average_transactions_per_weekday, pl):
    order1 = {
        "Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thursday": 5, "Friday" : 6, "Saturday":7, "Sunday":1 
    }
    df10 = average_transactions_per_weekday.with_columns(
        pl.col("weekday").replace(order1).alias("weekday_order")
    )
    df11 = df10.sort("weekday_order").drop("weekday_order")
    df11
    return df10, df11, order1


@app.cell
def _(df11, px):
    day_fig = px.line(
        df11,
        x="weekday",
        y="average_transactions",
        title = "How Busy Each Day of The Week is on Average "
    )
    day_fig.update_layout(
        xaxis_title="Day of the Week", 
        yaxis_title="Total Transactions",
    )
    return (day_fig,)


@app.cell
def _(mo):
    mo.md(r"""##Which products are sold most and least often? Which drive the most revenue for the business?""")
    return


@app.cell
def _(df2, pl):
    product = df2.group_by("product_category").agg(
        pl.col("transaction_qty").sum().alias("Total_Sold")
    )
    product
    return (product,)


@app.cell
def _(product):
    Top_p = product.sort("Total_Sold", descending=True).head(3)
    Top_p
    return (Top_p,)


@app.cell
def _(product):
    Bottom_p = product.sort("Total_Sold", descending=False).head(3)
    Bottom_p
    return (Bottom_p,)


@app.cell
def _(Bottom_p, Top_p, pl):
    t_b_3 = pl.concat([
        Top_p,
        Bottom_p
    ])
    Table = t_b_3.rename({
        "product_category" : "Product Category",
        "Total_Sold" :"Total Sold"
    }).sort("Total Sold", descending=True)
    Table
    return Table, t_b_3


@app.cell
def _(mo):
    mo.md(r"""##Which Location Profits the Most""")
    return


@app.cell
def _(df2, pl):
    location = df2.group_by("store_location").agg(
        pl.col("profit").sum().alias("Total_Profit")
    )
    location
    return (location,)


@app.cell
def _(location, px):
    fig_location = px.bar(
        location,
        x = "store_location",
        y = "Total_Profit",
        title = "Total Profit by Location",
        color = "store_location"
    )
    fig_location.update_layout(
        xaxis_title="Store Location", 
        yaxis_title="Profit (USD)",
        legend_title_text="Location"
    )
    fig_location
    return (fig_location,)


@app.cell
def _(mo):
    mo.md(r"""##Which Hour of the Day Profits the Most""")
    return


@app.cell
def _(df2, pl):
    hour_df = df2.with_columns(
        pl.col("transaction_time").dt.hour().alias("Hour")
    )
    hour_df
    return (hour_df,)


@app.cell
def _(hour_df, pl):
    hour_table = hour_df.group_by("Hour").agg(
        pl.col("profit").sum().alias("Total_Profit")
    )
    hour_table
    return (hour_table,)


@app.cell
def _(hour_table, px):
    fig_hour = px.bar(
        hour_table,
        x = "Hour",
        y = "Total_Profit",
        title = "Total Profit per Hour of the Day",
        color = "Hour"
    )
    fig_hour.update_layout(
        xaxis_title="Hour of the Day", 
        yaxis_title="Total Profit (USD)",
    )
    fig_hour
    return (fig_hour,)


if __name__ == "__main__":
    app.run()
