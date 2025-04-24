
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# =====================
# 基础数据构建
# =====================

immune_cells = {
    "Macrophages": {
        "genes": ["CD68", "CD163", "MRC1", "MARCO"],
        "description": "Macrophages clear debris, regulate inflammation, and aid tissue repair."
    },
    "Monocytes": {
        "genes": ["CD14", "FCN1", "LYZ"],
        "description": "Monocytes are recruited during inflammation and differentiate into macrophages."
    },
    "Neutrophils": {
        "genes": ["S100A8", "S100A9", "MPO"],
        "description": "Neutrophils are first responders that fight infection and modulate inflammation."
    },
    "CD4+ T cells": {
        "genes": ["CD4", "IL7R", "FOXP3"],
        "description": "CD4+ T cells coordinate immune responses and regulate other immune cells."
    },
    "CD8+ T cells": {
        "genes": ["CD8A", "GZMB", "PRF1"],
        "description": "CD8+ T cells directly kill infected or damaged cells."
    },
    "B cells": {
        "genes": ["CD19", "MS4A1", "CD79A"],
        "description": "B cells produce antibodies and mediate humoral immunity."
    },
    "NK cells": {
        "genes": ["NCAM1", "NKG7", "KLRK1"],
        "description": "Natural Killer cells target virus-infected and cancerous cells."
    },
    "Eosinophils": {
        "genes": ["SIGLEC8", "IL5RA", "CCR3"],
        "description": "Eosinophils are involved in parasitic defense and allergic responses."
    },
    "Mast cells": {
        "genes": ["TPSAB1", "CPA3", "KIT"],
        "description": "Mast cells release histamine and modulate inflammation."
    }
}

# =====================
# 模拟 GTEx 表达数据
# =====================

def load_expression_data():
    np.random.seed(42)
    genes = sum([info["genes"] for info in immune_cells.values()], [])
    data = {
        "Gene": [],
        "Tissue": [],
        "TPM": []
    }
    for gene in genes:
        for tissue in ["Heart_Atrial", "Heart_Ventricular"]:
            tpm_values = np.random.normal(loc=5 if "Heart_Ventricular" in tissue else 2, scale=0.5, size=50)
            data["Gene"].extend([gene]*50)
            data["Tissue"].extend([tissue]*50)
            data["TPM"].extend(tpm_values)
    df = pd.DataFrame(data)
    return df

def plot_expression(df, gene):
    subset = df[df["Gene"] == gene]
    fig = go.Figure()
    for tissue in subset["Tissue"].unique():
        df_tissue = subset[subset["Tissue"] == tissue]
        fig.add_trace(go.Box(y=df_tissue["TPM"], name=tissue, boxpoints="all", jitter=0.5))
    fig.update_layout(title=f"{gene} Expression in Heart Tissues (GTEx Simulated)",
                      yaxis_title="TPM",
                      height=400)
    return fig

# =====================
# Streamlit 页面主函数
# =====================

def main():
    st.set_page_config(layout="wide")
    st.title("🫀 CardioImmune Atlas v2")
    st.markdown("### Immune Cell Marker Explorer (Standard Streamlit Version)")

    df = load_expression_data()

    cell = st.selectbox("Select an immune cell type:", list(immune_cells.keys()))
    st.info(immune_cells[cell]["description"])

    gene = st.selectbox("Select a marker gene:", immune_cells[cell]["genes"])
    st.plotly_chart(plot_expression(df, gene), use_container_width=True)

if __name__ == "__main__":
    main()
