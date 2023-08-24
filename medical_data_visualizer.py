import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
weight_data = df["weight"].to_numpy()
height_data = df["height"].to_numpy()
height_data_inm_squared = (height_data / 100) ** 2
overweight_data = np.full(70000, 0)
for i in range(len(df)):
    if weight_data[i] / height_data_inm_squared[i] > 25:
        overweight_data[i] = 1
    else:
        overweight_data[i] = 0
df['overweight'] = overweight_data

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
chol_data = df["cholesterol"].to_numpy()
gluc_data = df["gluc"].to_numpy()
new_chol_data = np.full(70000, 0)
new_gluc_data = np.full(70000, 0)
for i in range(len(df)):
    if chol_data[i] == 1:
        new_chol_data[i] = 0
    else:
        new_chol_data[i] = 1
for i in range(len(df)):
    if gluc_data[i] == 1:
        new_gluc_data[i] = 0
    else:
        new_gluc_data[i] = 1
df['cholesterol'] = new_chol_data
df['gluc'] = new_gluc_data

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat["total"] = 1
    df_cat = df_cat.groupby(["cardio","variable","value"], as_index = False).count()
    
    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat, x = "variable", y = "total", kind = "bar", hue="value", col = "cardio").fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr(method="pearson")

    # Generate a mask for the upper triangle
    mask = np.triu(corr)



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12,12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, linewidths=1, annot = True, square = True, mask = mask, fmt = ".1f", center = 0.08, cbar_kws = {"shrink": 0.5})



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
