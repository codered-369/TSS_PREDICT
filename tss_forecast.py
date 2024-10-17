# 16 - 10 -2024

# import re
# import pandas as pd
# from prophet import Prophet
# import matplotlib.pyplot as plt
# import os
# import time

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"  # Ensure this file contains the raw data

# # 1. Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # 2. Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     """Extracts date, product, and prices from raw TSS data."""
#     data = []

#     # Pattern to extract dates like '16.10.2024'
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     # Split raw text by 'TSS MARKET' sections
#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         # Extract date from the block
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue  # Skip if no date found

#         # Extract products and prices from the block
#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:  # Skip headers
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     # Convert to DataFrame
#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # 3. Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()


# # 4. Extract and clean the new data
# new_data = extract_data_from_text(raw_input_data)

# # 5. Combine the existing cleaned data with the new data
# df = pd.concat([df, new_data], ignore_index=True)

# # 6. Save the updated dataset back to the CSV
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # 7. Forecast for all products using the updated data
# os.makedirs("forecast_graphs", exist_ok=True)
# products = df["Product"].unique()

# for product in products:
#     # Filter data for the current product
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})

#     # Ensure the 'ds' column is datetime type
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')

#     # Drop rows with NaT in the 'ds' column after conversion
#     df_product = df_product.dropna(subset=['ds'])

#     # Aggregate duplicate entries by taking the mean
#     df_product = df_product.groupby('ds').mean().reset_index()

#     # Skip products with fewer than 2 data points
#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     # Limit data to the most recent 60 days for faster processing
#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]

#     # Handle irregular date ranges by resampling to daily frequency
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     # Train the Prophet model and log the time taken
#     start_time = time.time()
#     model = Prophet()
#     model.fit(df_product)
#     print(f"Training time for {product}: {time.time() - start_time:.2f} seconds")

#     # Make predictions for the next 30 days
#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Plot and display the forecast
#     fig = model.plot(forecast)
#     plt.title(f"{product} Price Forecast")
#     plt.xlabel("Date")
#     plt.ylabel("Average Price (₹/Qtl)")
#     plt.show()

#     # Sanitize product name for filename
#     sanitized_product_name = (
#         product.strip()
#         .replace(' ', '_')
#         .replace('\n', '_')
#         .replace('/', '_')
#         .replace('\\', '_')
#     )

#     # Save the graph
#     graph_path = f"forecast_graphs/{sanitized_product_name}_forecast.png"
#     fig.savefig(graph_path)
#     plt.close()
#     print(f"Saved forecast graph for {product} at {graph_path}")








# 17-10-2024

# import re
# import pandas as pd
# from prophet import Prophet
# import matplotlib.pyplot as plt
# import os
# import time
# import math

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # 1. Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # 2. Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # 3. Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# os.makedirs("forecast_graphs", exist_ok=True)
# products = df["Product"].unique()

# # Calculate number of rows and columns for subplots
# n_products = len(products)
# n_cols = 8  # Number of columns for better layout
# n_rows = math.ceil(n_products / n_cols)

# # Create subplots with multiple columns
# fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(15, 10 * n_rows))
# axes = axes.flatten()  # Flatten axes for easier indexing

# for i, product in enumerate(products):
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     start_time = time.time()
#     model = Prophet()
#     model.fit(df_product)
#     print(f"Training time for {product}: {time.time() - start_time:.2f} seconds")

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Plot the forecast on the respective subplot
#     model.plot(forecast, ax=axes[i])
#     axes[i].set_title(f"{product} Price Forecast")
#     axes[i].set_xlabel("Date")
#     axes[i].set_ylabel("Average Price (₹/Qtl)")

# # Remove unused subplots (if any)
# for j in range(i + 1, len(axes)):
#     fig.delaxes(axes[j])

# plt.tight_layout()  # Adjust layout to avoid overlap
# plt.show()



# 2nd edited


# import re
# import pandas as pd
# from prophet import Prophet
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# import os
# import math

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # 1. Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # 2. Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # 3. Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# products = df["Product"].unique()
# n_products = len(products)

# # Calculate the number of rows and columns for subplots
# n_cols = 2  # 2 graphs per row
# n_rows = math.ceil(n_products / n_cols)

# # Create a scrollable subplot layout
# fig = make_subplots(
#     rows=n_rows, cols=n_cols,
#     subplot_titles=[f"{product} Price Forecast" for product in products],
#     vertical_spacing=0.02  # Adjusted vertical spacing
# )

