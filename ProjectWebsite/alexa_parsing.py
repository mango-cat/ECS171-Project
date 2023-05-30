import pandas as pd
import numpy as np

df = pd.read_csv("top-1m.csv", names=["ranking", "hostname"])
whitelist = list(df["hostname"].head(10000))
