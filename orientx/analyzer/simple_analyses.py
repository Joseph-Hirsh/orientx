import matplotlib.pyplot as plt


def calculate_percentages(classifications_df):
    # Group by date and calculate counts for each orientation type
    grouped = classifications_df.groupby("Date")["Orientation"].agg(
        output_count=lambda x: (x == 1).sum(),
        input_count=lambda x: (x == 0).sum()
    )

    # Calculate percentages of output and input classifications
    grouped["percent_output"] = grouped["output_count"] / (grouped["output_count"] + grouped["input_count"])
    grouped["percent_input"] = grouped["input_count"] / (grouped["output_count"] + grouped["input_count"])

    return grouped.reset_index()


def visualize_percentages(df):
    plt.figure(figsize=(12, 6))

    # Plot percent output over time
    plt.plot(df["date"], df["percent_output"], marker="o", linestyle="-", label="Percent Output")

    # Plot percent input over time
    plt.plot(df["date"], df["percent_input"], marker="o", linestyle="-", label="Percent Input")

    # Customize the plot
    plt.title("Percentage of Output and Input-Oriented Posts Over Time")
    plt.xlabel("Date")
    plt.ylabel("Percentage")
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Display the plot
    plt.show()

# Example usage:

