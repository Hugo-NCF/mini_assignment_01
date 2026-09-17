# Mini Assignment 1 Rationale

I chose the MyAnimeList anime dataset because anime is something I am interested in, and I wanted to work with data that I actually care about. This dataset can help answer questions such as which genres tend to have higher ratings and whether more popular anime also tend to have higher scores.

One limitation of the dataset is that this project only loads the first 50 rows using `nrows=50`. Because of this, the results shown in the app do not represent every anime in the full dataset. Some genres may also appear more often than others in this smaller sample.

The summary metrics I chose are the number of anime shown, the average score, and the highest score. These are useful because they change based on the user's filters and give a quick summary of the anime currently being viewed.

For the charts, I used an Altair bar chart to show the average score by genre because bar charts make it easy to compare categories. I used a Plotly scatter plot to compare anime score and popularity because a scatter plot makes it easier to see whether there is a relationship between two numerical values. Both charts update whenever the filters change.
