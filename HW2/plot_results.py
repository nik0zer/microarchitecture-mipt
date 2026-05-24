import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def calculate_gmean(series):
    data = series.replace('ERR', np.nan).dropna().astype(float)
    data = data[data > 0]
    return np.exp(np.log(data).mean())

def plot_metric(combined_data, metric_name, title, filename):
    plt.figure(figsize=(15, 7))

    traces = combined_data.index.tolist()
    x = np.arange(len(traces))
    width = 0.2

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
    print(f"График сохранен в файл: {filename}")

csv_files = glob.glob("*-summary.csv")
if not csv_files:
    print("CSV файлы не найдены!")
    exit()

all_ipc = {}
all_mpki = {}

for f in csv_files:
    pred_name = f.replace("-summary.csv", "")
    df = pd.read_csv(f)

    df['IPC'] = pd.to_numeric(df['IPC'], errors='coerce')
    mpki_col = 'MPKI' if 'MPKI' in df.columns else 'L2_MissRate(%)'
    df[mpki_col] = pd.to_numeric(df[mpki_col], errors='coerce')

    df['Trace'] = df['Trace'].apply(lambda x: x.split('_')[0])

    ipc_series = df.set_index('Trace')['IPC']
    all_ipc[pred_name] = ipc_series

    mpki_series = df.set_index('Trace')[mpki_col]
    all_mpki[pred_name] = mpki_series

df_ipc = pd.DataFrame(all_ipc)
df_mpki = pd.DataFrame(all_mpki)

gmean_ipc = df_ipc.apply(calculate_gmean)
gmean_mpki = df_mpki.apply(calculate_gmean)

df_ipc.loc['GMEAN'] = gmean_ipc
df_mpki.loc['GMEAN'] = gmean_mpki

plot_metric(df_ipc, 'IPC', 'Comparison of IPC (Traces + GMEAN)', 'ipc_comparison.png')
plot_metric(df_mpki, 'MPKI / Miss Rate (%)', 'Comparison of Miss Rates (Traces + GMEAN)', 'miss_rate_comparison.png')