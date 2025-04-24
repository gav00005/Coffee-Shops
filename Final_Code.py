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
def _(mo):
    mo.md(r"""##Which days of the week tend to be busiest, and why do you think that's the case?""")
    return


@app.cell
def _(mo):
    mo.md(r"""##Which products are sold most and least often? Which drive the most revenue for the business?""")
    return


@app.cell
def _(mo):
    mo.md(r"""##Which Location Profits the Most""")
    return


@app.cell
def _(mo):
    mo.md(r"""##Which Hour of the Day Profits the Most""")
    return


if __name__ == "__main__":
    app.run()
