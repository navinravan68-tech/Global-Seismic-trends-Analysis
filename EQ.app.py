import streamlit as st

import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine




# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Global Earthquake Dashboard",
    page_icon="🌍",
    layout="wide"
)




# DATABASE CONNECTION
# ---------------------------
engine = create_engine(
    "postgresql://postgres:Navin1430@localhost:5432/earthquake_db"
)

st.sidebar.title("🌍 Global Seismic Trends")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "📊 SQL Analysis",
        "💡 Key Insights",
        "ℹ️ About the Project"
    ]
)

if page == "🏠 Overview":

        st.title("🌍 Global Seismic Trends Dashboard")
        st.markdown("### Earthquake Analysis (2021–2026) using dataset from USGS - United States Geological Survey")
        st.info("More than ***99% of*** earthquake records were expert-reviewed " \
                "✅ High data quality ✅ Reliable for analysis ✅ Expert validation ✅ Suitable for decision-making")
        st.divider()
        total_eq = pd.read_sql(
            "SELECT COUNT(*) AS total FROM earthquake_data;",
            engine
        ).iloc[0,0]

        avg_mag = pd.read_sql(
            "SELECT ROUND(AVG(mag)::numeric,2) AS avg_mag FROM earthquake_data;",
            engine
        ).iloc[0,0]

        max_mag = pd.read_sql(
            "SELECT MAX(mag) AS max_mag FROM earthquake_data;",
            engine
        ).iloc[0,0]

        tsunami_count = pd.read_sql(
            "SELECT COUNT(*) FROM earthquake_data WHERE tsunami=1;",
            engine
        ).iloc[0,0]

        
        # KPI CARDS
        

        col1,col2,col3,col4 = st.columns(4)

        col1.metric(
            "🌍 Total Earthquakes",
            f"{total_eq:,}"
        )

        col2.metric(
            "📈 Average Magnitude",
            avg_mag
        )

        col3.metric(
            "⚡ Maximum Magnitude",
            max_mag
        )

        col4.metric(
            "🌊 Tsunami Events",
            tsunami_count
        )

        st.divider()

        # YEARLY TREND

        year_df = pd.read_sql("""

        SELECT year,
        COUNT(*) AS earthquake_count
        FROM earthquake_data
        GROUP BY year
        ORDER BY year;

        """,engine)

        fig1 = px.line(
            year_df,
            x="year",
            y="earthquake_count",
            markers=True,
            title="Earthquakes by Year"
        )

        fig1.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Earthquakes"
        )

        # ---------------------------
        # MAGNITUDE DISTRIBUTION
        # ---------------------------

        mag_df = pd.read_sql("""

        SELECT mag
        FROM earthquake_data;

        """,engine)

        fig2 = px.histogram(
            mag_df,
            x="mag",
            nbins=30,
            title="Magnitude Distribution"
        )

        fig2.update_layout(
            xaxis_title="Magnitude",
            yaxis_title="Frequency"
        )

        # ---------------------------
        # DISPLAY CHARTS
        # ---------------------------

        left,right = st.columns(2)

        with left:
            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                fig2,
                use_container_width=True
            )

elif page == "📊 SQL Analysis":

    from db import run_query
    from queries import queries

    st.title("📊 SQL Analysis")

    selected = st.selectbox(
        "Choose SQL Query",
        list(queries.keys()),
        format_func=lambda x: f"Q{x}. {queries[x]['title']}"
    )

    st.subheader(queries[selected]["title"])

    with st.expander("📜 View SQL Query"):
        st.code(queries[selected]["sql"], language="sql")

    if st.button("▶ Run Query"):
        df = run_query(queries[selected]["sql"])
        st.dataframe(df, use_container_width=True)

