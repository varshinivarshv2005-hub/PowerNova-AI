from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

import pandas as pd


def generate_pdf_report(df, filename="powernova_report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    # --------------------------------
    # TITLE
    # --------------------------------
    title = Paragraph(
        "PowerNova AI - Electricity Analytics Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # --------------------------------
    # SUMMARY
    # --------------------------------
    avg_usage = round(df["usage_kwh"].mean(), 2)

    max_usage = round(df["usage_kwh"].max(), 2)

    min_usage = round(df["usage_kwh"].min(), 2)

    summary_text = f"""
    <b>Average Usage:</b> {avg_usage} kWh<br/>
    <b>Maximum Usage:</b> {max_usage} kWh<br/>
    <b>Minimum Usage:</b> {min_usage} kWh
    """

    summary = Paragraph(
        summary_text,
        styles["BodyText"]
    )

    elements.append(summary)

    elements.append(Spacer(1, 20))

    # --------------------------------
    # TABLE DATA
    # --------------------------------
    table_data = [["Timestamp", "Usage", "Voltage", "Current"]]

    recent_data = df.tail(10)

    for _, row in recent_data.iterrows():

        table_data.append([
            str(row["timestamp"]),
            str(row["usage_kwh"]),
            str(row["voltage"]),
            str(row["current"])
        ])

    # --------------------------------
    # TABLE
    # --------------------------------
    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige)
    ]))

    elements.append(table)

    # --------------------------------
    # BUILD PDF
    # --------------------------------
    doc.build(elements)

    return filename