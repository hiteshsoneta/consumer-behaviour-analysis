import pandas as pd

data = pd.read_json('Sports_and_Outdoors_5.json', lines=True)

review = pd.DataFrame(data.groupby('overall').size().sort_values(
    ascending=False).rename('No of Users').reset_index())


def get_data():
    return review.reviewerID.value_counts()