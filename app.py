# -*- coding: utf-8 -*-
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests
import os

# -------------------------------
# داده نمونه (می‌توانی API یا CSV واقعی جایگزین کنی)
# -------------------------------
data = pd.DataFrame({
    "تاریخ": pd.date_range(start="2026-01-01", periods=7, freq="D"),
    "CO": [0.4, 0.5, 0.3, 0.6, 0.4, 0.5, 0.3],
    "NO2": [12, 15, 10, 18, 14, 13, 11],
    "PM2.5": [25, 30, 22, 28, 27, 24, 26],
    "PM10": [40, 45, 38, 42, 41, 39, 40],
    "SO2": [5, 6, 4, 5, 5, 6, 4]
})

parameters = ["CO", "NO2", "PM2.5", "PM10", "SO2"]

# -------------------------------
# برنامه Dash
# -------------------------------
app = Dash(__name__)
app.title = "داشبورد آلودگی هوای اردکان"

app.layout = html.Div(style={"font-family":"Tahoma, sans-serif", "textAlign":"center", "margin":"20px"}, children=[
    
    html.H1("داشبورد آلودگی هوای اردکان", style={"color":"darkblue"}),
    
    # انتخاب پارامتر
    html.Label("انتخاب پارامتر:", style={"font-weight":"bold", "font-size":"18px"}),
    dcc.Dropdown(
        id="param-dropdown",
        options=[{"label": p, "value": p} for p in parameters],
        value="PM2.5",
        clearable=False,
        style={"width":"50%", "margin":"auto"}
    ),
    
    html.Br(),
    
    # نمودار
    dcc.Graph(id="param-graph"),
    
    html.Br(),
    
    # تحلیل کوتاه فارسی
    html.Div(id="analysis-box", style={"border":"1px solid #aaa", "padding":"15px", 
                                       "width":"60%", "margin":"auto", "border-radius":"10px",
                                       "background-color":"#f9f9f9", "text-align":"right"}),

    html.Br(),
    
    # منبع / نویسنده
    html.Footer("تهیه شده توسط غزل امیدواری، دانشجوی ارشد رشته مدیریت صنعتی، دانشگاه یزد",
                style={"margin-top":"40px", "font-size":"14px", "color":"gray"})
])

# -------------------------------
# Callback برای بروزرسانی نمودار و تحلیل
# -------------------------------
from dash.dependencies import Input, Output

@app.callback(
    Output("param-graph", "figure"),
    Output("analysis-box", "children"),
    Input("param-dropdown", "value")
)
def update_graph(param):
    fig = px.line(data, x="تاریخ", y=param, markers=True, 
                  title=f"مقدار {param} در طول زمان",
                  labels={"تاریخ":"تاریخ", param:param},
                  template="plotly_dark")
    fig.update_traces(line=dict(color="orange", width=3))
    
    # تحلیل کوتاه فارسی
    analysis = {
        "CO": "مقدار CO نسبتا پایین است، کیفیت هوا خوب است.",
        "NO2": "NO2 در سطح متوسط، توجه به سلامت تنفسی توصیه می‌شود.",
        "PM2.5": "PM2.5 کمی بالا است، برای بیماران تنفسی مراقب باشید.",
        "PM10": "PM10 نوسان متوسط دارد، کیفیت هوا قابل قبول است.",
        "SO2": "SO2 در سطح پایین و ایمن قرار دارد."
    }
    
    return fig, analysis.get(param, "")

# -------------------------------
# اجرای برنامه
# -------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