# # Loop through each product and generate the forecast
# for i, product in enumerate(products):
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Add forecast to the subplot
#     row = (i // n_cols) + 1
#     col = (i % n_cols) + 1

#     fig.add_trace(
#         go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name=f"{product} Forecast"),
#         row=row, col=col
#     )
#     fig.add_trace(
#         go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name=f"{product} Actual"),
#         row=row, col=col
#     )

# # Set the layout with a scrollable height
# fig.update_layout(
#     height=800,  # Adjust height as needed for scrollable effect
#     showlegend=False,
#     title_text="Product Price Forecasts"
# )

# # Display the interactive plot
# fig.show()




# 3rd edit




# import re
# import pandas as pd
# from prophet import Prophet
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# import os
# import math

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# products = df["Product"].unique()
# n_products = len(products)

# # Calculate the number of rows and columns for subplots
# n_cols = 2  # 2 graphs per row
# n_rows = math.ceil(n_products / n_cols)

# # Create a scrollable subplot layout with increased height and adjusted spacing
# fig = make_subplots(
#     rows=n_rows, cols=n_cols,
#     subplot_titles=[f"{product} Price Forecast" for product in products],
#     vertical_spacing=0.01  # Adjusted vertical spacing
# )

# # Loop through each product and generate the forecast
# for i, product in enumerate(products):
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Add forecast to the subplot
#     row = (i // n_cols) + 1
#     col = (i % n_cols) + 1

#     fig.add_trace(
#         go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name=f"{product} Forecast"),
#         row=row, col=col
#     )
#     fig.add_trace(
#         go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name=f"{product} Actual"),
#         row=row, col=col
#     )

# # Set the layout with increased height and smaller font sizes
# fig.update_layout(
#     height=1200,  # Increased height for better visibility
#     title_text="Product Price Forecasts",
#     title_font_size=20,
#     font=dict(size=10)  # Smaller font size
# )

# # Display the interactive plot
# fig.show()



# 4rh edit  
# import re
# import pandas as pd
# from prophet import Prophet
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# import os
# import math

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# products = df["Product"].unique()
# n_products = len(products)

# # Create a grid layout for the subplots
# n_cols = 2  # 2 graphs per row
# n_rows = math.ceil(n_products / n_cols)

# # Create the figure with adjusted subplot sizes
# fig = make_subplots(
#     rows=n_rows, cols=n_cols,
#     subplot_titles=[f"{product} Price Forecast" for product in products],
#     vertical_spacing=0.03  # Set to a smaller value
# )

# # Loop through each product and generate the forecast
# for i, product in enumerate(products):
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Add forecast to the subplot
#     row = (i // n_cols) + 1
#     col = (i % n_cols) + 1

#     fig.add_trace(
#         go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name=f"{product} Forecast"),
#         row=row, col=col
#     )
#     fig.add_trace(
#         go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name=f"{product} Actual"),
#         row=row, col=col
#     )

# # Set the layout with adjusted sizes for better visibility
# fig.update_layout(
#     height=1200,  # Increased height for better visibility
#     title_text="Product Price Forecasts",
#     title_font_size=20,
#     font=dict(size=10),  # Smaller font size
# )

# # Display the interactive plot
# fig.show()




















# 5th edition 

# import re
# import pandas as pd
# from prophet import Prophet
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# import os
# import math

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# products = df["Product"].unique()

# # Set the number of columns for subplots
# n_cols = 2  # Adjust this value for more or fewer columns
# n_products = len(products)
# n_rows = math.ceil(n_products / n_cols)

# # Create the figure
# fig = make_subplots(
#     rows=n_rows, cols=n_cols,
#     subplot_titles=[f"{product} Price Forecast" for product in products],
#     vertical_spacing=0.04  # Adjust this as necessary
# )

# # Loop through each product and generate the forecast
# for i, product in enumerate(products):
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Add forecast to the subplot
#     row = (i // n_cols) + 1
#     col = (i % n_cols) + 1

#     fig.add_trace(
#         go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name=f"{product} Forecast"),
#         row=row, col=col
#     )
#     fig.add_trace(
#         go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name=f"{product} Actual"),
#         row=row, col=col
#     )

