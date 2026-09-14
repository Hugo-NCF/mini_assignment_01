import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Sets up the page title and wide layout
st.set_page_config(page_title="Anime Explorer", layout="wide")

# Main title and short description
st.title("MyAnimeList Anime Explorer")
st.caption("Explore and filter anime from the MyAnimeList dataset.")

# Loads only the first 50 rows from the CSV
df = pd.read_csv("animes.csv", nrows=50)

# Shows a quick look at the dataset
with st.expander("Peek at the raw data (df.head, df.shape, df.columns)"):
    st.dataframe(df.head())

    # Gets the number of rows and columns
    rows = df.shape[0]
    cols = df.shape[1]
    st.write(f"**df.shape** — {rows} rows, {cols} columns.")

    # Shows all column names
    st.write(list(df.columns))

# Compares an interactive dataframe with a static table
with st.expander("st.dataframe vs st.table — see the difference"):
    col_a, col_b = st.columns(2)

    with col_a:
        st.caption("st.dataframe — interactive")
        st.dataframe(df.head())

    with col_b:
        st.caption("st.table — static")
        st.table(df.head())

st.divider()

# Starts the filtering section
st.subheader("Filter the anime")

# Creates an empty list to store each genre
genres = []

# Goes through every genre entry in the dataset
for item in df["genre"].dropna():

    # Removes brackets and quotation marks
    item = item.replace("[", "").replace("]", "").replace("'", "")

    # Splits anime with multiple genres
    for genre in item.split(","):
        genre = genre.strip()

        # Prevents duplicate genres
        if genre not in genres:
            genres.append(genre)

# Sorts the genres alphabetically
genres = sorted(genres)

# Adds an option that shows every genre
genre_options = ["All genres"] + genres

# Sets the default values for the filters
if "genre_choice" not in st.session_state:
    st.session_state.genre_choice = "All genres"

if "min_score" not in st.session_state:
    st.session_state.min_score = 0.0

if "search_text" not in st.session_state:
    st.session_state.search_text = ""

if "sort_by" not in st.session_state:
    st.session_state.sort_by = "score"

if "ascending" not in st.session_state:
    st.session_state.ascending = False

# Resets all filters back to their starting values
def reset_filters():
    st.session_state.genre_choice = "All genres"
    st.session_state.min_score = 0.0
    st.session_state.search_text = ""
    st.session_state.sort_by = "score"
    st.session_state.ascending = False

# Reset button uses session state to change the widgets
st.button("Reset Filters", on_click=reset_filters)

# Places the two main filters side by side
col1, col2 = st.columns(2)

with col1:
    # Lets the user choose a genre
    genre_choice = st.selectbox(
        "Filter by genre",
        genre_options,
        key="genre_choice"
    )

with col2:
    # Lets the user choose the minimum score
    min_score = st.slider(
        "Minimum anime score",
        min_value=0.0,
        max_value=10.0,
        step=0.1,
        key="min_score"
    )

# Lets the user search for an anime by title
search_text = st.text_input(
    "Search by anime title",
    placeholder="e.g. Naruto",
    key="search_text"
)

# Keeps anime that meet the minimum score
meets_score = df["score"] >= min_score
filtered = df[meets_score]

# Applies the genre filter if one was selected
if genre_choice != "All genres":
    matches_genre = filtered["genre"].str.contains(
        genre_choice,
        case=False,
        na=False
    )
    filtered = filtered[matches_genre]

# Applies the title search if the user typed something
if search_text:
    matches_search = filtered["title"].str.contains(
        search_text,
        case=False,
        na=False
    )
    filtered = filtered[matches_search]

# Places the sorting options side by side
sort_col1, sort_col2 = st.columns(2)

with sort_col1:
    # Lets the user choose which column to sort by
    sort_by = st.selectbox(
        "Sort by",
        ["score", "members", "popularity", "ranked"],
        key="sort_by"
    )

with sort_col2:
    # Lets the user switch between ascending and descending order
    ascending = st.checkbox(
        "Ascending order",
        key="ascending"
    )

# Sorts the filtered data
filtered = filtered.sort_values(
    by=sort_by,
    ascending=ascending
)

st.divider()

# Creates three columns for summary statistics
m1, m2, m3 = st.columns(3)

# Shows how many anime are currently visible
m1.metric("Anime shown", len(filtered))

# Calculates the average score of the filtered anime
if len(filtered) > 0:
    avg_score = round(filtered["score"].mean(), 2)
else:
    avg_score = "—"

m2.metric("Average anime score", avg_score)

# Finds the highest score in the filtered anime
if len(filtered) > 0:
    highest_score = filtered["score"].max()
else:
    highest_score = "—"

m3.metric("Highest anime score", highest_score)

# Displays the final filtered dataset
st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True
)

st.divider()

# Starts the charts section
st.subheader("Charts")

# Only shows charts when at least one anime matches the filters
if len(filtered) == 0:
    st.info("No anime match the current filters. Change the filters to see charts.")

else:
    chart_col1, chart_col2 = st.columns(2)

    # Makes a separate copy of the genre and score data for the chart
    genre_data = filtered[["genre", "score"]].dropna().copy()

    # Cleans the genre text
    genre_data["genre"] = (
        genre_data["genre"]
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace("'", "", regex=False)
    )

    # Splits multiple genres into a list
    genre_data["genre"] = genre_data["genre"].str.split(",")

    # Gives each genre its own row
    genre_data = genre_data.explode("genre")

    # Removes extra spaces around genre names
    genre_data["genre"] = genre_data["genre"].str.strip()

    # Finds the average anime score for each genre
    by_genre = (
        genre_data.groupby("genre", as_index=False)["score"]
        .mean()
        .sort_values("score", ascending=False)
    )

    with chart_col1:
        st.caption(
            "Altair — average score by genre "
            "(comparing categories → bar chart)"
        )

        # Creates a bar chart comparing average score by genre
        altair_chart = (
            alt.Chart(by_genre)
            .mark_bar()
            .encode(
                x=alt.X(
                    "genre:N",
                    title="Genre",
                    sort="-y"
                ),
                y=alt.Y(
                    "score:Q",
                    title="Average Score",
                    scale=alt.Scale(domain=[0, 10])
                ),
                tooltip=[
                    "genre",
                    alt.Tooltip("score:Q", format=".2f")
                ],
            )
        )

        st.altair_chart(
            altair_chart,
            use_container_width=True
        )

    with chart_col2:
        st.caption(
            "Plotly — anime score vs. popularity "
            "(comparing two numbers → scatter plot)"
        )

        # Creates a scatter plot showing score compared to popularity
        plotly_fig = px.scatter(
            filtered,
            x="popularity",
            y="score",
            hover_name="title",
            title="Score vs. Popularity"
        )

        # Keeps anime scores on their normal 0 to 10 scale
        plotly_fig.update_yaxes(range=[0, 10])

        st.plotly_chart(
            plotly_fig,
            use_container_width=True
        )