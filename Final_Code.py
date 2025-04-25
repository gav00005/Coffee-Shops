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
def _(mo):
    mo.md(r"""###The first thing we did was import the dataset for the Coffee Shop Sales which can be seen below""")
    return


@app.cell
def _(pl):
    df = pl.read_csv("data/Coffee Shop Sales.csv")
    df
    return (df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ###Then Next Part Was Updating the Table as Seen Below
        Columns that had to do with time recieved the proper units, and a revenue column was made to track the revenue made per transaction. The str.to_time function can be found here https://docs.pola.rs/user-guide/concepts/data-types-and-structures/#data-types
        """
    )
    return


@app.cell
def _(df, pl):
    df1 = df.with_columns(
        pl.col("transaction_date").str.to_date("%m/%d/%Y"),
        pl.col("transaction_time").str.to_time("%H:%M:%S"),
        (pl.col("transaction_qty")*pl.col("unit_price")).alias("revenue"),
    )
    df1
    return (df1,)


@app.cell
def _(mo):
    mo.md(
        """
        ###The Final Thing Added For the Inital Setup Was a Column that Showed the Day of the Week
        Which can be seen below:
        """
    )
    return


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
    mo.md(r"""##How have Maven Roasters Sales trended over time?""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ###Creating New Dataframe
        The team created a dataframe that just included the transaction date, and grouped it with the total transactions that happened that day while also removing repeated transactions. The table can be seen below:
        """
    )
    return


@app.cell
def _(df2, pl):
    sales = df2.group_by("transaction_date").agg(
        pl.col("transaction_id").n_unique().alias("Total_Transactions")
    )
    sales
    return (sales,)


@app.cell
def _(mo):
    mo.md(
        """
        ###Maven Roasters Sales Over Time Scatter Plot
        The Team decided that a Scatter plot would best show how the sales have changed over time. From the scatter plot below the team can confidently say that Maven Roasters Sales have been steadily increasing over time.
        """
    )
    return


@app.cell
def _(px, sales):
    sales_chart = px.scatter(
        sales,
        x = "transaction_date",
        y = "Total_Transactions",
        title= "Maven Roasters Sales Over Time"
    )
    sales_chart.update_layout(
        xaxis_title="Dates", 
        yaxis_title="Sales",
    )
    sales_chart
    return (sales_chart,)


@app.cell
def _(mo):
    mo.md(r"""##Which days of the week tend to be busiest, and why do you think that's the case?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ###Intial New Data Frame Setup
        The first step to solving this problem was setting up a new dataframe. To do this the team first removed the repeating transaction ID's, then made a table grouped by the total transactions. When first made the weekday column displayed a bunch of the same days, so after looking at the polars Guide .first() was found here to fix this. The link and table are below:
        https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.dataframe.group_by.GroupBy.first.html
        """
    )
    return


@app.cell
def _(df2, pl):
    df_unique = df2.unique(subset=["transaction_id"])

    df_transpd = (
        df_unique
        .group_by("transaction_date")
        .agg(pl.count("transaction_id").alias("total_transactions"),
             pl.col("weekday").first()
        )
        .sort("transaction_date")
    )
    df_transpd
    return df_transpd, df_unique


@app.cell
def _(mo):
    mo.md(r"""###A Dataframe was Then Made to Show Sales Averages per Day of the Week""")
    return


@app.cell
def _(df_transpd, pl):
    df_av = (
        df_transpd
        .group_by("weekday")
        .agg(pl.col("total_transactions").mean().alias("average_transactions"))
    )
    df_av
    return (df_av,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ###Final Data Frame
        For the final data frame for this section to be useful it needed to be ordered by day of the week. So a dictionary was created to map the days of the week to a number, than inserted into the dataframe and then sorted by that. 
        """
    )
    return


@app.cell
def _(df_av, pl):
    order = {
        "Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thursday": 5, "Friday" : 6, "Saturday":7, "Sunday":1 
    }
    df_av2 = df_av.with_columns(
        pl.col("weekday").replace(order).alias("weekday_order")
    )
    df_av3 = df_av2.sort("weekday_order")
    df_av3
    return df_av2, df_av3, order


@app.cell
def _(mo):
    mo.md(
        """
        ###Final Graph
        A Line graph was chosen to better show the differences between the transactional averages per day. It can be seen that Monday, Thursday and Friday have the highest averages. This makes sense as people generally want coffee on Monday to get a good start of the week, and on Thursday and Friday so that they can get through the day faster for the weekend. 
        """
    )
    return


@app.cell
def _(df_av3, px):
    av_fig = px.line(
        df_av3,
        x="weekday",
        y="average_transactions",
        title = "Average Amount of Transactions per Day"
    )
    av_fig.update_layout(
        xaxis_title="Day of the Week", 
        yaxis_title="Transaction Number",
    )
    av_fig
    return (av_fig,)


@app.cell
def _(mo):
    mo.md(r"""##Which products are sold most and least often? Which drive the most revenue for the business?""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ###Product Table
        A table that shows the top 3 most and least sold products was produced. When looking at said table Coffee, Tea, and Bakery items were sold the most, while Loose Tea, Branded, and Packaged Chocolate Items were sold the least
        """
    )
    return


@app.cell
def _(df2, pl):
    prod = df2.group_by("product_category").agg(
        pl.col("transaction_qty").sum().alias("total_sold")
    )
    Top_p = prod.sort("total_sold", descending=True).head(3)
    Bottom_p = prod.sort("total_sold", descending=False).head(3)
    prod_comb = pl.concat([
        Top_p,
        Bottom_p
    ])
    prod_comb2 = prod_comb.sort("total_sold", descending = True)
    prod_comb3 = prod_comb2.rename({
        "product_category":"Product Type",
        "total_sold":"Amount Sold"
    })
    prod_comb3
    return Bottom_p, Top_p, prod, prod_comb, prod_comb2, prod_comb3


@app.cell
def _(mo):
    mo.md(
        """
        ###Revenue Table
        Like above a table was created to show the top and bottom 3 products with the lowest revenue. When looking at the table you can see that Coffee, Tea, and Bakery items produce the most revenue, while Loose Tea, Flavours, and Packaged Chocolate produce the least revenue. 
        """
    )
    return


@app.cell
def _(hour_df, pl):
    prod_rev = hour_df.group_by("product_category").agg(
        pl.col("revenue").sum().alias("total_revenue").round(2)
    )
    Top_rev = prod_rev.sort("total_revenue", descending=True).head(3)
    bot_rev = prod_rev.sort("total_revenue", descending=False).head(3)
    rev_comb = pl.concat([
        Top_rev,
        bot_rev
    ])
    rev_comb2 = rev_comb.sort("total_revenue", descending = True)
    rev_comb3 = rev_comb2.rename({
        "product_category" : "Product Type",
        "total_revenue" : "Product Revenue"})
    rev_comb3 
    return Top_rev, bot_rev, prod_rev, rev_comb, rev_comb2, rev_comb3


@app.cell
def _(mo):
    mo.md(r"""##Which Produces the Most Revenue""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ###Revenue Data Frame
        The first step was creating a dataframe that added total revenue for each location, which can be seen below:
        """
    )
    return


@app.cell
def _(df2, pl):
    location = df2.group_by("store_location").agg(
        pl.col("revenue").sum().alias("total_revenue").round(2)
    )
    location.sort("total_revenue", descending=True)
    location
    return (location,)


@app.cell
def _(mo):
    mo.md(
        """
        ###Location Revenue Chart
        From the chart below it can be see that Maven Roasters makes about the same amount of revenue from each location, with the Hell's Kitchen Location Slightly leading the Pack in terms of Revenue. 
        """
    )
    return


@app.cell
def _(location, px):
    fig_location = px.bar(
        location,
        x = "store_location",
        y = "total_revenue",
        title = "Maven Roasters Total Revenue by Location",
        color = "store_location"
    )
    fig_location.update_layout(
        xaxis_title="Store Location", 
        yaxis_title="Revenue (USD)",
        legend_title_text="Location"
    )
    fig_location
    return (fig_location,)


@app.cell
def _(mo):
    mo.md(r"""##Which Hour of the Day Generates the Most Revenue""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ###Adding Hour of Day Column
        The first step was adding an hour of the day coloumn to the cleaned data frame
        """
    )
    return


@app.cell
def _(df2, pl):
    hour_df = df2.with_columns(
        pl.col("transaction_time").dt.hour().alias("Hour")
    )
    hour_df
    return (hour_df,)


@app.cell
def _(mo):
    mo.md(
        """
        ###Creating New Data Frame
        The next step was creating a data frame that shows the total revenue by hour of the day, which can be seen below
        """
    )
    return


@app.cell
def _(hour_df, pl):
    hour_table = hour_df.group_by("Hour").agg(
        pl.col("revenue").sum().alias("Total_Revenue").round(2)
    )
    hour_table2 = hour_table.sort("Hour", descending=False)
    hour_table2
    return hour_table, hour_table2


@app.cell
def _(hour_table2, px):
    fig_hour = px.bar(
        hour_table2,
        x = "Hour",
        y = "Total_Revenue",
        title = "Revenue by Hour of the Day",
        color = "Hour"
    )
    fig_hour.update_layout(
        xaxis_title="Hour of the Day", 
        yaxis_title="Total Revenue (USD)",
    )
    fig_hour
    return (fig_hour,)


if __name__ == "__main__":
    app.run()
