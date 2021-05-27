import pandas as pd

current_timestamp = pd.to_datetime("today")
current_timestamp2 = pd.to_datetime("now").normalize
print(current_timestamp)
print(current_timestamp2)