elif page=="💡 Key Insights":
      st.title("💡 Key Insights")
      st.markdown("### Executive Summary")
      st.info(
        """
        This page summarizes the key findings derived from the SQL analysis
        performed on the Global Earthquake Dataset.
        """
    )
      
      st.divider()

      st.header("🌋 Magnitude & Depth")

      st.subheader("Top 10 strongest earthquakes.")
      st.success("👉The strongest earthquakes were concentrated in ***Russia, Alaska, New Zealand, the South Sandwich Islands, the Philippines, Pazarcik (Turkiye), Myanmar, and the southeast of the Loyalty Islands.*** " \
                 "These locations are located along or close to the Pacific Ring of Fire, one of the world's most seismically active regions, making them highly prone to major earthquakes")
      st.subheader("Top 10 Deepest earthquakes.")
      st.success("👉The deepest recorded earthquakes occurred mainly in the ***Vanuatu*** and ***Fiji regions***, with ***depths exceeding 680 km.*** " \
                 "These regions lie within active subduction zones, where descending tectonic plates generate deep-focus seismic activity.")
      st.subheader("Average Depth per Country.")
      st.success("👉The analysis covered ***230 countries and regions***. ***North Korea, Fiji, and Brazil*** recorded the ***highest average earthquake depths***, indicating that seismic events in these areas tend to originate much deeper beneath the Earth's surface. " \
                  "Interestingly, these locations do not correspond to the regions with the highest earthquake magnitudes, " \
                  "demonstrating that greater focal depth does not necessarily result in stronger earthquakes. This highlights that earthquake magnitude depends on the amount of energy released along faults rather than depth alone.")

      st.subheader("Average Magnitude per Mangitude Type.")
      st.success("👉 The analysis shows that Destructive earthquakes have the ***highest average magnitude (7.33)***, followed by ***Strong earthquakes (5.31)*** and ***Moderate earthquakes (4.15)***. " \
                "This trend confirms that earthquakes classified as more destructive are associated with significantly greater energy release. " \
                "As magnitude increases, the potential for structural damage, ground shaking, and secondary hazards such as landslides and tsunamis also increases.")
      
      st.divider()
      st.header("📅 Time Analysis")

      st.subheader("Year with most Earthquake.")
      st.success("👉***2024*** recorded the highest number of earthquakes ***(18,659)***, making it the most seismically active year in the dataset.")

      st.subheader("Month with highest number Earthquake.")
      st.success("👉***March*** recorded the highest number of earthquakes, with ***10,906*** events, making it the most seismically active month in the dataset.")

      st.subheader("Day of the week with most Earthquake.")
      st.success("👉***Tuesday*** had the highest number of recorded earthquakes ***(16,477)***, making it the most active day in the dataset.")

      st.subheader("Count of earthquakes per hour of day.")
      st.success("👉***The relatively uniform hourly distribution suggests that earthquakes occur independently of the time of day, " \
                "reinforcing that seismic activity is controlled by geological processes rather than daily human or environmental cycles***.")

      st.subheader("Most active reporting network.")
      st.success("👉The high number of events reported by the ***USGS*** does not imply that most earthquakes occur in the United States. " \
                "Instead, it reflects the organization's ***extensive global seismic monitoring network*** and its role as one of the world's leading providers of earthquake data")
      
      st.divider()
      st.header("💰 Casualties & Economic Loss")

      st.subheader("Top 5 places with highest casualties.")
      st.text("Since there is no columns such as casulaities mag and sig is taken for analysis")
      st.success("The ***2025 Kamchatka Peninsula, Russia Earthquake (M8.8) was the strongest event*** in the dataset, while ***the Pazarcik, Türkiye Earthquake Sequence recorded the highest significance score (2,910)***. " \
                "This highlights that ***earthquake significance is influenced by more than magnitude,*** including factors such as affected population and overall impact.")

      st.subheader("Average economic loss per alert level.")
      st.success("***Red Alert*** earthquakes were the most severe, with the highest average magnitude ***(6.74)*** and significance ***(2,303)***, although they accounted for only ***26 events***. \
                 Conversely, most earthquakes ***(109,554)*** had ***no alert level***, indicating that high-impact earthquakes are relatively rare.")

      st.divider()
      st.header("📊 Event Type & Quality Matrix.")

      st.subheader("Count of reviewed and automatic Earthquake")
      st.success("***Reviewed earthquake*** records account for ***114,059*** events, while only ***172*** events remain ***automatically generated***. " \
                "This demonstrates that the ***dataset*** is predominantly composed of ***expert-verified*** and ***high-quality*** seismic records.")

      st.subheader("Count by Earthquake type.")
      st.success("More than 99% of recorded events are natural earthquakes, with non-earthquake seismic events representing only a negligible proportion of the dataset.")
      st.success("***The dataset contains a small number of non-earthquake events (e.g., mining explosions, quarry blasts, volcanic eruptions, and landslides), " \
                "demonstrating that modern seismic monitoring networks detect both natural and human-induced ground vibrations.***")

      st.divider()
      st.header("🌊 Tsunami & Alert Analysis.")

      st.subheader("Number of Earthquake by data type")
      st.success("Basic seismic metadata (Origin and Phase Data) is available for nearly every earthquake, whereas advanced products such as ***ShakeMap and LossPAGER*** are generated mainly for significant events.")

      st.subheader("Average RMS and gap per country.")
      st.success("***Nevada, Indonesia, and Texas*** recorded the ***lowest average RMS values***, indicating ***high-quality earthquake location estimates***. " \
                    "Regions with lower RMS and smaller azimuthal gaps generally benefit from better seismic station coverage and more reliable earthquake locations.")

      st.subheader("Events with High Station Coverage.")
      st.success("***Japan, Russia, and Alaska*** recorded the highest seismic station coverage, with ***619, 566, and 516*** reporting stations, respectively. Greater station coverage enhances the accuracy and reliability of earthquake detection and analysis.")

      st.subheader("Count of Earthquake by alert level.")
      st.success("Most earthquakes ***(108,683 events)*** had ***no assigned alert level***, while ***Green Alerts (4,494)*** were the most frequent among classified events. ***Red (26) and Orange (25)*** alerts were exceptionally ***rare***, indicating that high-impact earthquakes occur infrequently.")

      st.divider()
      st.header("📈 Seismic Pattern & Trends")

      st.subheader("Top 5 Countries with the Highest Average Earthquake Magnitude (Past 5 Years).")
      st.success("***New Zealand (M8.1)*** and ***Russia (M8.1)*** recorded the ***highest average earthquake magnitudes***, followed by ***Myanmar (M7.7)***, the ***Kahramanmaraş earthquake sequence (M7.65)***, and ***Alaska (M7.57)***. These regions are located along highly active tectonic plate boundaries.")

      st.subheader("Countries that experienced both shallow and deep earthquakes within the same month.")
      st.success("***Alaska, Indonesia, Japan, Russia, Chile, and the Philippines*** experienced both ***shallow*** and ***deep*** earthquakes across multiple months, highlighting the complex tectonic activity associated with active subduction zones.")

      st.subheader("Year-over-Year Growth Rate in Global Earthquake Count.")
      st.success("Earthquake activity showed noticeable year-to-year fluctuations, with the largest increase occurring in ***2025 (+22.29%)***. The sharp decline in ***2026 (-57.10%)*** is likely due to ***incomplete yearly data*** rather than an actual reduction in global seismic activity")

      st.subheader("Top 3 Most Seismically Active Regions (Frequency × Average Magnitude).")
      st.success("The ***South Sandwich Islands*** region recorded the ***highest overall seismic activity***, followed by the ***Kermadec Islands region*** and the ***South of the Fiji Islands***. Their high activity scores result from a combination of ***frequent earthquakes*** and ***moderate-to-high average magnitudes***.")

      st.divider()
      st.header("🌍 Depth, Location & Distance Analysis")

      st.subheader("Average Depth of Earthquakes Within ±5° Latitude of the Equator.")
      st.success("***The Philippines recorded the deepest average earthquakes (116.85 km)*** near the equator, followed by ***Papua New Guinea, Peru, Ecuador, and Indonesia***. These regions are located along ***active subduction zones***, where earthquakes commonly occur at greater depths.")

      st.subheader("Countries Having the Highest Ratio of Shallow to Deep Earthquakes.")
      st.success("***Hawaii*** recorded the highest shallow-to-deep earthquake ratio ***(932:1)***, followed by ***Iran*** and ***Canada***, indicating that earthquakes in these regions are overwhelmingly shallow. Regions such as ***Russia*** and ***Puerto Rico*** " \
                "showed lower ratios due to frequent deep-focus earthquakes associated with subduction zones.")

      st.subheader("The average magnitude difference between earthquakes with tsunami alerts and those without.")
      st.success("***No tsunami-triggered earthquake records are available in the dataset (2021–2026). Therefore, the average magnitude difference between tsunami and non-tsunami events cannot be computed.***")

      st.subheader("Events with the Lowest Data Reliability (Highest Average Error Margins).")
      st.success("Earthquakes near ***Alaska, New Zealand, the Kermadec Islands, and Vanuatu*** exhibited the ***highest uncertainty scores***, suggesting lower data reliability due to ***sparse seismic station coverage*** and ***challenging geographic locations***.")

      st.subheader("Regions with the Highest Frequency of Deep-Focus Earthquakes (Depth > 300 km).")
      st.success("***Fiji*** recorded the highest number of deep-focus earthquakes ***(1,201)***, followed by ***Tonga, Indonesia, Japan Region, and Timor-Leste***. These regions are located along active subduction zones, where tectonic plates descend deep into the Earth's mantle.")

      st.divider()
