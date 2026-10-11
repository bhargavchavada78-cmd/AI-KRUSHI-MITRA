from datetime import date, datetime
import pandas as pd
import streamlit as st

from database.queries import (
    add_farmer, get_farmers, get_farmer, update_farmer,
    add_farm, get_farms,
    add_crop, get_crops, get_crop, get_full_crop_status,
    get_alerts, add_alert,
)
from deep_learning.health_service import save_health_check
from machine_learning.predict_risk import predict_risk
from weather.weather_service import get_weather
from nlp.farmer_assistant import ask_farmer_assistant


# ---------------------------------------------------------
# Page configuration and common helpers
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Krushi Mitra",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Visual theme: fresh, modern agricultural dashboard
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --akm-green: #176b45;
        --akm-green-dark: #104b33;
        --akm-green-soft: #e8f5ed;
        --akm-lime: #c8e6a0;
        --akm-cream: #f7faf5;
        --akm-ink: #1d3026;
        --akm-muted: #68796f;
        --akm-border: #dce8df;
    }

    .stApp {
        background: linear-gradient(180deg, #f6faf5 0%, #ffffff 42%, #f7faf7 100%);
        color: var(--akm-ink);
    }
    [data-testid="stHeader"] { background: rgba(246, 250, 245, 0.88); }
    [data-testid="stMainBlockContainer"] {
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Main brand banner */
    .akm-hero {
        position: relative;
        overflow: hidden;
        padding: 1.65rem 1.8rem;
        margin: 0 0 1.5rem 0;
        border-radius: 22px;
        color: white;
        background: linear-gradient(120deg, #104b33 0%, #176b45 58%, #438b56 100%);
        box-shadow: 0 12px 30px rgba(23, 107, 69, 0.16);
    }
    .akm-hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -48px;
        top: -105px;
        border: 35px solid rgba(255,255,255,0.09);
        border-radius: 50%;
        pointer-events: none;
    }
    .akm-eyebrow {
        color: #d6f0d8;
        font-size: 0.78rem;
        font-weight: 750;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .akm-brand-title {
        color: #ffffff;
        font-size: clamp(1.8rem, 3vw, 2.55rem);
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -0.035em;
        margin: 0;
    }
    .akm-brand-subtitle {
        color: #e0f1e4;
        margin-top: 0.6rem;
        font-size: 1rem;
        max-width: 720px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #edf6ee 0%, #f8fbf7 100%);
        border-right: 1px solid #dce9de;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #365747;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 11px;
        padding: 0.48rem 0.55rem;
        transition: background 0.18s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #dcefe0;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        font-weight: 600;
    }

    /* Headings and content blocks */
    h1, h2, h3 { color: #173f2c; letter-spacing: -0.025em; }
    h2 { padding-bottom: 0.25rem; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--akm-border) !important;
        border-radius: 16px !important;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dfebe1;
        border-radius: 16px;
        padding: 1rem 1.05rem;
        box-shadow: 0 4px 14px rgba(23, 70, 43, 0.045);
    }
    [data-testid="stMetricLabel"] { color: #5f7466; font-weight: 650; }
    [data-testid="stMetricValue"] { color: #176b45; font-weight: 800; }

    /* Inputs: force readable dark text on white controls (fixes white-on-white text) */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #cbdccf !important;
        background: #ffffff !important;
        color: #1d3026 !important;
        -webkit-text-fill-color: #1d3026 !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stNumberInput"] input::placeholder,
    [data-testid="stDateInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {
        color: #68796f !important;
        -webkit-text-fill-color: #68796f !important;
        opacity: 1 !important;
    }
    /* Force selected dropdown values and their inner spans to stay dark.
       Streamlit/BaseWeb can otherwise inherit white text from the theme. */
    [data-testid="stSelectbox"] [data-baseweb="select"],
    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stMultiSelect"] [data-baseweb="select"],
    [data-testid="stMultiSelect"] [data-baseweb="select"] *,
    [data-testid="stSelectbox"] input,
    [data-testid="stMultiSelect"] input {
        color: #1d3026 !important;
        -webkit-text-fill-color: #1d3026 !important;
        caret-color: #1d3026 !important;
    }
    [data-baseweb="popover"], [data-baseweb="menu"],
    [role="listbox"], [role="option"] {
        background-color: #ffffff !important;
        color: #1d3026 !important;
    }
    [role="option"], [role="option"] *,
    [data-baseweb="menu"] *, [data-baseweb="popover"] * {
        color: #1d3026 !important;
        -webkit-text-fill-color: #1d3026 !important;
    }
    /* Keep dropdown arrows visible on the light control background. */
    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiSelect"] svg { color: #365747 !important; fill: #365747 !important; }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"] {
        color: #304d3b;
    }
    [data-testid="stFileUploader"] section {
        background: #f7fbf7;
        border: 1.5px dashed #9ec5a8;
        border-radius: 14px;
        color: #1d3026 !important;
    }
    [data-testid="stFileUploader"] section * { color: #304d3b !important; }

    /* Sidebar slide-in / slide-out navigation and collapse control */
    [data-testid="stSidebar"] {
        transition: width 0.25s ease, min-width 0.25s ease;
        box-shadow: 5px 0 22px rgba(20, 75, 51, 0.045);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        display: flex;
        align-items: center;
        border: 1px solid transparent;
        margin: 0.16rem 0;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #d8eddd;
        border-color: #b8d9c0;
        color: #104b33 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
        color: #104b33 !important;
        font-weight: 750;
    }
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarHeader"] button {
        color: #176b45 !important;
        border-radius: 9px !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarHeader"] button:hover {
        background: #dcefe0 !important;
    }

    /* Buttons */
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 10px;
        border: 1px solid #176b45;
        background: #176b45;
        color: #ffffff;
        font-weight: 700;
        padding: 0.55rem 1rem;
        transition: transform 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 3px 8px rgba(23, 107, 69, 0.12);
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: #104b33;
        border-color: #104b33;
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 6px 13px rgba(23, 107, 69, 0.18);
    }
    .stButton > button:focus, .stFormSubmitButton > button:focus {
        box-shadow: 0 0 0 3px rgba(23, 107, 69, 0.18);
    }

    /* Tabs and tables */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid #dce8df;
    }
    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 0.65rem 1rem;
        font-weight: 650;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #176b45;
        border-bottom-color: #176b45;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #e0e9e2;
        border-radius: 12px;
        overflow: hidden;
    }
    [data-testid="stAlert"] { border-radius: 12px; }
    hr { border-color: #e2ebe4; }

    /* Mobile spacing */
    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem 2rem; }
        .akm-hero { padding: 1.25rem; border-radius: 16px; }
        .akm-brand-subtitle { font-size: 0.9rem; }
    }
    </style>

    <div class="akm-hero">
        <div class="akm-eyebrow">Smart Agriculture • AI-powered support</div>
        <div class="akm-brand-title">🌱 AI Krushi Mitra</div>
        <div class="akm-brand-subtitle">A farmer-friendly crop advisory dashboard using Machine Learning, Deep Learning, NLP, live weather data and MySQL.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES = [
    "Home",
    "Crop Information",
    "Crop Health Check",
    "Weather & ML Risk",
    "Alerts",
    "AI Assistant",
    "Farmer Profile",
    "Settings",
]
page = st.sidebar.radio("Navigation", PAGES)


