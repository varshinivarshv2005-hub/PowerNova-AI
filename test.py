from utils.simulator import generate_data
from utils.database import create_table, insert_data, fetch_data

# Create table
create_table()

# Generate and store data
for i in range(5):

    data = generate_data()

    insert_data(data)

    print("Inserted:", data)

# Fetch stored data
df = fetch_data()

print("\nDatabase Data:\n")

print(df)