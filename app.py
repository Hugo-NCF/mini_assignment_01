import streamlit as st
import pandas as pd

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

# Places the two main filters side by side
col1, col2 = st.columns(2)

with col1:
    # Lets the user choose a genre
    genre_choice = st.selectbox(
        "Filter by genre",
        genre_options
    )

with col2:
    # Lets the user choose the minimum score
    min_score = st.slider(
        "Minimum anime score",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.1,
    )

# Lets the user search for an anime by title
search_text = st.text_input(
    "Search by anime title",
    placeholder="e.g. Naruto"
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
        ["score", "members", "popularity", "ranked"]
    )

with sort_col2:
    # Lets the user switch between ascending and descending order
    ascending = st.checkbox(
        "Ascending order",
        value=False
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