def show_error(action, error):
    st.error(f"{action} failed: {error}")


def load_rows(function, label):
    """Load database rows without crashing the entire dashboard."""
    try:
        return function(), None
    except Exception as exc:
        return [], f"{label}: {exc}"


def row_label(row, id_index=0, name_index=1, prefix="ID"):
    try:
        return f"{prefix} {row[id_index]} — {row[name_index]}"
    except (IndexError, TypeError):
        return str(row)


farmers, farmers_error = load_rows(get_farmers, "Could not load farmers")
farms, farms_error = load_rows(get_farms, "Could not load farms")
crops, crops_error = load_rows(get_crops, "Could not load crops")

# Based on the current database queries:
# farmers: (farmer_id, name, mobile, language)
# farms:   (farm_id, farmer_id, location, area, soil_type)
# crops:   (crop_id, farm_id, crop_name, variety, sowing_date, irrigation_type)
farmer_options = list(farmers)
farm_options = list(farms)
crop_options = list(crops)


def crop_label(row):
    """Show the crop name first and keep its database ID easy to identify."""
    if len(row) > 2:
        return f"{row[2]} (Crop ID: {row[0]})"
    return str(row)


def farm_label(row):
    location = row[2] if len(row) > 2 else "Farm"
    return f"Farm ID {row[0]} — {location}"


def farmer_label(row):
    name = row[1] if len(row) > 1 else "Farmer"
    mobile = row[2] if len(row) > 2 else ""
    return f"Farmer ID {row[0]} — {name} ({mobile})"


def render_database_errors():
    for error in (farmers_error, farms_error, crops_error):
        if error:
            st.warning(error)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

if page == "Home":
    st.header("Farmer Dashboard")
    render_database_errors()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registered Farmers", len(farmers))
    col2.metric("Farms", len(farms))
    col3.metric("Registered Crops", len(crops))
    col4.metric("Crop Health", "Ready to check")

    st.subheader("Getting Started")
    st.markdown(
        """
        1. Add farmer and farm details in **Farmer Profile**.
        2. Register a crop in **Crop Information**.
        3. Upload a cotton leaf image in **Crop Health Check**.
        4. Check live weather and the experimental risk model in **Weather & ML Risk**.
        5. Review alerts and ask crop-care questions in **Alerts** and **AI Assistant**.
        """
    )

    if crop_options:
        st.subheader("Registered Crops")
        summary = []
        for crop in crop_options:
            crop_id = crop[0]
            try:
                status = get_full_crop_status(crop_id)
                summary.append({
                    "Crop ID": crop_id,
                    "Crop": status["crop_name"],
                    "Variety": status.get("variety"),
                    "Sowing Date": status.get("sowing_date"),
                    "Age (days)": status.get("crop_age"),
                    "Growth Stage": status.get("stage"),
                })
            except Exception:
                summary.append({
                    "Crop ID": crop_id,
                    "Crop": crop[2] if len(crop) > 2 else "Unknown",
                    "Variety": crop[3] if len(crop) > 3 else "",
                    "Sowing Date": crop[4] if len(crop) > 4 else "",
                    "Age (days)": "Unavailable",
                    "Growth Stage": "Unavailable",
                })
        st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)
    else:
        st.info("No crops are registered yet. Add a farm and crop to get started.")


# ---------------------------------------------------------
# CROP INFORMATION
# ---------------------------------------------------------

elif page == "Crop Information":
    st.header("🌾 Crop Information")
    render_database_errors()

    tab_view, tab_add = st.tabs(["Registered Crops", "Add Crop"])

    with tab_view:
        if not crop_options:
            st.info("No crops found. Add a crop using the second tab.")
        else:
            selected_crop = st.selectbox(
                "Select crop",
                crop_options,
                format_func=crop_label,
                key="crop_info_select",
            )
            try:
                status = get_full_crop_status(int(selected_crop[0]))
                if status:
                    a, b, c = st.columns(3)
                    a.metric("Crop Age", f'{status["crop_age"]} days')
                    b.metric("Growth Stage", status["stage"])
                    c.metric("Crop", status["crop_name"])
                    st.write("**Variety:**", status.get("variety") or "Not specified")
                    st.write("**Sowing date:**", status.get("sowing_date") or "Not specified")
                    st.write("**Irrigation type:**", selected_crop[5] if len(selected_crop) > 5 else "Not specified")
                else:
                    st.warning("Crop was not found in the database.")
            except Exception as exc:
                show_error("Loading crop information", exc)

            records = []
            for crop in crop_options:
                try:
                    status = get_full_crop_status(int(crop[0]))
                    if status:
                        records.append({
                            "Crop ID": status["crop_id"],
                            "Farm ID": crop[1],
                            "Crop": status["crop_name"],
                            "Variety": status.get("variety"),
                            "Sowing Date": status.get("sowing_date"),
                            "Age (days)": status.get("crop_age"),
                            "Stage": status.get("stage"),
                        })
                except Exception:
                    continue
            if records:
                st.subheader("All Crop Records")
                st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)

    with tab_add:
        if not farm_options:
            st.warning("Add a farmer and farm in Farmer Profile before registering a crop.")
        else:
            with st.form("add_crop_form", clear_on_submit=True):
                selected_farm = st.selectbox("Farm", farm_options, format_func=farm_label)
                crop_name = st.text_input("Crop name", placeholder="e.g. Cotton")
                variety = st.text_input("Variety", placeholder="e.g. local variety")
                sowing_date = st.date_input("Sowing date", value=date.today())
                irrigation_type = st.selectbox(
                    "Irrigation type",
                    ["Drip", "Sprinkler", "Flood", "Rain-fed", "Other"],
                )
                submitted = st.form_submit_button("Save Crop")

            if submitted:
                if not crop_name.strip():
                    st.error("Enter a crop name.")
                else:
                    try:
                        add_crop(
                            int(selected_farm[0]),
                            crop_name.strip(),
                            variety.strip(),
                            sowing_date,
                            irrigation_type,
                        )
                        st.success("Crop saved to MySQL. Refresh the page to see it.")
                        st.rerun()
                    except Exception as exc:
                        show_error("Saving crop", exc)


