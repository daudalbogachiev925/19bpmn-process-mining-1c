from lxml import etree

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"

def render_bpmn(transitions: dict, output='process.bpmn'):
    """Строит BPMN 2.0 XML по переходам."""
    nsmap = {None: BPMN_NS}
    root = etree.Element(f'{{{BPMN_NS}}}definitions', nsmap=nsmap)
    process = etree.SubElement(root, f'{{{BPMN_NS}}}process',
                               id='Process_1', isExecutable='false')
    nodes = set()
    for a, b in transitions:
        nodes.add(a); nodes.add(b)

    node_ids = {}
    for i, n in enumerate(sorted(nodes)):
        tid = f'task_{i}'
        node_ids[n] = tid
        etree.SubElement(process, f'{{{BPMN_NS}}}task',
                         id=tid, name=str(n))

    for i, ((a, b), w) in enumerate(transitions.items()):
        etree.SubElement(process, f'{{{BPMN_NS}}}sequenceFlow',
                         id=f'flow_{i}',
                         sourceRef=node_ids[a],
                         targetRef=node_ids[b],
                         name=str(w))

    tree = etree.ElementTree(root)
    tree.write(output, pretty_print=True, xml_declaration=True,
               encoding='UTF-8')
    return output

def render_svg(graph, output='process.svg'):
    """Простой SVG-рендер через matplotlib."""
    import matplotlib.pyplot as plt
    import networkx as nx
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_color='#aed6f1',
            node_size=2000, font_size=9, arrows=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    return output
