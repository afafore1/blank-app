import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    # Load the cleaned CSV data
    contract_value_path = "contract_value.csv"
    savings_path = "savings.csv"

    contract_value_df = pd.read_csv(contract_value_path, delimiter="\t")
    savings_df = pd.read_csv(savings_path, delimiter="\t")

    # Convert monetary values to numeric
    contract_value_df["Value"] = pd.to_numeric(contract_value_df["Value"].replace('[\$,]', '', regex=True),
                                               errors='coerce')
    savings_df["Saved"] = pd.to_numeric(savings_df["Saved"].replace('[\$,]', '', regex=True), errors='coerce')

    # Merge datasets
    merged_df = pd.merge(contract_value_df, savings_df, on=["Agency", "Description", "Uploaded on", "Link"])
    return merged_df


def main():
    st.set_page_config(layout="wide")
    st.title("Contract Savings Analysis")

    # Load Data
    df = load_data()

    # Layout Columns
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Contract Value vs Actual Savings")
        st.dataframe(df.style.format({"Value": "${:,.2f}", "Saved": "${:,.2f}"}))

    with col2:
        # Calculate Total Savings
        total_savings = df["Saved"].sum()
        total_contract_value = df["Value"].sum()
        st.subheader("Summary Metrics")
        st.metric(label="Total Contract Value", value=f"${total_contract_value:,.2f}")
        st.metric(label="Total Savings", value=f"${total_savings:,.2f}",
                  delta=f"{(total_savings / total_contract_value) * 100:.2f}% saved")

    # Aggregate Data by Agency
    savings_summary = df.groupby("Agency")[['Value', 'Saved']].sum().reset_index()

    # Plot Bar Chart with Seaborn
    st.subheader("Total Contract Value vs Savings by Agency")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Agency", y="Value", data=savings_summary, label="Contract Value", color="blue", alpha=0.7)
    sns.barplot(x="Agency", y="Saved", data=savings_summary, label="Saved", color="green", alpha=0.7)
    ax.set_xlabel("Agency")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Contract Value vs Savings by Agency")
    ax.legend()
    plt.xticks(rotation=90)

    st.pyplot(fig)

    # Interactive Agency Filter
    st.subheader("Filter by Agency")
    agency_selection = st.selectbox("Select an Agency", df["Agency"].unique())
    filtered_df = df[df["Agency"] == agency_selection]
    st.dataframe(filtered_df.style.format({"Value": "${:,.2f}", "Saved": "${:,.2f}"}))


if __name__ == "__main__":
    main()