# ---------------------------------------------------------
# CROP HEALTH CHECK
# ---------------------------------------------------------

elif page == "Crop Health Check":
    from PIL import Image

    st.header("🍃 Crop Health Check")
    st.write("Upload a clear cotton leaf photo for an experimental CNN prediction.")
    st.warning(
        "This CNN currently recognizes cotton-leaf classes only. "
        "Its prediction is not a confirmed diagnosis or a pesticide recommendation."
    )

    if not crop_options:
        st.warning("Register a crop first in Crop Information.")
    else:
        selected_crop = st.selectbox(
            "Select the crop record",
            crop_options,
            format_func=crop_label,
            key="health_crop_select",
        )
        uploaded_image = st.file_uploader(
            "Upload cotton leaf image",
            type=["jpg", "jpeg", "png", "webp"],
            key="health_image_upload",
        )

        if uploaded_image is not None:
            try:
                preview = Image.open(uploaded_image).convert("RGB")
                st.image(preview, caption="Uploaded crop leaf", width=350)

                if st.button("🔍 Analyze Crop Health", type="primary"):
                    with st.spinner("Analyzing image and saving results to MySQL..."):
                        uploaded_image.seek(0)
                        result = save_health_check(int(selected_crop[0]), uploaded_image)

                    st.success("Crop image analyzed and saved successfully.")
                    c1, c2 = st.columns(2)
                    c1.metric(
                        "Predicted condition",
                        result["prediction"].replace("_", " ").title(),
                    )
                    c2.metric("Model confidence", f'{result["confidence"]:.2f}%')
                    st.write("**Confidence category:**", result["confidence_level"])
                    st.caption(
                        "Confidence is the model's confidence in its predicted class, "
                        "not disease severity. Confirm suspected disease with a local "
                        "agriculture expert before applying any treatment."
                    )
                    with st.expander("Saved record details"):
                        st.write("Crop ID:", result["crop_id"])
                        st.write("Image ID:", result["image_id"])
                        st.write("Analysis ID:", result["analysis_id"])
                        st.write("Image path:", result["image_path"])
            except Exception as exc:
                show_error("Crop health check", exc)


# ---------------------------------------------------------
# WEATHER AND EXPERIMENTAL ML RISK
# ---------------------------------------------------------

