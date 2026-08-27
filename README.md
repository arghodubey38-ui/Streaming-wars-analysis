# Global Streaming Content Analysis

A Python data analysis project exploring how streaming content libraries — size, ratings, leading platform, and dominant genre — vary across 24 countries.

## Overview

This project analyzes `country_summary.csv`, a dataset summarizing streaming content by country. It answers questions such as:

- Which countries have the largest content libraries?
- Does library size relate to content quality (IMDb ratings)?
- Which platform dominates globally, and does the leading platform affect ratings?
- How consistent are ratings across countries?

## Dataset

**File:** `country_summary.csv`
**Rows:** 24 countries
**Columns:**

| Column | Type | Description |
|---|---|---|
| `country` | text | Country name |
| `total_titles` | number | Total number of titles available in that country |
| `avg_imdb` | number | Average IMDb rating of titles in that country |
| `top_platform` | text | Streaming platform with the most content in that country |
| `top_genre` | text | Most common genre in that country |

The dataset is clean — no missing values — so no data cleaning step is required before analysis.

**Note:** `top_platform` and `top_genre` are heavily skewed (Netflix and Drama dominate almost every row), so they offer limited variation on their own. The more interesting findings come from `total_titles` and `avg_imdb`.

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn

Install with:
```bash
pip install pandas numpy matplotlib seaborn
```

## Getting Started (Jupyter Notebook)

1. Make sure `country_summary.csv` is in the same folder as the notebook.
2. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
3. Open `Streaming_Wars_Analysis.ipynb`.
4. Run the cells in order (Shift+Enter), starting with the imports:
   ```python
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   import seaborn as sns
   ```
5. Load and preview the data:
   ```python
   df = pd.read_csv('country_summary.csv')
   df.head()
   ```
6. Check data quality:
   ```python
   df.info()
   df.isnull().sum()
   ```

## Core Analysis

**1. Top countries by content volume**
```python
df.sort_values('total_titles', ascending=False).head(10)
```

**2. Visualize the top 10**
```python
sns.barplot(data=df.sort_values('total_titles', ascending=False).head(10), x='total_titles', y='country')
plt.title('Top 10 Countries by Total Titles')
plt.show()
```

**3. Platform dominance**
```python
df['top_platform'].value_counts()
```

**4. Visualize platform dominance**
```python
sns.countplot(data=df, y='top_platform', order=df['top_platform'].value_counts().index)
plt.title('Number of Countries Where Each Platform Leads')
plt.show()
```

## Extended Analysis

**1. Rank countries by library size**
```python
df['title_rank'] = df['total_titles'].rank(ascending=False)
```

**2. Bucket countries into library-size categories**
```python
bins = [0, 100, 500, 6000]
labels = ['Small', 'Medium', 'Large']
df['library_size'] = pd.cut(df['total_titles'], bins=bins, labels=labels)
```

**3. Compare ratings across library-size categories**
```python
sns.boxplot(data=df, x='library_size', y='avg_imdb')
plt.title('Rating Spread by Library Size Category')
plt.show()
```

**4. Compare average ratings by leading platform**
```python
df.groupby('top_platform')['avg_imdb'].mean().sort_values(ascending=False)
```

**5. Correlation heatmap**
```python
sns.heatmap(df[['total_titles', 'avg_imdb']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
```

## Key Findings

- The United States, India, United Kingdom, South Korea, and Japan lead in total titles.
- Netflix is the top platform in the large majority of countries surveyed.
- Drama is the dominant genre almost everywhere, limiting genre-based comparisons.
- The most meaningful variation across countries shows up in `total_titles` and `avg_imdb`, not platform or genre.

## Project Structure

```
.
├── country_summary.csv          # Source dataset
├── Streaming_Wars_Analysis.ipynb # Jupyter notebook with analysis code
└── README.md                     # Project documentation
```

## License

For educational and portfolio use.