elif page=="ℹ️ About the Project":
      

        st.title("ℹ️ About the Project")
        st.divider()

        st.header("📌 Project Overview")

        st.write("""
                    The **Global Seismic Trends Dashboard** is an end-to-end data analytics project
                    designed to analyze worldwide earthquake events from **2021–2026** using
                    SQL, Python, PostgreSQL, and Streamlit.

                    The project focuses on uncovering seismic patterns, earthquake characteristics,
                    and geographical trends through interactive dashboards and advanced SQL analysis.
                    """)


        st.header("🎯 Project Objective")

        st.write("""
        - Analyze global earthquake occurrences.
        - Identify seismic hotspots and high-risk regions.
        - Study earthquake magnitude and depth patterns.
        - Perform advanced SQL analysis using real-world data.
        - Build an interactive Streamlit dashboard for data exploration.
        """)


        st.header("🗂️ Dataset Information")

        st.markdown("""
        - **Source:** USGS Earthquake Catalog
        - **Time Period:** 2021–2026
        - **Records:** 114,000+ Earthquake Events
        - **Countries Covered:** 230+
        - **Database:** PostgreSQL
        """)


        st.header("🛠️ Tech Stack")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            - 🐍 Python
            - 🗄 PostgreSQL
            - 🔗 SQLAlchemy
            - 📊 Streamlit
            """)

        with col2:
            st.markdown("""
            - 📈 Plotly
            - 🐼 Pandas
            - 💻 VS Code
            - 📝 Git & GitHub
            """)


        st.header("💡 Skills Demonstrated")

        st.markdown("""
        - Data Cleaning & Preprocessing
        - SQL Query Optimization
        - Advanced SQL (CTEs, Window Functions, Aggregations)
        - Exploratory Data Analysis (EDA)
        - Data Visualization
        - Dashboard Development
        - Database Management
        - Business & Geological Insights
        """)

        st.header("🚀 Dashboard Features")

        st.markdown("""
        ✅ Dashboard

        ✅ Interactive SQL Analysis (27 Queries)

        ✅ Key Business & Geological Insights

        ✅ Earthquake Trend Analysis

        ✅ Magnitude & Depth Analysis

        ✅ Reporting Network Analysis

        ✅ Abbreviations & Metadata Reference
        """)
    
        st.header("👨‍💻 Developer")

        st.markdown("""
        **Navin R**

        Aspiring **Data Analyst** passionate about transforming raw data into meaningful insights through SQL, Python, and interactive dashboards.
        """)

        # ----------------------------------------------------
        # Connect
        # ----------------------------------------------------
        st.header("🔗 Connect")

        st.markdown("""
        📧 **Email:** navinravan68@gmail.com

        💼 **LinkedIn:** www.linkedin.com/in/navin-ravichandran-15a259404

        💻 **GitHub:** https://github.com/navinravan68-tech
        """)

        st.divider()

        st.caption(
        """
        Global Seismic Trends Dashboard © 2026

        Built with ❤️ using Streamlit | PostgreSQL | Python
        """
        )



