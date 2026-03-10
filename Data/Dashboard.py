import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Algorithm Benchmarks", layout="wide")
CSV_FILE = "results.csv"  
current_dir = os.path.dirname(__file__)
benchmark_dir = os.path.join(current_dir, "benchmark_results")
csv_path = os.path.join(current_dir, "benchmark_results", CSV_FILE)
# --- Data Loading Logic ---

@st.cache_data
def load_data():
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        # Optional: Add an efficiency metric
        # Higher is better (Found short path while exploring fewer cells)
        data['efficiency'] = data['path_length'] / data['cells_explored']
        return data
    return None

df = load_data()

# --- Dashboard UI ---
st.title("🏆 Maze Solver Analytics")

if df is not None:
    # Top Row Metrics
    st.subheader("Aggregate Statistics")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Total Runs", len(df))
    with m2:
        fastest = df.loc[df['runtime'].idxmin()]
        st.metric("Fastest Algorithm", fastest['algorithm'], f"{fastest['runtime']:.4f}s")
    with m3:
        avg_cells = int(df['cells_explored'].mean())
        st.metric("Avg Cells Explored", avg_cells)
    with m4:
        st.metric("Max Maze Size", f"{df['maze_width'].max()}x{df['maze_height'].max()}")

    st.divider()

    # Performance Comparison Plots
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Search Effort (Cells Explored)")
        # Box plot shows the spread and outliers (important for DFS)
        fig1 = px.box(df, x="algorithm", y="cells_explored", color="algorithm", 
                     notched=True, title="Exploration Breadth by Algorithm")
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.markdown("### Path Optimality")
        # Comparing path length against maze density
        fig2 = px.line(df.sort_values('density'), x="density", y="path_length", color="algorithm",
                      title="Path Length vs. Obstacle Density", markers=True)
      
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Detailed Table with Filters
    st.subheader("Drill-down Data")
    selected_algo = st.multiselect("Filter Algorithms", df['algorithm'].unique(), default=df['algorithm'].unique())
    
    view_df = df[df['algorithm'].isin(selected_algo)]
    st.dataframe(view_df.style.highlight_max(axis=0, subset=['runtime'], color='#ff4b4b22'), use_container_width=True)

else:
    st.error(f"Could not find `{CSV_FILE}` in the current directory.")
    st.info("Ensure your script is generating the CSV with the correct filename.")