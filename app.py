from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_excel("data_mmda_traffic_spatial.csv.xlsx", sheet_name="data_mmda_traffic_spatial")

    # ---------------- DOUGHNUT CHART ---------------- #
    df_doughnut = df.dropna(subset=['Involved'])
    df_expanded = df_doughnut.assign(Vehicle=df_doughnut['Involved'].str.upper().str.split(" AND |,| / | & ")).explode('Vehicle')
    df_expanded['Vehicle'] = df_expanded['Vehicle'].str.strip()
    vehicle_counts = df_expanded['Vehicle'].value_counts().reset_index()
    vehicle_counts.columns = ['Vehicle', 'Count']
    vehicle_counts = vehicle_counts.head(10)
    fig_doughnut = px.pie(
        vehicle_counts,
        values='Count',
        names='Vehicle',
        hole=0.4,
        title='Vehicle Type Distribution in Traffic Accidents',
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_doughnut.update_traces(textposition='inside', textinfo='percent+label')
    fig_doughnut.update_layout(showlegend=True, title_font_size=20, plot_bgcolor='black', paper_bgcolor='black', font=dict(family="Poppins, sans-serif"), margin=dict(t=40, b=40))
    chart_doughnut = fig_doughnut.to_html(full_html=False)

    # ---------------- MAP CHART ---------------- #
    df_map = df.copy()
    df_map['City'] = df_map['City'].replace({"ParaÃƒÂ±aque": "Paranaque"})
    df_map = df_map.dropna(subset=['Latitude', 'Longitude'])
    fig_map = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="City",
        hover_name="Location",
        hover_data={"Date": True, "Time": True, "Type": True, "City": True},
        zoom=5.5,
        height=700,
        title="Traffic Incident Locations",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_map.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor='black',
        plot_bgcolor='black',
        font_color='white',
        title_font_size=20,
        font=dict(family="Poppins, sans-serif"),
        margin={"r": 0, "t": 40, "l": 0, "b": 40}
    )
    chart_map = fig_map.to_html(full_html=False)

    # ---------------- BAR CHART: Vehicle Involvement by Year ---------------- #
    df = df.dropna(subset=['Involved'])
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')
    df = df.dropna(subset=['Datetime'])
    df['Year'] = df['Datetime'].dt.year
    df_exp = df.assign(Vehicle=df['Involved'].str.upper().str.split(" AND |,| / | & ")).explode('Vehicle')
    df_exp['Vehicle'] = df_exp['Vehicle'].str.strip()
    grouped = df_exp.groupby(['Year', 'Vehicle']).size().reset_index(name='Accident Count')
    top_vehicles = grouped.groupby('Vehicle')['Accident Count'].sum().nlargest(10).index
    filtered = grouped[grouped['Vehicle'].isin(top_vehicles)]
    fig_bar = px.bar(
        filtered,
        x='Year',
        y='Accident Count',
        color='Vehicle',
        barmode='group',
        title='Vehicle Involvement by Year (Top 10 Vehicle Types)',
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_bar.update_layout(
        xaxis=dict(dtick=1),
        title_font_size=20,
        legend_title_text='Vehicle Type',
        plot_bgcolor='black',
        paper_bgcolor='black',
        hovermode='x unified',
        font=dict(family="Poppins, sans-serif"),
        margin=dict(t=40, b=40)
    )
    chart_bar = fig_bar.to_html(full_html=False)

    # ---------------- LINE CHART: Accidents by Hour in Top Cities ---------------- #
    df['Hour'] = df['Datetime'].dt.hour
    top_cities = df['City'].value_counts().head(10).index.tolist()
    df_top = df[df['City'].isin(top_cities)]
    grouped = df_top.groupby(['City', 'Hour']).size().reset_index(name='Accident Count')
    fig_line = px.line(
        grouped,
        x="Hour",
        y="Accident Count",
        color="City",
        markers=True,
        title="Accidents by Hour in Top 10 Cities",
        labels={"Hour": "Hour of Day", "Accident Count": "Number of Accidents"},
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_line.update_layout(
        hovermode="x unified",
        xaxis=dict(dtick=1),
        title_font_size=20,
        legend_title_text='City',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family="Poppins, sans-serif"),
        margin=dict(t=40, b=40)
    )
    chart_line = fig_line.to_html(full_html=False)

    # ---------------- BAR CHART: Top 10 Cities with Most Traffic Incidents ---------------- #
    city_counts = df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Incident_Count']
    top_cities = city_counts.head(10).sort_values(by='Incident_Count', ascending=True)
    fig_city_bar = px.bar(
        top_cities,
        x='Incident_Count',
        y='City',
        orientation='h',
        text='Incident_Count',
        title='Top 10 Cities with Most Traffic Incidents',
        template='plotly_dark',
        color='City',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        hover_data={"Incident_Count": True, "City": True}
    )
    fig_city_bar.update_traces(textposition='outside', hovertemplate='City: %{y}<br>Incidents: %{x}')
    fig_city_bar.update_layout(
        xaxis_title='Number of Incidents',
        yaxis_title='City',
        margin={"r":20,"t":50,"l":100,"b":40},
        height=600,
        font=dict(family="Poppins, sans-serif")
    )
    chart_city_bar = fig_city_bar.to_html(full_html=False)

    # ---------------- LINE CHART: Monthly Trend of Traffic Incidents ---------------- #
    df['Month'] = df['Datetime'].dt.to_period('M').astype(str)
    monthly_trend = df.groupby('Month').size().reset_index(name='Incident Count')
    monthly_trend['Month'] = pd.to_datetime(monthly_trend['Month'])
    monthly_trend = monthly_trend.sort_values('Month')
    fig_monthly = px.line(
        monthly_trend,
        x='Month',
        y='Incident Count',
        title='Monthly Trend of Traffic Incidents',
        template='plotly_dark',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_monthly.update_layout(
        title_font_size=20,
        xaxis_title='Month',
        yaxis_title='Number of Incidents',
        plot_bgcolor='black',
        paper_bgcolor='black',
        hovermode='x unified',
        font=dict(family="Poppins, sans-serif"),
        margin=dict(t=40, b=40)
    )
    chart_monthly = fig_monthly.to_html(full_html=False)

    # ---------------- PREDICTIVE CHART ---------------- #
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    df_predict = df.dropna(subset=['Date', 'Time', 'Type', 'City', 'Lanes_Blocked'])
    df_predict['Time'] = df_predict['Time'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0]
    df_predict['Datetime'] = pd.to_datetime(df_predict['Date'].astype(str) + ' ' + df_predict['Time'], errors='coerce')
    df_predict = df_predict.dropna(subset=['Datetime'])
    df_predict['Hour'] = df_predict['Datetime'].dt.hour
    df_predict['DayOfWeek'] = df_predict['Datetime'].dt.dayofweek
    df_predict['CityEncoded'] = LabelEncoder().fit_transform(df_predict['City'])
    df_predict['TypeEncoded'] = LabelEncoder().fit_transform(df_predict['Type'])
    df_predict['Blockage'] = (df_predict['Lanes_Blocked'] >= 2).astype(int)

    X = df_predict[['Hour', 'DayOfWeek', 'CityEncoded', 'TypeEncoded']]
    y = df_predict['Blockage']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    df_predict['Predicted_Blockage'] = model.predict_proba(X)[:, 1]
    hourly_risk = df_predict.groupby('Hour')['Predicted_Blockage'].mean().reset_index()
    hourly_risk.columns = ['Hour', 'Average Predicted Risk']

    fig_predict = px.bar(
        hourly_risk,
        x='Hour',
        y='Average Predicted Risk',
        title='Predicted Risk of Major Traffic Blockage by Hour',
        template='plotly_dark',
        height=600,
        color='Average Predicted Risk',
        color_continuous_scale='Plasma'
    )
    fig_predict.update_layout(
        xaxis=dict(dtick=1, title='Hour of Day (0–23)'),
        yaxis_title='Predicted Risk Level',
        title_font_size=20,
        plot_bgcolor='black',
        paper_bgcolor='black',
        hovermode='x unified',
        font=dict(family="Poppins, sans-serif"),
        margin=dict(t=40, b=40)
    )
    chart_predict = fig_predict.to_html(full_html=False)

    # ---------------- RENDER ---------------- #
    return render_template(
        "dashboard.html",
        chart_map=chart_map,
        chart_doughnut=chart_doughnut,
        chart_bar=chart_bar,
        chart_line=chart_line,
        chart_city_bar=chart_city_bar,
        chart_monthly=chart_monthly,
        chart_predict=chart_predict
    )

if __name__ == '__main__':
    app.run(debug=True)