elif page == "Weather & ML Risk":
    st.header("🌦️ Weather and Crop Risk")
    st.write("Live weather comes from Open-Meteo. The risk model is experimental.")

    default_location = ""
    if farm_options:
        default_location = str(farm_options[0][2]) if len(farm_options[0]) > 2 else ""

    location = st.text_input(
        "Farm location (town or village)",
        value=default_location,
        placeholder="e.g. Sami, Gujarat",
    )

    live_weather = None
    if st.button("Get Live Weather", type="primary"):
        if not location.strip():
            st.error("Enter a farm location.")
        else:
            try:
                live_weather = get_weather(location.strip())
                st.session_state["akm_live_weather"] = live_weather
                st.session_state["akm_live_weather_location"] = location.strip()
            except Exception as exc:
                show_error("Getting live weather", exc)

    live_weather = st.session_state.get("akm_live_weather")
    if live_weather:
        st.caption(f"Latest fetched location: {st.session_state.get('akm_live_weather_location', location)}")
        w1, w2, w3, w4 = st.columns(4)
        w1.metric("Temperature", f'{live_weather["temperature"]} °C')
        w2.metric("Humidity", f'{live_weather["humidity"]}%')
        w3.metric("Current rain", f'{live_weather["rainfall"]} mm')
        w4.metric("Rain probability (next 6 hours)", f'{live_weather["rain_probability"]}%')
        st.caption("Weather is fetched live and is not automatically saved to the weather-history table in this version.")

    st.subheader("Experimental Cotton Risk Prediction")
    st.info(
        "The risk model requires eight features. Weather values may be prefilled from "
        "the latest fetched weather; the remaining values are user estimates. "
        "This model is experimental and should not be used alone for treatment decisions."
    )

    weather_for_risk = st.session_state.get("akm_live_weather", {})
    with st.form("risk_form"):
        c1, c2 = st.columns(2)
        with c1:
            avg_temp = st.number_input(
                "Average temperature (°C)",
                value=float(weather_for_risk.get("temperature", 30.0)),
                min_value=-10.0,
                max_value=60.0,
            )
            avg_humidity = st.number_input(
                "Average humidity (%)",
                value=float(weather_for_risk.get("humidity", 60.0)),
                min_value=0.0,
                max_value=100.0,
            )
            rainfall = st.number_input(
                "Rainfall (mm)",
                value=float(weather_for_risk.get("precipitation", weather_for_risk.get("rainfall", 0.0))),
                min_value=0.0,
                max_value=1000.0,
            )
            leaf_wetness = st.number_input(
                "Leaf wetness (hours)",
                value=4.0,
                min_value=0.0,
                max_value=24.0,
            )
        with c2:
            wind_speed = st.number_input(
                "Wind speed (km/h)",
                value=10.0,
                min_value=0.0,
                max_value=200.0,
            )
            soil_moisture = st.number_input(
                "Soil moisture (%)",
                value=40.0,
                min_value=0.0,
                max_value=100.0,
            )
            regional_incidence = st.number_input(
                "Prior regional incidence (%)",
                value=10.0,
                min_value=0.0,
                max_value=100.0,
            )
            selected_risk_crop = st.selectbox(
                "Crop for optional alert",
                crop_options,
                format_func=crop_label,
                index=0 if crop_options else None,
            ) if crop_options else None
        run_risk = st.form_submit_button("Predict Cotton Risk")

    if run_risk:
        risk_input = {
            "day_of_year": datetime.now().timetuple().tm_yday,
            "avg_temp_c": avg_temp,
            "avg_humidity_pct": avg_humidity,
            "rainfall_mm": rainfall,
            "leaf_wetness_hours": leaf_wetness,
            "wind_speed_kmph": wind_speed,
            "soil_moisture_pct": soil_moisture,
            "prior_regional_incidence_pct": regional_incidence,
        }
        try:
            st.session_state["akm_last_risk"] = predict_risk(risk_input)
            st.session_state["akm_last_risk_crop_id"] = (
                int(selected_risk_crop[0]) if selected_risk_crop is not None else None
            )
        except Exception as exc:
            st.session_state.pop("akm_last_risk", None)
            show_error("Risk prediction", exc)

    risk_result = st.session_state.get("akm_last_risk")
    if risk_result:
        r1, r2 = st.columns(2)
        r1.metric("Predicted risk", risk_result["predicted_risk"])
        r2.metric("Model confidence", f'{risk_result["model_confidence_percent"]:.2f}%')
        st.caption("Experimental model output; confidence is not a guarantee of risk.")

        risk_crop_id = st.session_state.get("akm_last_risk_crop_id")
        if risk_crop_id is not None:
            if st.button("Save this risk as a crop alert"):
                message = (
                    f'Experimental cotton risk model predicted '
                    f'{risk_result["predicted_risk"]} risk '
                    f'({risk_result["model_confidence_percent"]:.2f}% model confidence). '
                    "Verify local conditions before taking action."
                )
                try:
                    add_alert(
                        int(risk_crop_id),
                        "ML Risk",
                        message,
                        str(risk_result["predicted_risk"]),
                        "Open",
                    )
                    st.success("Risk alert saved.")
                except Exception as exc:
                    show_error("Saving risk alert", exc)


# ---------------------------------------------------------
# ALERTS
# ---------------------------------------------------------

