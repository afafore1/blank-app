import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data():
    # Load the cleaned CSV data
    contract_value_path = "contract_value.csv"
    savings_path = "savings.csv"
    
    contract_value_df = pd.read_csv(contract_value_path, delimiter="\t")
    savings_df = pd.read_csv(savings_path, delimiter="\t")
    
    # Convert monetary values to numeric
    contract_value_df["Value"] = pd.to_numeric(contract_value_df["Value"].replace('[\$,]', '', regex=True), errors='coerce')
    savings_df["Saved"] = pd.to_numeric(savings_df["Saved"].replace('[\$,]', '', regex=True), errors='coerce')
    
    # Merge datasets
    merged_df = pd.merge(contract_value_df, savings_df, on=["Agency", "Description", "Uploaded on", "Link"])
    return merged_df

def main():
    st.set_page_config(layout="wide")
    st.title("Contract Savings Analysis")
    
    # Load Data
    df = load_data()
    
    # Interactive Agency Filter
    st.subheader("Filter by Agency")
    agency_selection = st.selectbox("Select an Agency", ["All"] + list(df["Agency"].unique()))
    
    filtered_df = df if agency_selection == "All" else df[df["Agency"] == agency_selection]
    
    # Display table
    st.subheader(f"Contract Details for {agency_selection}")
    st.dataframe(filtered_df.style.format({"Value": "${:,.2f}", "Saved": "${:,.2f}"}))
    
    # Aggregate Data by Agency
    savings_summary = filtered_df.groupby("Agency")[['Value', 'Saved']].sum().reset_index()
    
    if agency_selection == "All":
        # Display Summary Metrics
        total_savings = df["Saved"].sum()
        total_contract_value = df["Value"].sum()
        top_saving_agency = df.groupby("Agency")["Saved"].sum().idxmax()
        least_saving_agency = df.groupby("Agency")["Saved"].sum().idxmin()
        highest_contract_agency = df.groupby("Agency")["Value"].sum().idxmax()
        
        st.subheader("Summary Metrics")
        st.metric(label="Total Contract Value", value=f"${total_contract_value:,.2f}")
        st.metric(label="Total Savings", value=f"${total_savings:,.2f}", delta=f"{(total_savings/total_contract_value)*100:.2f}% saved")
        st.write(f"**Top Saving Agency:** {top_saving_agency}")
        st.write(f"**Agency with Least Savings:** {least_saving_agency}")
        st.write(f"**Agency with Highest Contract Value:** {highest_contract_agency}")
        
        # Heatmap for Savings Distribution
        st.subheader("Savings Heatmap by Agency")
        heatmap_data = df.pivot_table(index="Agency", values="Saved", aggfunc=np.sum)
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.heatmap(heatmap_data, cmap="Greens", annot=True, fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig)
    else:
        # Plot Pie Chart for Selected Agency
        st.subheader(f"Savings Distribution for {agency_selection}")
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie([savings_summary["Saved"].sum(), savings_summary["Value"].sum() - savings_summary["Saved"].sum()], 
               labels=["Saved", "Remaining Value"], autopct='%1.1f%%', startangle=140, colors=["green", "blue"])
        ax.set_title(f"Savings Breakdown for {agency_selection}")
        st.pyplot(fig)
    
if __name__ == "__main__":
    main()
