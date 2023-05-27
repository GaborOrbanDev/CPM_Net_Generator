print("-- Minimális méretű projektháló generátor --")

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from typing import Union
import argparse


def read_and_parse_file(file_name: str) -> pd.DataFrame:
    project = pd.read_excel(file_name)
    project.Requirements = project.Requirements.apply(lambda x: [] if pd.isnull(x) else x.split(','))
    project["abc"] = project.Requirements.apply(lambda x: "".join(x))
    project["length"] = project.Requirements.apply(lambda x: len(x))
    project = project.sort_values(by=["length","abc"])
    project.reset_index().drop("index", axis="columns", inplace=True)
    project.drop("abc", axis="columns", inplace=True)
    project.drop("length", axis="columns", inplace=True)
    project.Requirements = project.Requirements.apply(lambda x: [i.strip() for i in x])
    return project


def get_node(g: nx.DiGraph, edge_name: str) -> Union[int, None]:
    edges = nx.get_edge_attributes(g, 'name')
    for edge in edges:
        if edges[edge] == edge_name:
            return edge[1]
    return None
  
        
def create_graph(project: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_node(0)

    spares = []
    tasks = project.to_dict(orient='records')
    while True:
        for task in tasks:
            if len(task["Requirements"]) == 0:
                target_node = len(G.nodes)
                G.add_node(target_node)
                G.add_edge(0, target_node, name=task["ActivityID"], duration=task["Duration"])
            elif len(task["Requirements"]) == 1:
                root_node = get_node(G, task["Requirements"][0])
                if root_node is None:
                    spares.append(task)
                    continue
                target_node = len(G.nodes)
                G.add_node(target_node)
                G.add_edge(root_node, target_node, name=task["ActivityID"], duration=task["Duration"])
            else:
                reqs: list = task["Requirements"].copy()
                target_nodes = [get_node(G, r) if get_node(G, r) is not None else -1 for r in reqs]
                target_node = max(target_nodes)
                reqs.pop(target_nodes.index(target_node))
                
                if -1 in target_nodes:
                    spares.append(task)
                    continue
                root_nodes = target_nodes
                for root_node in root_nodes:
                    if (root_node, target_node) in G.edges or root_node == target_node:
                        continue
                    G.add_edge(root_node, target_node, name="Ø", duration=0)
                root_node = target_node
                target_node = len(G.nodes)
                G.add_node(target_node)
                G.add_edge(root_node, target_node, name=task["ActivityID"], duration=task["Duration"])
        
        if spares == []:
            break
        else:
            tasks = spares
            spares = []
            continue

    return G


def print_graph(G: nx.DiGraph) -> None:
    plt.figure(figsize=(20, 15))
    pos = nx.layout.shell_layout(G)
    node_colors = ['red' if node == 0 or node == len(G.nodes) - 1 else 'blue' for node in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_size=16, font_family="sans-serif", font_color='white')
    nx.draw_networkx_edge_labels(G, pos, font_size=12, font_family="sans-serif", edge_labels=nx.get_edge_attributes(G, "name"))
    plt.show()


def main(file_name: str) -> None:
    project = read_and_parse_file(file_name)
    print("File betöltve, feldolgozva")
    G = create_graph(project)
    print("Gráf generálva")
    # print(nx.is_directed_acyclic_graph(G))
    print_graph(G)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minimális méretű projektháló generátor © Orbán Gábor (github.com/GaborOrbanDev)")
    parser.add_argument("-f", "--file_name", action="store", help="Megadhatja a beolvasandó excel file nevét / elérési útját. \
                                                                    Alapértelmezett esetben a programmal egy mappában lévő \
                                                                    activity_input.xlsx filet fogja keresni")
    args = parser.parse_args()

    if args.file_name is not None:
        try:
            main(args.file_name)
        except Exception as ex:
            print(ex)
    else:
        try:
            main("activity_input.xlsx")
        except Exception as ex:
            print(ex)