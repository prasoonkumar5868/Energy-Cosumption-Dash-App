## World Energy Consumption Dashboard

This is an interactive dashboard built with **Plotly Dash** to visualize global energy consumption trends over time. Users can select different countries and energy types, and view data both as a line chart and on a world map.

## Features

- **Country Selector:** Choose one or more countries to compare.
- **Energy Type Selector:** Choose from coal, oil, gas, renewables, or nuclear.
- **Line Chart:** View energy consumption over time (from 1960 onward).
- **Choropleth Map:** Shows total consumption for the selected energy type across countries from 2000–2024.
- **Download CSV:** Export filtered country and energy data.

Tech Stack

- **Dash** (Plotly)
- **Plotly Express**
- **Pandas**
- **HTML/CSS**


## Folder Structure

.
├── app.py # Main Dash application
├── data/
│ └── owid-energy-data.csv # Energy dataset (Our World in Data)
├── assets/
│ └── custom.css # Optional CSS styling
└── README.md



## Dataset

Source: [Our World in Data - Energy Dataset](https://github.com/owid/energy-data)

Key columns used:
- `year`
- `country`
- `iso_code`
- `coal_consumption`, `oil_consumption`, `gas_consumption`, `renewables_consumption`, `nuclear_consumption`

## How to Run

1. **Clone this repo**:
   ```bash
   git clone https://github.com/your-username/energy-dashboard.git
   cd energy-dashboard
2. **Install dependencies**:
pip install -r requirements.txt
3. **Run the app**:
python app.py
Visit the location as given in your terminal.