elif page == "Alerts":
    st.header("🔔 Crop Alerts")
    if not crop_options:
        st.info("Register a crop before viewing or creating crop alerts.")
    else:
        selected_crop = st.selectbox(
            "Select crop",
            crop_options,
            format_func=crop_label,
            key="alerts_crop_select",
        )

        try:
            alerts = get_alerts(int(selected_crop[0]))
            if alerts:
                alert_df = pd.DataFrame(
                    alerts,
                    columns=[
                        "Alert ID", "Crop ID", "Alert Type",
                        "Message", "Severity", "Status", "Created At",
                    ][:len(alerts[0])],
                )
                st.dataframe(alert_df, use_container_width=True, hide_index=True)
            else:
                st.info("No alerts for this crop yet.")
        except Exception as exc:
            show_error("Loading alerts", exc)

        with st.expander("Create a manual alert"):
            with st.form("manual_alert_form", clear_on_submit=True):
                alert_type = st.selectbox(
                    "Alert type",
                    ["Weather", "Crop Health", "Watering", "Harvesting", "General"],
                )
                message = st.text_area("Alert message")
                severity = st.selectbox("Severity", ["Low", "Medium", "High"])
                status = st.selectbox("Status", ["Open", "Resolved"])
                save_alert = st.form_submit_button("Save Alert")
            if save_alert:
                if not message.strip():
                    st.error("Enter an alert message.")
                else:
                    try:
                        add_alert(
                            int(selected_crop[0]),
                            alert_type,
                            message.strip(),
                            severity,
                            status,
                        )
                        st.success("Alert saved to MySQL.")
                        st.rerun()
                    except Exception as exc:
                        show_error("Saving alert", exc)


# ---------------------------------------------------------
# RULE-BASED NLP FARMER ASSISTANT
# ---------------------------------------------------------

elif page == "AI Assistant":
    st.header("🤖 Farmer Assistant")
    st.caption("Rule-based NLP assistant — no LLM is used in this version.")

    selected_crop = None
    selected_farm = None
    if crop_options:
        selected_crop = st.selectbox(
            "Crop context",
            [None] + crop_options,
            format_func=lambda row: "No crop selected" if row is None else crop_label(row),
            key="assistant_crop_select",
        )
    if farm_options:
        selected_farm = st.selectbox(
            "Farm context",
            [None] + farm_options,
            format_func=lambda row: "No farm selected" if row is None else farm_label(row),
            key="assistant_farm_select",
        )

    st.write("Try asking about crop growth, weather, watering, leaf problems, or harvesting.")
    question = st.text_input(
        "Your question",
        placeholder="e.g. How old is my crop? Should I water today?",
    )

    if st.button("Ask Assistant", type="primary"):
        if not question.strip():
            st.warning("Type a question first.")
        else:
            try:
                answer = ask_farmer_assistant(
                    question,
                    crop_id=int(selected_crop[0]) if selected_crop else None,
                    farm_id=int(selected_farm[0]) if selected_farm else None,
                )
                st.markdown("**Assistant:**")
                st.write(answer)
            except Exception as exc:
                show_error("Farmer assistant", exc)

    with st.expander("Important note"):
        st.write(
            "The assistant uses keyword-based intent detection and existing database "
            "records. It does not use an LLM and may not understand every phrasing. "
            "For disease or pesticide decisions, consult a local agriculture expert."
        )


# ---------------------------------------------------------
# FARMER PROFILE AND FARM MANAGEMENT
# ---------------------------------------------------------

