#Data processing libraries
import numpy as np
import pandas as pd

#Visualization libraries
import warnings
import matplotlib.pyplot as plt

## %matplotlib inline
## %config InlineBackend.figure_format = "retina"

#Personal libraries
import usr_lib.db_handler as dbh

def main():
    df_yf = dbh.get_stock_yf("AAPL")
    print(df_yf)
    
if __name__ == "__main__":
    main()