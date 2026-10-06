from datetime import datetime
from process_miner import mine

def test_simple_chain():
    log = [
        {'document_ref': 'A', 'status': 'new', 'changed_at': datetime(2024,1,1,10)},
        {'document_ref': 'A', 'status': 'done', 'changed_at': datetime(2024,1,1,11)},
        {'document_ref': 'B', 'status': 'new', 'changed_at': datetime(2024,1,1,10)},
        {'document_ref': 'B', 'status': 'done', 'changed_at': datetime(2024,1,1,12)},
    ]
    r = mine(log)
    assert r['transitions'][('new','done')] == 2
    assert r['num_cases'] == 2
