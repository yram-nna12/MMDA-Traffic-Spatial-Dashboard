# MMDA Traffic Spatial Dashboard

The **MMDA Traffic Spatial Dashboard** is a simple yet effective web-based application built to visualize and interpret traffic conditions across Metro Manila. This project leverages spatial data and traffic information to help users better understand congestion patterns using a clean, user-friendly interface.

Designed for both commuters and planners, the dashboard uses traffic data stored in Excel sheets and presents them visually through an interactive layout powered by HTML, CSS, and Python.

---

## Features

- Interactive map view of Metro Manila
- Visual traffic indicators (e.g., low, moderate, heavy)
- Excel-based traffic data integration
- Responsive design for desktop and mobile
- Basic filtering for zones and traffic severity *(optional depending on implementation)*

---

## Sample Data Format

|      Location      | Traffic Level |    Timestamp       |
|--------------------|---------------|--------------------|
| **EDSA - Cubao**   |	   Heavy	   | 2025-07-20 08:00 AM|
| **C5 - BGC Exit**  |	  Moderate   | 2025-07-20 08:00 AM|
| **Roxas Boulevard**|	   Light	   | 2025-07-20 08:00 AM|

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Backend logic and data processing |
| **HTML**   | Structure and layout of the dashboard |
| **CSS**    | Styling and responsiveness |
| **Excel (.xlsx)** | Source of traffic data (static or simulated) |

---

## How to Run the Project

### 1.Clone the repository:

git clone https://github.com/your-username/mmda-traffic-spatial-dashboard.git
cd mmda-traffic-spatial-dashboard

### 2.Install dependencies:

pip install flask pandas openpyxl

### 3.Run the backend (if used):

python app.py and open your browser and go to: http://localhost:5000 (example only)

---

## Requirements & Installation

### Required Python Packages

Make sure you have Python 3.8+ installed. Then install the following packages:

```bash
pip install flask pandas openpyxl
pip install flask pandas openpyxl plotly scikit-learn
