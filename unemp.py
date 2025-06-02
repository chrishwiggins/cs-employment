# < some code ; chris.wiggins@gmail.com >
import pandas as pd
import matplotlib.pyplot as plt

# data from the New York Fed.
# different college majors and their unemployment/underemployment rates.

############
### get data
############

# It's an Excel file sitting right on the NY Fed's site.
data_source_url = (
    "https://www.newyorkfed.org/medialibrary/Research/Interactives/"
    "Data/college-labor-market/College-labor-data"
)

# This "outcomes by major" sheet has some extra stuff at the top we don't need.
# Looks like the actual data kicks off at row 11 (which is index 10 if you're a zero-based counter).
try:
    major_outcomes_df = pd.read_excel(
        data_source_url,
        sheet_name="outcomes by major",
        header=10,  # Skip those first 10 rows of junk
    )
except Exception as e:
    print(
        f"Whoops! Couldn't grab the data. Double-check the URL or your internet connection. Error: {e}"
    )
    exit()

# For this analysis, we're really only interested in the major, unemployment rate,
# and underemployment rate. Let's also ditch any rows that are missing info in those columns.
cleaned_df = major_outcomes_df[
    ["Major", "Unemployment Rate", "Underemployment Rate"]
].dropna()

# For clarity, pick out some "star" majors.
# We'll highlight Computer Science, the overall average, and the majors
# chilling at the top or bottom of the unemployment and underemployment lists.
cs_data = cleaned_df[cleaned_df["Major"] == "Computer Science"].iloc[0]
overall_data = cleaned_df[cleaned_df["Major"] == "Overall"].iloc[0]
most_unemployed = cleaned_df.loc[cleaned_df["Unemployment Rate"].idxmax()]
least_unemployed = cleaned_df.loc[cleaned_df["Unemployment Rate"].idxmin()]
most_underemployed = cleaned_df.loc[cleaned_df["Underemployment Rate"].idxmax()]
least_underemployed = cleaned_df.loc[cleaned_df["Underemployment Rate"].idxmin()]

# EDA: Let's get this scatter plot cooking.
plt.figure(figsize=(14, 10))  # A decent size so we can actually read it

# First, throw all the other majors on there as subtle gray points for some context.
plt.scatter(
    cleaned_df["Unemployment Rate"],
    cleaned_df["Underemployment Rate"],
    color="lightgray",
    zorder=1,  # Keep these in the background
    label="Other Majors",
)

# Our "star" majors get different colors and beefier markers so they stand out.
plt.scatter(
    cs_data["Unemployment Rate"],
    cs_data["Underemployment Rate"],
    color="red",
    s=120,
    label=f"Computer Science ({cs_data['Unemployment Rate']}%, {cs_data['Underemployment Rate']}%)",
)
plt.scatter(
    overall_data["Unemployment Rate"],
    overall_data["Underemployment Rate"],
    color="blue",
    s=120,
    label=f"Overall ({overall_data['Unemployment Rate']}%, {overall_data['Underemployment Rate']}%)",
)
plt.scatter(
    most_unemployed["Unemployment Rate"],
    most_unemployed["Underemployment Rate"],
    color="green",
    s=120,
    label=f"Highest Unemployment: {most_unemployed['Major']} ({most_unemployed['Unemployment Rate']}%)",
)
plt.scatter(
    least_unemployed["Unemployment Rate"],
    least_unemployed["Underemployment Rate"],
    color="orange",
    s=120,
    label=f"Lowest Unemployment: {least_unemployed['Major']} ({least_unemployed['Unemployment Rate']}%)",
)
plt.scatter(
    most_underemployed["Unemployment Rate"],
    most_underemployed["Underemployment Rate"],
    color="purple",
    s=120,
    label=f"Highest Underemployment: {most_underemployed['Major']} ({most_underemployed['Underemployment Rate']}%)",
)
plt.scatter(
    least_underemployed["Unemployment Rate"],
    least_underemployed["Underemployment Rate"],
    color="brown",
    s=120,
    label=f"Lowest Underemployment: {least_underemployed['Major']} ({least_underemployed['Underemployment Rate']}%)",
)


# Okay, this might get a little busy, but we're labeling every single point.
# The special "star" points get bigger, colored labels, too.
for index, row in cleaned_df.iterrows():
    label_color = "gray"
    label_size = 8

    # Figuring out if this major is one of our special ones, then tweaking its label.
    if row["Major"] == "Computer Science":
        label_color = "red"
        label_size = 12
    elif row["Major"] == "Overall":
        label_color = "blue"
        label_size = 12
    elif row["Major"] == most_unemployed["Major"]:
        label_color = "green"
        label_size = 12
    elif row["Major"] == least_unemployed["Major"]:
        label_color = "orange"
        label_size = 12
    elif row["Major"] == most_underemployed["Major"]:
        label_color = "purple"
        label_size = 12
    elif row["Major"] == least_underemployed["Major"]:
        label_color = "brown"
        label_size = 12

    plt.text(
        x=row["Unemployment Rate"]
        + 0.1,  # Nudging the label a tiny bit so it's not sitting right on the point
        y=row["Underemployment Rate"] + 0.1,
        s=row["Major"],
        fontsize=label_size,
        color=label_color,
        zorder=2,  # Make sure these labels show up on top
    )

# Last touches on the plot: titles and labels to make it super clear.
plt.xlabel("Unemployment Rate (%)", fontsize=14)
plt.ylabel("Underemployment Rate (%)", fontsize=14)
plt.title("Unemployment vs. Underemployment by Major (All Labeled!)", fontsize=16)
plt.legend(
    loc="upper left", bbox_to_anchor=(1, 1)
)  # Shoving the legend outside so it doesn't block anything
plt.grid(alpha=0.3)  # A subtle grid, just enough to help guide the eye
plt.tight_layout()  # This cleans up the plot, no more cut-off labels!

# instead of showing the plot, save it to a file.
plt.savefig("unemployment_underemployment_plot.png")
# plt.close()
# < /some code >