# # Set the layout with increased height for better visibility
# fig.update_layout(
#     height=1200,  # Adjust height for scrolling
#     title_text="Product Price Forecasts",
#     title_font_size=20,
#     font=dict(size=12),  # Adjust font size
# )

# # Display the interactive plot
# fig.show()





# 6th edition   

# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # Initialize the Dash app
# app = Dash(__name__)

# # Get unique products
# products = df["Product"].unique()

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products],
#         value=products[0],  # Set default value
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     df_product = df[df["Product"] == selected_product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         return go.Figure()  # Return an empty figure if not enough data

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Create the forecast graph
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#     fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#     fig.update_layout(
#         title=f"{selected_product} Price Forecast",
#         xaxis_title="Date",
#         yaxis_title="Price",
#         height=600
#     )
    
#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)







# 7th



# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # Filter products with sufficient data for forecasting
# products_with_data = df.groupby("Product").filter(lambda x: len(x) > 1)["Product"].unique()

# # Initialize the Dash app
# app = Dash(__name__)

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products_with_data],
#         value=products_with_data[0] if products_with_data.size > 0 else None,  # Set default value if available
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     if selected_product is None:  # Handle case where no product is selected
#         return go.Figure()

#     df_product = df[df["Product"] == selected_product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         return go.Figure()  # Return an empty figure if not enough data

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Create the forecast graph
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#     fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#     fig.update_layout(
#         title=f"{selected_product} Price Forecast",
#         xaxis_title="Date",
#         yaxis_title="Price",
#         height=600
#     )
    
#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)




# 8th 


# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # Preprocess all product data and store forecasts
# forecasts = {}
# products_with_data = df.groupby("Product").filter(lambda x: len(x) > 1)["Product"].unique()

# for product in products_with_data:
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     # Check for sufficient data before fitting the model
#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue  # Skip to the next product if not enough data

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Store forecast data
#     forecasts[product] = (forecast, df_product)

# # Initialize the Dash app
# app = Dash(__name__)

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products_with_data],
#         value=products_with_data[0] if products_with_data.size > 0 else None,  # Set default value if available
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     if selected_product is None:  # Handle case where no product is selected
#         return go.Figure()

#     # Debugging: Print selected product
#     print(f"Selected product: {selected_product}")

#     try:
#         forecast, df_product = forecasts[selected_product]

#         # Create the forecast graph
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#         fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#         fig.update_layout(
#             title=f"{selected_product} Price Forecast",
#             xaxis_title="Date",
#             yaxis_title="Price",
#             height=600
#         )
        
#         return fig

#     except Exception as e:
#         print(f"Error while updating graph for {selected_product}: {e}")
#         return go.Figure()  # Return an empty figure in case of error

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)











# 9th edition 


# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"([^\d]+?)\s+(\d+)\s+(\d+)\s+(\d+)")  # Updated regex to better capture product names

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product = match[0].strip()  # Strip whitespace from product name
#             min_price, max_price, avg_price = match[1:]

#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
            
#             data.append([current_date, product, int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # Preprocess all product data and store forecasts
# forecasts = {}
# products_with_data = df.groupby("Product").filter(lambda x: len(x) > 1)["Product"].unique()

# for product in products_with_data:
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     # Check for sufficient data before fitting the model
#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue  # Skip to the next product if not enough data

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Store forecast data
#     forecasts[product] = (forecast, df_product)

# # Initialize the Dash app
# app = Dash(__name__)

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products_with_data],
#         value=products_with_data[0] if products_with_data.size > 0 else None,  # Set default value if available
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     if selected_product is None:  # Handle case where no product is selected
#         return go.Figure()

#     # Debugging: Print selected product
#     print(f"Selected product: {selected_product}")

#     try:
#         forecast, df_product = forecasts[selected_product]

#         # Create the forecast graph
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#         fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#         fig.update_layout(
#             title=f"{selected_product} Price Forecast",
#             xaxis_title="Date",
#             yaxis_title="Price",
#             height=600
#         )
        
#         return fig

#     except Exception as e:
#         print(f"Error while updating graph for {selected_product}: {e}")
#         return go.Figure()  # Return an empty figure in case of error

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)





# 10th edition 




# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text




# def extract_data_from_text(raw_text):
#     # Define the products you want to keep
#     valid_products = ["Rashi", "Bette", "Kole", "Chali", "OldCh", "Pepper"]
    
