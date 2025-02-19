import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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
    st.title("Contract Savings Analysis")

    # Load Data
    df = load_data()

    # Display Table
    st.subheader("Contract Value vs Actual Savings")
    st.dataframe(df)

    # Aggregate Data by Agency
    savings_summary = df.groupby("Agency")[['Value', 'Saved']].sum().reset_index()

    # Calculate Total Savings
    total_savings = savings_summary["Saved"].sum()

    # Display Total Savings
    st.subheader("Total Amount Saved")
    st.write(f"**Total Savings: ${total_savings:,.2f}**")

    # Plot Bar Chart
    st.subheader("Total Contract Value vs Savings by Agency")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(savings_summary["Agency"], savings_summary["Value"], label="Contract Value", alpha=0.7)
    ax.bar(savings_summary["Agency"], savings_summary["Saved"], label="Saved", alpha=0.7)
    ax.set_xlabel("Agency")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Contract Value vs Savings by Agency")
    ax.legend()
    plt.xticks(rotation=90)

    st.pyplot(fig)


if __name__ == "__main__":
    main()