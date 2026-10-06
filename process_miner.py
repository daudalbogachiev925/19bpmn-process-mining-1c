from collections import defaultdict
import statistics
import networkx as nx

def mine(log: list) -> dict:
    """log: список событий {document_ref, status, changed_at}.
    Возвращает граф переходов, средние длительности, узкие места."""
    by_case = defaultdict(list)
    for e in log:
        by_case[e['document_ref']].append(e)

    transitions = defaultdict(int)
    durations = defaultdict(list)

    for case, events in by_case.items():
        events.sort(key=lambda x: x['changed_at'])
        for a, b in zip(events, events[1:]):
            key = (a['status'], b['status'])
            transitions[key] += 1
            durations[key].append(
                (b['changed_at'] - a['changed_at']).total_seconds())

    avg = {k: round(statistics.mean(v), 2) for k, v in durations.items()}
    median = {k: round(statistics.median(v), 2) for k, v in durations.items()}

    # Узкие места — переходы с самой большой медианой
    bottlenecks = sorted(median.items(), key=lambda x: -x[1])[:5]

    return {
        'transitions': dict(transitions),
        'avg': avg,
        'median': median,
        'bottlenecks': bottlenecks,
        'num_cases': len(by_case)
    }

def build_graph(transitions: dict) -> nx.DiGraph:
    g = nx.DiGraph()
    for (a, b), w in transitions.items():
        g.add_edge(a, b, weight=w)
    return g

def find_start_end(g):
    starts = [n for n in g.nodes if g.in_degree(n) == 0]
    ends = [n for n in g.nodes if g.out_degree(n) == 0]
    return starts, ends