#     # Prepare to store valid data
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")  # Date: DD.MM.YYYY
#     product_pattern = re.compile(r"([A-Za-z\s\.]+)\s+(\d+)\s+(\d+)\s+(\d+)")  # Product + Prices

#     # Split the input based on 'TSS MARKET' blocks
#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         # Extract date from each block
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue  # Skip if no valid date is found

#         # Find all product matches in the block
#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match

#             # Clean and normalize the product name
#             product = product.strip().replace(".", "").replace(" ", "")

#             # Check if the product is in the valid product list
#             if any(valid.lower() in product.lower() for valid in valid_products):
#                 # Append only the relevant product data
#                 data.append([current_date, product, int(min_price), int(max_price), int(avg_price)])

#     # Convert to DataFrame and drop duplicate products (if any)
#     df = pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
#     df = df.drop_duplicates(subset=["Product", "Date"])  # Avoid duplicate entries

#     return df

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# # Extract and save the cleaned data
# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # Preprocess all product data and store forecasts
# forecasts = {}
# products_with_data = df.groupby("Product").filter(lambda x: len(x) > 1)["Product"].unique()

# for product in products_with_data:
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         print(f"Skipping {product} due to insufficient data.")
#         continue

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Store forecast data
#     forecasts[product] = (forecast, df_product)

# # Initialize the Dash app
# app = Dash(__name__)

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products_with_data],
#         value=products_with_data[0] if products_with_data.size > 0 else None,
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     if selected_product is None:
#         return go.Figure()

#     print(f"Selected product: {selected_product}")

#     try:
#         forecast, df_product = forecasts[selected_product]

#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#         fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#         fig.update_layout(
#             title=f"{selected_product} Price Forecast",
#             xaxis_title="Date",
#             yaxis_title="Price",
#             height=600
#         )

#         return fig

#     except Exception as e:
#         print(f"Error while updating graph for {selected_product}: {e}")
#         return go.Figure()

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)






# 11th edition 



# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"
# VALID_PRODUCTS = ["Rashi", "Bette", "Kole", "Chali", "OldCh", "Pepper"]

# # Load existing cleaned data
# if not os.path.exists(DATA_FILE):
#     print("Data file not found! Creating a new one.")
#     df = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
# else:
#     df = pd.read_csv(DATA_FILE)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")  # Date: DD.MM.YYYY
#     product_pattern = re.compile(r"([A-Za-z\s\.]+)\s+(\d+)\s+(\d+)\s+(\d+)")  # Product + Prices

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         # Extract date from the block
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue  # Skip if no date is found

#         # Find all product matches
#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match

#             # Clean and normalize product name
#             product = product.strip().replace(".", "").replace(" ", "")

#             # Keep only relevant products
#             if any(valid.lower() in product.lower() for valid in VALID_PRODUCTS):
#                 data.append([current_date, product, int(min_price), int(max_price), int(avg_price)])

#     # Create DataFrame and remove duplicates (if any)
#     df = pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])
#     df = df.drop_duplicates(subset=["Product", "Date"])  # Avoid duplicate entries

#     return df

# # Read raw text data from the input file
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# # Extract new data and update the main DataFrame
# new_data = extract_data_from_text(raw_input_data)
# df = pd.concat([df, new_data], ignore_index=True)
# df.to_csv(DATA_FILE, index=False)
# print(f"New data saved to {DATA_FILE}")

# # Initialize the Dash app
# app = Dash(__name__)

# # Get unique products for the dropdown
# products = df["Product"].unique()

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products],
#         value=products[0] if len(products) > 0 else None,  # Set default if available
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Precompute forecasts for all products to avoid recalculation on click
# forecast_data = {}
# for product in products:
#     df_product = df[df["Product"] == product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] >= 2:  # Only forecast if enough data points
#         max_date = df_product['ds'].max()
#         df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#         df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#         model = Prophet()
#         model.fit(df_product)
#         future = model.make_future_dataframe(periods=30)
#         forecast = model.predict(future)

#         # Store forecast for later use
#         forecast_data[product] = forecast

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     if selected_product not in forecast_data:
#         return go.Figure()  # Return an empty figure if no forecast data available

#     forecast = forecast_data[selected_product]
#     df_product = df[df["Product"] == selected_product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})

#     # Create the forecast graph
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#     fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#     fig.update_layout(
#         title=f"{selected_product} Price Forecast",
#         xaxis_title="Date",
#         yaxis_title="Price",
#         height=600
#     )

