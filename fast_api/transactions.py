import numpy as np

import pandas as pd

# Load or create the DataFrame
df = pd.DataFrame({
	'amount': [100, 200, None],
	'refunded_amount': [10, None, 5],
	'refund_status': ['completed', 'pending', 'completed']
})

df.fillna(0, inplace=True)  # Reemplazar valores nulos

X = df[['amount', 'refunded_amount']].values
y = np.where(df['refund_status'] == 'completed', 1, 0)  # Convertir a 0 y 1

