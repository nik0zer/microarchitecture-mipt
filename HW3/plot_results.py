import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

def calculate_gmean(series):
    data = series.replace('ERR', np.nan).dropna().astype(float)
    data = data[data > 0]
    return np.exp(np.log(data).mean())

def plot_metric(combined_data, metric_name, title, filename):
    plt.figure(figsize=(15, 7))
    traces = combined_data.index.tolist()
    x = np.arange(len(traces))
    width = 0.15
    predictors = combined_data.columns

    for i, predictor in enumerate(predictors):
        plt.bar(x + (i * width) - (width * len(predictors) / 2),
                combined_data[predictor],
                width, label=predictor)

    plt.xlabel('Traces')
    plt.ylabel(metric_name)
    plt.title(title)
    plt.xticks(x, traces, rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename)

csv_files = glob.glob("L2-*-summary.csv")
if not csv_files:
    exit()

all_ipc = {}
all_miss_rate = {}

for f in csv_files:
    policy_name = f.replace("L2-", "").replace("-summary.csv", "")
    df = pd.read_csv(f)

    df['IPC'] = pd.to_numeric(df['IPC'], errors='coerce')
    df['L2_MissRate(%)'] = pd.to_numeric(df['L2_MissRate(%)'], errors='coerce')

    df['Trace'] = df['Trace'].apply(lambda x: x.split('_')[0])

    all_ipc[policy_name] = df.set_index('Trace')['IPC']
    all_miss_rate[policy_name] = df.set_index('Trace')['L2_MissRate(%)']

df_ipc = pd.DataFrame(all_ipc)
df_miss = pd.DataFrame(all_miss_rate)

df_ipc.loc['GMEAN'] = df_ipc.apply(calculate_gmean)
df_miss.loc['GMEAN'] = df_miss.apply(calculate_gmean)

plot_metric(df_ipc, 'IPC', 'L2 Policies Comparison: IPC (Traces + GMEAN)', 'l2_ipc_comparison.png')
plot_metric(df_miss, 'L2 Miss Rate (%)', 'L2 Policies Comparison: Miss Rate (Traces + GMEAN)', 'l2_miss_rate_comparison.png')