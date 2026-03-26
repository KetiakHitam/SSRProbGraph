"""
Umamusume SSR Gacha Probability Graph
Reads pull probability data from the Excel spreadsheet and renders
an interactive Plotly chart in the browser.
"""

import os
import pandas as pd
import plotly.graph_objects as go

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(
    SCRIPT_DIR,
    "Copy of Umamusume_ Kitasan Black Gacha Probabilities.xlsx",
)
OUTPUT_HTML = os.path.join(SCRIPT_DIR, "index.html")

SHEET_NAME = "Kitasan Black Rate Up"

# Row/column indices in the raw spreadsheet (0-indexed).
# Data rows start at row 5 and run to row 104 (pulls 10..1000).
DATA_ROW_START = 5
DATA_ROW_END = 105  # exclusive
COL_PULLS = 1
COL_PROB_START = 4   # 0LB
COL_PROB_END = 9     # exclusive (4LB/MLB is col 8)
COL_INV_START = 10   # inverse chance columns ("1 in X")
COL_INV_END = 15     # exclusive

LB_LABELS = ["0LB", "1LB", "2LB", "3LB", "4LB / MLB"]

# Colors: grey for 0LB, scaling up to gold for MLB.
LB_COLORS = [
    "#2ECC71",  # 0LB  - green
    "#F1C40F",  # 1LB  - yellow
    "#E67E22",  # 2LB  - mustard orange
    "#E74C3C",  # 3LB  - orange
    "#C0392B",  # 4LB  - red
]

# Spark milestones (pulls where a guaranteed copy is awarded).
SPARK_MILESTONES = [200, 400, 600]


def load_data():
    """Return (pulls, probabilities_dict, inverse_dict) from the spreadsheet."""
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET_NAME, header=None)
    data = df.iloc[DATA_ROW_START:DATA_ROW_END]

    pulls = data.iloc[:, COL_PULLS].astype(int).tolist()

    probs = {}
    inverse = {}
    for i, label in enumerate(LB_LABELS):
        raw = data.iloc[:, COL_PROB_START + i]
        probs[label] = [float(v) * 100 for v in raw]  # decimal -> %

        inv_raw = data.iloc[:, COL_INV_START + i]
        inverse[label] = [str(v) if pd.notna(v) else "" for v in inv_raw]

    return pulls, probs, inverse


def build_figure(pulls, probs, inverse):
    """Construct the Plotly figure with all traces and annotations."""
    fig = go.Figure()

    for i, label in enumerate(LB_LABELS):
        # Build custom hover text with percentage and inverse odds.
        hover = []
        for j, p in enumerate(pulls):
            pct = probs[label][j]
            inv = inverse[label][j]
            text = (
                f"<b>{label}</b><br>"
                f"Pulls: {p}<br>"
                f"Chance: {pct:.4f}%<br>"
            )
            if inv:
                text += f"Odds: {inv}"
            hover.append(text)

        fig.add_trace(go.Scatter(
            x=pulls,
            y=probs[label],
            mode="lines",
            name=label,
            line=dict(color=LB_COLORS[i], width=2.5),
            hovertext=hover,
            hoverinfo="text",
        ))

    # Vertical dashed lines at spark milestones.
    for sp in SPARK_MILESTONES:
        fig.add_vline(
            x=sp,
            line_dash="dash",
            line_color="rgba(255,255,255,0.25)",
            annotation_text=f"Spark ({sp})",
            annotation_position="top",
            annotation_font_color="rgba(255,255,255,0.5)",
            annotation_font_size=11,
        )

    # 50% reference line.
    fig.add_hline(
        y=50,
        line_dash="dot",
        line_color="rgba(255,255,255,0.15)",
        annotation_text="50%",
        annotation_position="left",
        annotation_font_color="rgba(255,255,255,0.35)",
        annotation_font_size=11,
    )

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text="Umamusume SSR Rate-Up Gacha Probabilities (0.75%)",
            font=dict(size=20),
        ),
        xaxis=dict(
            title="Number of Pulls",
            dtick=50,
            range=[0, 1010],
            gridcolor="rgba(255,255,255,0.08)",
        ),
        yaxis=dict(
            title="Probability (%)",
            range=[0, 105],
            dtick=10,
            gridcolor="rgba(255,255,255,0.08)",
        ),
        legend=dict(
            title="Limit Break",
            font=dict(size=13),
            bgcolor="rgba(0,0,0,0.4)",
        ),
        hovermode="x unified",
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#16213e",
        margin=dict(t=80, b=60, l=60, r=30),
    )

    return fig


def main():
    pulls, probs, inverse = load_data()
    fig = build_figure(pulls, probs, inverse)
    fig.write_html(OUTPUT_HTML, auto_open=True)
    print(f"Graph saved to: {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
