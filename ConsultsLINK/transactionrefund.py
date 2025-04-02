import pandas as pd
from conection import connect_db  # Adjusted to relative import if 'database' is in the same package

conn = connect_db()
query = "SELECT amount, refund_status, refunded_amount FROM transactions"

df = pd.read_sql(query, conn)
print(df.head())  # Ver los primeros registros
