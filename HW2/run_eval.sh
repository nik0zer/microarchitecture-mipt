#!/bin/bash

if [ "$#" -ne 2 ]; then
    exit 1
fi

ORIG_DIR="$(pwd)"
CHAMPSIM_DIR="$1"
PREDICTOR="$2"

WARMUP=2000000
SIM=10000000

cd "$CHAMPSIM_DIR" || exit 1

sed -i -E "s/\"branch_predictor\":[ \t]*\"[a-zA-Z0-9_]+\"/\"branch_predictor\": \"$PREDICTOR\"/g" champsim_config.json

./config.sh champsim_config.json
make -j$(nproc)

if [ ! -f "bin/champsim" ]; then
    exit 1
fi

TRACES_DIR="traces"
OUT_DIR="$ORIG_DIR/${PREDICTOR}-result"
SUMMARY_FILE="$ORIG_DIR/${PREDICTOR}-summary.csv"

mkdir -p "$OUT_DIR"

echo "Trace,IPC,Instructions,Accuracy(%),MPKI,Mispredictions" > "$SUMMARY_FILE"

shopt -s nullglob
TRACES=("$TRACES_DIR"/*.xz)
TOTAL_TRACES=${#TRACES[@]}

if [ "$TOTAL_TRACES" -eq 0 ]; then
    exit 1
fi

CURRENT=1
for TRACE in "${TRACES[@]}"; do
    BASENAME=$(basename "$TRACE" .champsimtrace.xz)
    LOG_FILE="$OUT_DIR/${BASENAME}.log"

    echo -n "[$CURRENT / $TOTAL_TRACES] $BASENAME ... "

    ./bin/champsim --warmup-instructions $WARMUP --simulation-instructions $SIM "$TRACE" > "$LOG_FILE" 2>&1

    IPC=$(grep "cumulative IPC:" "$LOG_FILE" | tail -n 1 | awk '{print $5}')
    INSTR=$(grep "cumulative IPC:" "$LOG_FILE" | tail -n 1 | awk '{print $7}')
    ACCURACY=$(grep "Branch Prediction Accuracy:" "$LOG_FILE" | tail -n 1 | awk '{print $6}' | tr -d '%')
    MPKI=$(grep "Branch Prediction Accuracy:" "$LOG_FILE" | tail -n 1 | awk '{print $8}')

    if [ -z "$IPC" ]; then IPC="ERR"; fi
    if [ -z "$ACCURACY" ]; then ACCURACY="ERR"; fi
    if [ -z "$MPKI" ]; then MPKI="ERR"; fi
    if [ -z "$INSTR" ]; then INSTR=$SIM; fi

    if [ "$MPKI" != "ERR" ] && [ "$INSTR" != "ERR" ]; then
        MISSES=$(awk "BEGIN { printf \"%d\", ($MPKI * $INSTR / 1000) }")
    else
        MISSES="ERR"
    fi

    echo "$BASENAME,$IPC,$INSTR,$ACCURACY,$MPKI,$MISSES" >> "$SUMMARY_FILE"
    echo "Done"

    ((CURRENT++))
done