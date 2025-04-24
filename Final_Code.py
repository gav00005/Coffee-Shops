import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell
def _(pl):
    df = pl.read_excel("data/Coffee Shop Sales.xlsx")
    return (df,)


if __name__ == "__main__":
    app.run()
