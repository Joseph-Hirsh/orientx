import matplotlib.pyplot as plt


def calculate_semantic_orientation(classifications_df):
    grouped = classifications_df.groupby("Date")["Orientation"].agg(
        output_count=lambda x: (x == 1).sum(),
        input_count=lambda x: (x == 0).sum()
    )

    grouped["semantic_orientation"] = grouped["output_count"] / (grouped["output_count"] + grouped["input_count"])

    return grouped.reset_index()


def visualize_semantic_orientation(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df["Date"], df["semantic_orientation"], marker="o", linestyle="-")
    plt.title("Semantic Orientation Over Time")
    plt.xlabel("Date")
    plt.ylabel("Semantic Orientation")
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.grid()
    plt.tight_layout()
    plt.show()