#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)









# 12th



# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"
# VALID_PRODUCTS = ['Rashi', 'Bette', 'Kole', 'Chali', 'Old Ch', 'Pepper']

# # Check if the input file exists
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# # Extract new data from the raw input and filter only valid products
# new_data = extract_data_from_text(raw_input_data)
# filtered_data = new_data[new_data["Product"].isin(VALID_PRODUCTS)]

# # Clear existing data and save the new data to CSV
# if not filtered_data.empty:
#     filtered_data.to_csv(DATA_FILE, index=False)
#     print(f"Fresh data saved to {DATA_FILE} with {len(filtered_data)} records.")
# else:
#     print("No valid product data found in the input file. Please check the contents.")

# # Initialize the Dash app
# app = Dash(__name__)

# # Get unique products from the filtered data
# products = filtered_data["Product"].unique()

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products],
#         value=products[0] if products.size > 0 else None,  # Set default value if products exist
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     df_product = filtered_data[filtered_data["Product"] == selected_product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         return go.Figure()  # Return an empty figure if not enough data

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Create the forecast graph
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#     fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#     fig.update_layout(
#         title=f"{selected_product} Price Forecast",
#         xaxis_title="Date",
#         yaxis_title="Price",
#         height=600
#     )
    
#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)








# 13th  

# correct working code 




# import re
# import pandas as pd
# from prophet import Prophet
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objs as go
# import os

# # Constants
# DATA_FILE = "data.csv"
# INPUT_FILE = "tss_input.txt"
# VALID_PRODUCTS = ['Rashi', 'Bette', 'Kole', 'Chali', 'Old Ch', 'Pepper']

# # Check if the input file exists
# if not os.path.exists(INPUT_FILE):
#     print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
#     exit(1)

# # Load existing cleaned data if it exists
# if os.path.exists(DATA_FILE):
#     existing_data = pd.read_csv(DATA_FILE)
# else:
#     existing_data = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Function to clean and extract data from raw text
# def extract_data_from_text(raw_text):
#     data = []
#     date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
#     product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

#     blocks = raw_text.split("TSS MARKET")[1:]

#     for block in blocks:
#         date_match = date_pattern.search(block)
#         if date_match:
#             current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
#         else:
#             continue

#         for match in product_pattern.findall(block):
#             product, min_price, max_price, avg_price = match
#             if product.lower() in ["items", "kg.", "total", "bags"]:
#                 continue
#             data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

#     return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# # Read raw text data from the input file
# with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#     raw_input_data = f.read()

# # Extract new data from the raw input and filter only valid products
# new_data = extract_data_from_text(raw_input_data)
# filtered_data = new_data[new_data["Product"].isin(VALID_PRODUCTS)]

# # Append new data to existing data and remove duplicates
# if not filtered_data.empty:
#     combined_data = pd.concat([existing_data, filtered_data]).drop_duplicates().reset_index(drop=True)
#     combined_data.to_csv(DATA_FILE, index=False)
#     print(f"Data saved to {DATA_FILE} with {len(combined_data)} records.")
# else:
#     print("No valid product data found in the input file. Please check the contents.")

# # Initialize the Dash app
# app = Dash(__name__)

# # Get unique products from the combined data
# products = combined_data["Product"].unique()

# # Layout of the Dash app
# app.layout = html.Div([
#     html.H1("Product Price Forecasts"),
#     dcc.Dropdown(
#         id='product-dropdown',
#         options=[{'label': product, 'value': product} for product in products],
#         value=products[0] if products.size > 0 else None,  # Set default value if products exist
#         clearable=False
#     ),
#     dcc.Graph(id='forecast-graph')
# ])

# # Callback to update the graph based on the selected product
# @app.callback(
#     Output('forecast-graph', 'figure'),
#     Input('product-dropdown', 'value')
# )
# def update_graph(selected_product):
#     df_product = combined_data[combined_data["Product"] == selected_product][["Date", "Avg Price"]]
#     df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
#     df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
#     df_product = df_product.dropna(subset=['ds'])
#     df_product = df_product.groupby('ds').mean().reset_index()

#     if df_product.shape[0] < 2:
#         return go.Figure()  # Return an empty figure if not enough data

#     max_date = df_product['ds'].max()
#     df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
#     df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

#     model = Prophet()
#     model.fit(df_product)

#     future = model.make_future_dataframe(periods=30)
#     forecast = model.predict(future)

#     # Create the forecast graph
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
#     fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual'))

#     fig.update_layout(
#         title=f"{selected_product} Price Forecast",
#         xaxis_title="Date",
#         yaxis_title="Price",
#         height=600
#     )
    
#     return fig


# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

















# 14th 












import re
import pandas as pd
from prophet import Prophet
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import os

# Constants
DATA_FILE = "data.csv"
INPUT_FILE = "tss_input.txt"
VALID_PRODUCTS = ['Rashi', 'Bette', 'Kole', 'Chali', 'Old Ch', 'Pepper']

# Check if the input file exists
if not os.path.exists(INPUT_FILE):
    print(f"Input file '{INPUT_FILE}' not found. Please create it with the raw data.")
    exit(1)

# Load existing cleaned data if it exists
if os.path.exists(DATA_FILE):
    existing_data = pd.read_csv(DATA_FILE)
else:
    existing_data = pd.DataFrame(columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# Function to clean and extract data from raw text
def extract_data_from_text(raw_text):
    data = []
    date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    product_pattern = re.compile(r"(\w[\w\s]*?)\s+(\d+)\s+(\d+)\s+(\d+)")

    blocks = raw_text.split("TSS MARKET")[1:]

    for block in blocks:
        date_match = date_pattern.search(block)
        if date_match:
            current_date = pd.to_datetime(date_match.group(1), format="%d.%m.%Y")
        else:
            continue

        for match in product_pattern.findall(block):
            product, min_price, max_price, avg_price = match
            if product.lower() in ["items", "kg.", "total", "bags"]:
                continue
            data.append([current_date, product.strip(), int(min_price), int(max_price), int(avg_price)])

    return pd.DataFrame(data, columns=["Date", "Product", "Min Price", "Max Price", "Avg Price"])

# Read raw text data from the input file
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    raw_input_data = f.read()

# Extract new data from the raw input and filter only valid products
new_data = extract_data_from_text(raw_input_data)
filtered_data = new_data[new_data["Product"].isin(VALID_PRODUCTS)]

# Append new data to existing data and remove duplicates
if not filtered_data.empty:
    combined_data = pd.concat([existing_data, filtered_data]).drop_duplicates().reset_index(drop=True)
    combined_data.to_csv(DATA_FILE, index=False)
    print(f"Data saved to {DATA_FILE} with {len(combined_data)} records.")
else:
    print("No valid product data found in the input file. Please check the contents.")

# Initialize the Dash app
app = Dash(__name__)

# Get unique products from the combined data
products = combined_data["Product"].unique()

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Product Price Forecasts"),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': product, 'value': product} for product in products],
        value=products[0] if products.size > 0 else None,  # Set default value if products exist
        clearable=False
    ),
    dcc.Graph(id='forecast-graph')
])

# Callback to update the graph based on the selected product
@app.callback(
    Output('forecast-graph', 'figure'),
    Input('product-dropdown', 'value')
)
def update_graph(selected_product):
    df_product = combined_data[combined_data["Product"] == selected_product][["Date", "Avg Price"]]
    df_product = df_product.rename(columns={"Date": "ds", "Avg Price": "y"})
    df_product['ds'] = pd.to_datetime(df_product['ds'], errors='coerce')
    df_product = df_product.dropna(subset=['ds'])
    df_product = df_product.groupby('ds').mean().reset_index()

    if df_product.shape[0] < 2:
        return go.Figure()  # Return an empty figure if not enough data

    max_date = df_product['ds'].max()
    df_product = df_product[df_product['ds'] >= (max_date - pd.Timedelta(days=60))]
    df_product = df_product.set_index('ds').asfreq('D').fillna(method='ffill').reset_index()

    # Train the model with average price
    model = Prophet()
    model.fit(df_product)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Create the forecast graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast Avg', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df_product['ds'], y=df_product['y'], mode='markers', name='Actual Avg', marker=dict(size=10, color='black')))
    
    # Add the confidence intervals
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Confidence Interval', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Confidence Interval', line=dict(color='green', dash='dash')))
    
    fig.update_layout(
        title=f"{selected_product} Price Forecast",
        xaxis_title="Date",
        yaxis_title="Price",
        height=600
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




















# 15t
















