queries={
    1:{
        "title":" Top 10 strongest earthquakes",
        "sql":"""SELECT id,place, mag
                    FROM earthquake_data
                    ORDER BY mag DESC
                    LIMIT 10;"""
    },
    2:{
        "title":"Top 10 deepest earthquakes",
        "sql":"""SELECT
                    id,
                    place,
                    depth_km
                    FROM earthquake_data
                ORDER BY depth_km DESC
                LIMIT 10;"""
    },
    3:{
        "title":" Shallow earthquakes < 50 km and mag > 7.5",
        "sql":"""SELECT place, mag, depth_km, depth_category
         FROM earthquake_data
         WHERE mag>7.5 AND depth_km<50;"""
    },
    4:{
        "title":" Average depth per country",
        "sql":"""SELECT country, AVG(depth_km) as average_depth
         FROM earthquake_data
         GROUP BY country
         ORDER BY average_depth DESC ;"""
    },
    5:{
        "title":" Average magnitude per magnitude type",
        "sql":"""SELECT mag_type, AVG(mag) as average_magnitude
         FROM earthquake_data
         GROUP BY mag_type
         ORDER BY average_magnitude DESC;"""
    },
    6:{
        "title":"Year with most earthquakes",
        "sql":"""SELECT year,count(type) as most_eq
            FROM earthquake_data
            GROUP BY year
            LIMIT 1;"""
    },
    7:{
        "title":"Month with highest number of earthquakes",
        "sql":"""SELECT month,count(type) as most_eq
            FROM earthquake_data
            GROUP BY month
            ORDER BY most_eq DESC
            LIMIT 1;"""
    },
    8:{
        "title":"Day of week with most earthquakes",
        "sql":"""SELECT day_of_week,count(type) as most_eq
            FROM earthquake_data
            GROUP BY day_of_week
            LIMIT 1;"""
    },
    9:{
        "title":" Count of earthquakes per hour of day",
        "sql":"""SELECT
        EXTRACT(HOUR FROM CAST("time" AS TIMESTAMP)) AS hour_of_day,
        COUNT(*) AS earthquake_count
        FROM earthquake_data
        GROUP BY hour_of_day
        ORDER BY hour_of_day;"""
    },
    10:{
        "title":"Most active reporting network",
        "sql":"""SELECT net,count(net) as most_reported
        FROM earthquake_data
        GROUP BY net
        ORDER BY most_reported DESC
        LIMIT 1;"""
    },
    11:{
        "title":"top 5 highest casualties",
        "sql":"""SELECT
                place,mag,
                sig,depth_km
                FROM earthquake_data
                ORDER BY mag DESC
                LIMIT 5;"""
    },
    12:{
        "title":"Average economic loss by alert level",
        "sql":"""SELECT
        alert,
        AVG(mag) AS avg_magnitude,
        AVG(sig) AS avg_significance,
        COUNT(*) AS earthquake_count
        FROM earthquake_data
        WHERE alert IS NOT NULL
        GROUP BY alert
        ORDER BY avg_significance DESC;"""

    },
    13:{
        "title":"Count of reviewed vs automatic earthquakes ",
        "sql":"""SELECT status, COUNT(status) as count
            FROM earthquake_data
            GROUP BY status;"""
    },
    14:{
        "title":"Count by earthquake type",
        "sql":"""SELECT type, COUNT(type) as count
            FROM earthquake_data
            GROUP BY type
            ORDER BY count DESC;"""
    },
    15:{
        "title":" Number of earthquakes by data type",
        "sql":"""SELECT
    TRIM(unnest(string_to_array(types, ','))) AS type_name,
    COUNT(types) AS count
    FROM earthquake_data
    WHERE types is not null
    GROUP BY type_name
    ORDER BY count DESC;"""
    },
    16:{
        "title":"Average RMS and gap per country",
        "sql":"""SELECT country, AVG(rms)AS avg_rms,
       AVG(gap)AS avg_gap
    FROM earthquake_data
    WHERE country IS NOT NULL
    AND country <> 'Unknown'
    GROUP BY country
    ORDER BY avg_rms , avg_gap DESC
    LIMIT 20;"""
    },
    17:{
        "title":"Events with high station coverage ",
        "sql":"""SELECT country, nst
        FROM earthquake_data
        ORDER BY nst DESC
        LIMIT 15;"""
    },
    18:{
        "title":"Count earthquakes by alert levels",
        "sql":"""SELECT alert, COUNT(alert) as EQ_count
         FROM earthquake_data
         WHERE type = 'earthquake'
         GROUP BY alert
         ORDER BY EQ_count DESC;"""
    },
    19:{
        "title":"The top 5 countries with the highest average magnitude of earthquakes in the past 5 years ",
        "sql":"""SELECT country, ROUND(CAST(AVG(mag)AS numeric),2) AS avg_mag
        FROM earthquake_data
        WHERE year BETWEEN 2021 AND 2026
        GROUP BY country
        ORDER BY avg_mag DESC
        LIMIT 5;"""
    },
    20:{
        "title":"Countries that have experienced both shallow and deep earthquakes within the same month.",
        "sql":"""SELECT country,
                month,
                SUM(CASE WHEN depth_category = 'Shallow' THEN 1 ELSE 0 END) AS shallow_count,
                SUM(CASE WHEN depth_category = 'Deep' THEN 1 ELSE 0 END) AS deep_count
        FROM earthquake_data
        WHERE depth_category IN ('Shallow', 'Deep')
        GROUP BY country, month
        HAVING COUNT(DISTINCT depth_category) = 2
        ORDER BY country, month;"""
    },
    21:{
        "title":"the year-over-year growth rate in the total number of earthquakes globally ",
        "sql":"""WITH yearly_counts AS (
    SELECT year,
           COUNT(*) AS total_earthquakes
    FROM earthquake_data
    GROUP BY year
)
SELECT year,
       total_earthquakes,
       ROUND(
           (
             (total_earthquakes -
              LAG(total_earthquakes) OVER (ORDER BY year)
             ) * 100.0
           ) /
           LAG(total_earthquakes) OVER (ORDER BY year),
           2
       ) AS yoy_growth_rate
            FROM yearly_counts
            ORDER BY year;"""
    },
    22:{
        "title":" List the 3 most seismically active regions by combining both frequency and average magnitude",
        "sql":"""SELECT place,
       COUNT(*) AS earthquake_count,
       ROUND(AVG(mag)::numeric,2) AS avg_mag,
       ROUND((COUNT(*) * AVG(mag))::numeric,2) AS activity_score
            FROM earthquake_data
            GROUP BY place
            ORDER BY activity_score DESC
            LIMIT 3;"""

    },
    23:{
        "title":"The average depth of earthquakes within ±5° latitude range of the equator",
        "sql":"""SELECT country,
                ROUND(AVG(depth_km)::numeric,2) AS avg_depth
        FROM earthquake_data
        WHERE latitude BETWEEN -5 AND 5
        GROUP BY country
        ORDER BY avg_depth DESC;"""

    },
    24:{
        "title":"Countries having the highest ratio of shallow to deep earthquakes",
        "sql":"""SELECT country,
       COUNT(CASE WHEN depth_category='Shallow' THEN 1 END) AS shallow_count,
       COUNT(CASE WHEN depth_category='Deep' THEN 1 END) AS deep_count,
       ROUND(
           COUNT(CASE WHEN depth_category='Shallow' THEN 1 END)::numeric /
           NULLIF(COUNT(CASE WHEN depth_category='Deep' THEN 1 END),0),
           2
       ) AS shallow_deep_ratio
        FROM earthquake_data
        GROUP BY country
        ORDER BY shallow_deep_ratio DESC NULLS LAST
        LIMIT 25;"""
    },
    25:{
        "title":"The average magnitude difference between earthquakes with tsunami alerts and those without.",
        "sql":"""SELECT
    ROUND(AVG(CASE WHEN tsunami = 1 THEN mag END)::numeric, 2) AS tsunami_avg_mag,
    ROUND(AVG(CASE WHEN tsunami = 0 THEN mag END)::numeric, 2) AS non_tsunami_avg_mag,
    ROUND(
        (
            AVG(CASE WHEN tsunami = 1 THEN mag END) -
            AVG(CASE WHEN tsunami = 0 THEN mag END)
        )::numeric,
        2
    ) AS magnitude_difference
        FROM earthquake_data;"""

    },
    26:{
        "title":"Events with the lowest data reliability (highest average error margins)",
        "sql":"""SELECT id,
       place,
       gap,
       rms,
       ROUND((gap * rms)::numeric,2) AS reliability_score
        FROM earthquake_data
        ORDER BY reliability_score DESC
        LIMIT 20;"""

    },
    27:{
        "title":"the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)",
        "sql":"""SELECT country,
       COUNT(*) AS deep_focus_count
        FROM earthquake_data
        WHERE depth_km > 300
        GROUP BY country
        ORDER BY deep_focus_count DESC;"""

    }
}