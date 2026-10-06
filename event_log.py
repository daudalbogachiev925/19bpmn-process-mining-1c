import pandas as pd

def load_events(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=['changed_at'])
    df.sort_values(['document_ref', 'changed_at'], inplace=True)
    return df

def split_by_case(df: pd.DataFrame) -> dict:
    cases = {}
    for doc, group in df.groupby('document_ref'):
        cases[doc] = group.to_dict('records')
    return cases

def case_duration(case_events: list) -> float:
    if len(case_events) < 2:
        return 0
    return (case_events[-1]['changed_at'] - case_events[0]['changed_at']).total_seconds()
