import sys
import pandas as pd
from event_log import load_events
from process_miner import mine, build_graph
from bpmn_renderer import render_bpmn, render_svg

def main(csv_path):
    print("=== Загрузка событий ===")
    df = load_events(csv_path)
    print(f"Событий: {len(df)}, дел: {df['document_ref'].nunique()}")

    log = df.to_dict('records')
    result = mine(log)

    print(f"\n=== Переходы ({len(result['transitions'])}) ===")
    for k, v in sorted(result['transitions'].items(), key=lambda x: -x[1]):
        print(f"  {k[0]} → {k[1]}: {v}")

    print(f"\n=== Топ-5 узких мест (по медиане, сек) ===")
    for (a, b), sec in result['bottlenecks']:
        print(f"  {a} → {b}: {sec} сек")

    print("\n=== Граф и BPMN ===")
    g = build_graph(result['transitions'])
    render_bpmn(result['transitions'], 'process.bpmn')
    render_svg(g, 'process.svg')
    print("Готово: process.bpmn, process.svg")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'examples/sample_log.csv'
    main(path)
