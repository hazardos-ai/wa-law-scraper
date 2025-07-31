# Examples

This section contains practical examples of using the D3 Project Template.

## Basic Usage

Here's a simple example to get you started:

```python
from d3_project_template import TemplateClass

# Create an instance
template = TemplateClass()

# Use the template
result = template.sample_method()
print(f"Result: {result}")
```

## Advanced Examples

### Data Processing Example

```python
import pandas as pd
from d3_project_template.data import process_data

# Load your data
df = pd.read_csv("data.csv")

# Process with the template
processed_df = process_data(df)
print(processed_df.head())
```

### Visualization Example

```python
import matplotlib.pyplot as plt
from d3_project_template.visualization import create_plot

# Generate a sample plot
fig, ax = create_plot(data, plot_type="scatter")
plt.show()
```

## Notebook Examples

For interactive examples, check out:

- [Basic Tutorial Notebook](notebooks/tutorial.ipynb)
- [Advanced Features Notebook](notebooks/advanced.ipynb)
- [Data Analysis Workflow](notebooks/workflow.ipynb)
