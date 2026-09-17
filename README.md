# MyAnimeList Anime Explorer

This project is a Streamlit application that explores anime data from a MyAnimeList dataset.

The app loads the first 50 rows of the dataset and allows users to filter and explore the anime using different controls.

## Features

* Filter anime by genre
* Filter by minimum score
* Search for anime by title
* Sort the results by score, members, popularity, or ranking
* View summary statistics for the filtered anime
* View the filtered data in a table
* Compare average anime scores by genre with an Altair bar chart
* Compare popularity and score with a Plotly scatter plot
* Reset all filters using a session state reset button

## Dataset

The dataset comes from a public MyAnimeList dataset on Kaggle.

For this assignment, the app uses:

```python
pd.read_csv("animes.csv", nrows=50)
```

This limits the application to the first 50 rows of the larger dataset.

## Run the App

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run:

```bash
streamlit run app.py
```

## Technologies

* Python
* Streamlit
* pandas
* Altair
* Plotly