elif page == "Farmer Profile":
    st.header("👨‍🌾 Farmer Profile and Farm Management")
    render_database_errors()

    tab_farmers, tab_add_farmer, tab_farms, tab_add_farm = st.tabs(
        ["Farmers", "Register Farmer", "Farms", "Register Farm"]
    )

    with tab_farmers:
        if farmer_options:
            farmer_table = []
            for row in farmer_options:
                farmer_table.append({
                    "Farmer ID": row[0],
                    "Name": row[1] if len(row) > 1 else "",
                    "Mobile": row[2] if len(row) > 2 else "",
                    "Language": row[3] if len(row) > 3 else "",
                })
            st.dataframe(pd.DataFrame(farmer_table), use_container_width=True, hide_index=True)

            chosen_farmer = st.selectbox(
                "Select farmer to update",
                farmer_options,
                format_func=farmer_label,
                key="update_farmer_select",
            )
            with st.form("update_farmer_form"):
                new_name = st.text_input("Name", value=str(chosen_farmer[1] or ""))
                new_mobile = st.text_input("Mobile", value=str(chosen_farmer[2] or ""))
                new_language = st.selectbox(
                    "Language",
                    ["Gujarati", "Hindi", "English"],
                    index=["Gujarati", "Hindi", "English"].index(chosen_farmer[3])
                    if len(chosen_farmer) > 3 and chosen_farmer[3] in ["Gujarati", "Hindi", "English"]
                    else 0,
                )
                update_button = st.form_submit_button("Update Farmer")
            if update_button:
                try:
                    update_farmer(int(chosen_farmer[0]), new_name.strip(), new_mobile.strip(), new_language)
                    st.success("Farmer profile updated.")
                    st.rerun()
                except Exception as exc:
                    show_error("Updating farmer", exc)
        else:
            st.info("No farmers registered yet.")

    with tab_add_farmer:
        with st.form("add_farmer_form", clear_on_submit=True):
            name = st.text_input("Full name")
            mobile = st.text_input("Mobile number")
            language = st.selectbox("Preferred language", ["Gujarati", "Hindi", "English"])
            submit_farmer = st.form_submit_button("Register Farmer")
        if submit_farmer:
            if not name.strip() or not mobile.strip():
                st.error("Name and mobile number are required.")
            else:
                try:
                    add_farmer(name.strip(), mobile.strip(), language)
                    st.success("Farmer registered in MySQL.")
                    st.rerun()
                except Exception as exc:
                    show_error("Registering farmer", exc)

    with tab_farms:
        if farm_options:
            farm_table = []
            for row in farm_options:
                farm_table.append({
                    "Farm ID": row[0],
                    "Farmer ID": row[1] if len(row) > 1 else "",
                    "Location": row[2] if len(row) > 2 else "",
                    "Area": row[3] if len(row) > 3 else "",
                    "Soil Type": row[4] if len(row) > 4 else "",
                })
            st.dataframe(pd.DataFrame(farm_table), use_container_width=True, hide_index=True)
        else:
            st.info("No farms registered yet.")

    with tab_add_farm:
        if not farmer_options:
            st.warning("Register a farmer first.")
        else:
            with st.form("add_farm_form", clear_on_submit=True):
                owner = st.selectbox(
                    "Farmer",
                    farmer_options,
                    format_func=farmer_label,
                    key="new_farm_owner",
                )
                farm_location = st.text_input("Village / town / location")
                area = st.number_input("Farm area (acres)", min_value=0.0, value=1.0, step=0.5)
                soil_type = st.selectbox(
                    "Soil type",
                    ["Black soil", "Goradu soil", "Sandy", "Loamy", "Other"],
                )
                submit_farm = st.form_submit_button("Register Farm")
            if submit_farm:
                if not farm_location.strip():
                    st.error("Enter the farm location.")
                else:
                    try:
                        add_farm(
                            int(owner[0]),
                            farm_location.strip(),
                            area,
                            soil_type,
                        )
                        st.success("Farm registered in MySQL.")
                        st.rerun()
                    except Exception as exc:
                        show_error("Registering farm", exc)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

elif page == "Settings":
    st.header("⚙️ Settings")
    st.write("Choose your preferred display language.")
    language = st.selectbox(
        "Language",
        ["Gujarati", "Hindi", "English"],
        index=["Gujarati", "Hindi", "English"].index(
            st.session_state.get("akm_language", "English")
        ),
    )
    st.session_state["akm_language"] = language
    st.success(f"Display preference set to {language} for this session.")
    st.info(
        "This setting currently applies only during the active Streamlit session. "
        "It does not yet translate every page or save the preference to the farmer record."
    )
    st.subheader("Project Modules")
    st.markdown(
        """
        - **Deep Learning:** cotton leaf image classification.
        - **Machine Learning:** experimental cotton risk prediction.
        - **NLP:** keyword-based farmer assistant without an LLM.
        - **SQL / MySQL:** farmer, farm, crop, health-analysis, and alert records.
        - **Weather:** live forecast data from Open-Meteo.
        - **Streamlit:** dashboard interface.
        """
    )

st.sidebar.divider()
st.sidebar.caption("AI Krushi Mitra • Prototype")
