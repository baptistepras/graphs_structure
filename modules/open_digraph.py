from typing import List, Dict, Tuple, Set, Union
from random import randint, sample, choice
import os
import sys
root = os.path.normpath(os.path.join(os.path.dirname(__file__)))
sys.path.append(root)  # allows us to fetch files from the project root


class Node:

    # Constructor
    def __init__(self, identity: int, label: str, parents: Dict[int, int], children: Dict[int, int]) -> None:
        """
        Constructs a new node object
        :param identity: int; its unique id in the graph
        :param label: string;
        :param parents: int->int dict; maps a parent nodes id to its multiplicity
        :param children: int->int dict; maps a child nodes id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    # Getters
    def get_id(self) -> int:
        """
        Returns node id
        """
        return self.id

    def get_label(self) -> str:
        """
        Returns node label
        """
        return self.label

    def get_parents(self) -> Dict[int, int]:
        """
        Returns node parents dict
        """
        return self.parents

    def get_children(self) -> Dict[int, int]:
        """
        Returns node children dict
        """
        return self.children

    # Setters
    def set_id(self, new_identity: int) -> None:
        """
        Changes node id
        :param new_identity: int; its unique id in the graph
        """
        self.id = new_identity

    def set_label(self, new_label: str) -> None:
        """
        Changes node label
        :param new_label: string;
        """
        self.label = new_label

    def set_children(self, new_children) -> None:
        """
        Changes node children dict
        :param new_children: int->int dict; maps a child nodes id to its multiplicity
        """
        self.children = new_children

    def add_parent_id(self, parent_id) -> None:
        """
        Adds a new parent to node parents dict
        :param parent_id: int;
        """
        if parent_id in self.get_parents():  # Already a parent
            self.parents[parent_id] += 1  # Increase the multiplicity
        else:  # Not yet a parent
            self.parents[parent_id] = 1

    def add_child_id(self, child_id):
        """
        Adds a new child to node children dict
        :param child_id: int;
        """
        if child_id in self.get_children():  # Already a child
            self.children[child_id] += 1  # Increase the multiplicity
        else:  # Not yet a child
            self.children[child_id] = 1

    # Printing methods
    def __str__(self) -> str:
        """
        Used by the __repr__ method
        """
        return f'({self.get_id()}, {self.get_label()}, {self.get_parents()}, {self.get_children()})'

    def __repr__(self) -> str:
        """
        Used to print the object
        """
        return str(self)

    # Methods
    def __eq__(self, other) -> bool:
        """
        Implementation of the "==" between two nodes
        :param other: Node;
        """
        return (self.get_id() == other.get_id() and self.get_label() == other.get_label() and
                self.get_parents() == other.get_parents() and self.get_children() == other.get_children())

    def copy(self):
        """
        Creates a copy of the node
        """
        return Node(self.get_id(), self.get_label(), self.get_parents(), self.get_children())

    def remove_parent_once(self, identity: int) -> None:
        """
        Removes an occurrence of the parent
        :param identity: int;
        """
        if identity in self.get_parents():
            if self.get_parents()[identity] <= 1:
                del self.parents[identity]
            else:
                self.parents[identity] -= 1

    def remove_child_once(self, identity: int) -> None:
        """
        Removes an occurrence of the child
        :param identity: int;
        """
        if identity in self.get_children():
            if self.get_children()[identity] <= 1:
                del self.children[identity]
            else:
                self.children[identity] -= 1

    def remove_parent_id(self, identity: int) -> None:
        """
        Removes a given parent
        :param identity: int;
        """
        if identity in self.get_parents():
            del self.parents[identity]

    def remove_child_id(self, identity: int) -> None:
        """
        Removes a given child
        :param identity: int;
        """
        if identity in self.get_children():
            del self.children[identity]

    def indegree(self) -> int:
        """
        Calculates the incoming degree of a node in the graph
        """
        return len(self.get_parents())

    def outdegree(self) -> int:
        """
        Calculates the outgoing degree of a node in the graph
        """
        return len(self.get_children())

    def degree(self) -> int:
        """
        Calculates the total degree of a node in the graph
        """
        return self.indegree() + self.outdegree()
        # return self.indegree() - self.outdegree()


class OpenDigraph:  # for open directed graph

    # Constructors
    def __init__(self, inputs: List[int] = None, outputs: List[int] = None, nodes: List[Node] = None) -> None:
        """
        Constructs a new OpenDigraph object
        No argument create an empty digraph
        :param inputs: int list; the ids of the input nodes
        :param outputs: int list; the ids of the output nodes
        :param nodes: node iter;
        """
        if inputs is None:
            self.inputs = []
        else:
            self.inputs = inputs

        if outputs is None:
            self.outputs = []
        else:
            self.outputs = outputs

        if nodes is None:
            self.nodes = {}
        else:
            self.nodes = {node.id: node for node in nodes}  # self.nodes: <int,node> dict

    @classmethod
    def empty(cls):
        """
        Creates an instance of the class with empty inputs, outputs, and nodes
        """
        return cls(inputs=[], outputs=[], nodes=[])

    # Getters
    def get_input_ids(self) -> List[int]:
        """
        Returns digraph input list
        """
        return self.inputs

    def get_output_ids(self) -> List[int]:
        """
        Returns digraph output list
        """
        return self.outputs

    def get_id_node_map(self) -> Dict[int, Node]:
        """
        Returns digraph nodes dictionnary
        """
        return self.nodes

    def get_nodes(self) -> List[Node]:
        """
        Returns a list of all the nodes
        """
        return list(self.nodes.values())

    def get_node_ids(self) -> List[int]:
        """
        Returns a list of all the ids
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, node_id: int) -> Node:
        """
        Returns a node given its id
        """
        return self.nodes[node_id]

    def get_nodes_by_ids(self, ids: List[int]) -> List[Node]:
        """
        Returns a list of nodes given a list of ids
        """
        return [self.nodes[node_id] for node_id in ids if node_id in self.nodes]

    # Setters
    def set_inputs(self, new_inputs: List[int]) -> None:
        """
        Changes digraph input list
        :param new_inputs: List[int];
        """
        nodes = self.get_node_ids()
        for i in new_inputs:
            if i not in nodes:  # An ID doesn't exist
                raise ValueError("A given ID doesn't exist")
                # We will also have to check that the graph is still well-formed later
        self.inputs = new_inputs

    def set_outputs(self, new_outputs: List[int]) -> None:
        """
        Changes digraph output list
        :param new_outputs: List[int];
        """
        nodes = self.get_node_ids()
        for i in new_outputs:
            if i not in nodes:  # An ID doesn't exist
                raise ValueError("A given ID doesn't exist")
                # We will also have to check that the graph is still well-formed later
        self.outputs = new_outputs

    def add_input_id(self, input_id: int) -> None:
        """
        Adds a new input to the input list
        :param input_id: int;
        """
        if input_id not in self.get_input_ids():  # Useless to add it twice
            if input_id in self.get_node_ids():  # Check that the ID exists
                self.inputs.append(input_id)
            else:
                ValueError("ID doesn't exist")  # We will also have to check that the graph is still well-formed later

    def add_output_id(self, output_id: int) -> None:
        """
        Adds a new input to the input list
        :param output_id: int;
        """
        if output_id not in self.get_output_ids():  # Useless to add it twice
            if output_id in self.get_node_ids():  # Check that the ID exists
                self.outputs.append(output_id)
            else:
                ValueError("ID doesn't exist")  # We will also have to check that the graph is still well-formed later

    # Printing methods
    def __str__(self) -> str:
        """
        Used by the __repr__ method
        """
        return f'({self.get_input_ids()}, {self.get_output_ids()}, {self.get_nodes()})'

    def __repr__(self) -> str:
        """
        Used to print the object
        """
        return str(self)

    # Methods
    def __eq__(self, other) -> bool:
        """
        Implementation of the "==" between two digraphs
        :param other: OpenDigraph;
        """
        return (self.get_input_ids() == other.get_input_ids() and self.get_output_ids() == other.get_output_ids()
                and self.get_nodes() == other.get_nodes())

    def copy(self):
        """
        Creates a copy of the graph
        """
        return OpenDigraph(list(self.get_input_ids()), list(self.get_output_ids()),
                           list(self.get_nodes_by_ids(self.get_node_ids())))

    def new_id(self):
        """
        Finds and return an unused ID in the graph
        """
        used_ids = set(self.get_input_ids() + self.get_output_ids() + list(self.get_node_ids()))
        return max(used_ids) + 1 if used_ids else 0  # If there's no existing id, return 0, else the max + 1
        # We suppose that if we have n ids, they all go from 0 to n-1
        # Still doesn't cause any problem if we don't have that condition
        # We'll just have ids not numerotated from 0 to n-1
        # But this function is faster (O(n)) than checking for the first unused id from 0 to n (O(n^2))

    def add_edge(self, src: int, tgt: int) -> None:
        """
        Adds an edge from the source node to the target node
        :param src: int; id of the source node
        :param tgt: int; id of the target node
        """
        nodes = self.get_node_ids()
        if src in nodes and tgt in nodes:
            self.get_node_by_id(src).add_child_id(tgt)  # Add a child to the source node
            self.get_node_by_id(tgt).add_parent_id(src)  # Add a parent to the target node
        else:
            raise ValueError("src or tgt doesn't exist")

    def add_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Adds edges between each pair of node IDs in the list of edges
        :param edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.add_edge(src, tgt)

    def remove_edge(self, src: int, tgt: int) -> None:
        """
        Removes an edge from the graph between the source node and the target node
        :param src: int; id of the source node
        :param tgt: int; id of the target node
        """
        nodes = self.get_node_ids()
        if src in nodes and tgt in nodes:
            self.get_node_by_id(tgt).remove_child_once(src)  # Remove a child of the source node
            self.get_node_by_id(src).remove_parent_once(tgt)  # Remove a parent of the target node
        else:
            raise ValueError("src or tgt doesn't exist")

    def remove_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Removes an edge between each pair of node IDs in the list of edges
        :param edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.remove_edge(src, tgt)

    def remove_parallel_edges(self, src: int, tgt: int) -> None:
        """
        Removes all edges from the graph between the source node and the target node
        :param src: int; id of the source node
        :param tgt: int; id of the target node
        """
        nodes = self.get_node_ids()
        if src in nodes and tgt in nodes:
            self.get_node_by_id(tgt).remove_parent_id(src)  # Remove all parents of the source node
            self.get_node_by_id(src).remove_child_id(tgt)  # Remove all children of the target node
        else:
            raise ValueError("src or tgt doesn't exist")

    def remove_several_parallel_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Removes all edges between each pair of node IDs in the list of edges
        :param edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.remove_parallel_edges(src, tgt)

    def add_node(self, label="", parents=None, children=None) -> int:
        """
        Adds a node with a label to the graph, assigning it a new id.
        Links it with the parent and child id nodes with their respective multiplicities.
        If the default values for parents and/or children are None, assign them an empty dictionary.
        Returns the id of the new node.
        :param label: string;
        :param parents: List[int]; ids of the parents
        :param children: List[int]; ids of the childrens
        """
        nodes = self.get_node_ids()
        # Create a new object Node
        new_node = Node(self.new_id(), label, {}, {})
        if parents is not None:
            for parent in parents:
                if parent in nodes:  # Check that the parent exists
                    new_node.add_parent_id(parent)
                else:
                    raise ValueError("One parent doesn't exist")
        if children is not None:
            for child in children:
                if child in nodes:  # Check that the child exists
                    new_node.add_child_id(child)
                else:
                    raise ValueError("One child doesn't exist")

        # Add the new node to the graph
        self.nodes[new_node.get_id()] = new_node

        return new_node.get_id()

    def add_input_node(self, node_id: int, child_id: int) -> None:
        """
        Adds a new input node to the graph and links it to the specified child node.
        :param node_id: int; id of the new input node
        :param child_id: int; id of the child node
        """
        # Asserts to keep the graph well-formed
        if node_id in self.get_node_ids():
            raise ValueError("Node already exists")
        if child_id not in self.get_node_ids():
            raise ValueError("Child doesn't exist")

        # Create a new input node with no parents and one child
        node = Node(node_id, "", {}, {})
        self.nodes[node_id] = node
        self.add_input_id(node_id)
        self.add_edge(node_id, child_id)

    def add_output_node(self, node_id: int, parent_id: int) -> None:
        """
        Adds a new output node to the graph and links it to the specified parent node.
        :param node_id: int; id of the new output node
        :param parent_id: int; id of the parent node
        """
        # Asserts to keep the graph well-formed
        if node_id in self.get_node_ids():
            raise ValueError("Node already exists")
        if parent_id not in self.get_node_ids():
            raise ValueError("Parent doesn't exist")

        # Create a new output node with one parent and no children
        node = Node(node_id, "", {}, {})
        self.nodes[node_id] = node
        self.add_output_id(node_id)
        self.add_edge(parent_id, node_id)

    def remove_id(self, identity: int) -> None:
        """
        Removes a node from its id
        :param identity: int; id of the node to remove
        """
        if identity in self.get_node_ids():

            parents = list(self.get_node_by_id(identity).get_parents().keys())
            children = list(self.get_node_by_id(identity).get_children().keys())
            for parent in parents:  # Remove all links with parents
                self.remove_parallel_edges(parent, identity)
            for child in children:  # Remove all links with children
                self.remove_parallel_edges(identity, child)
            self.nodes.pop(identity)

            inputs = self.get_input_ids()
            outputs = self.get_output_ids()
            if identity in inputs:  # Check if the node was an input
                self.set_inputs([node for node in inputs if node != identity])
            elif identity in outputs:  # Check if the node was an output
                self.set_inputs([node for node in outputs if node != identity])

    def remove_nodes_by_id(self, ids: List[int]) -> None:
        """
        Removes all nodes with IDs in the list of edges
        :param ids: list(int); list of nodes to remove
        """
        for identity in ids:
            self.remove_id(identity)

    def is_well_formed(self) -> bool:
        """
        Returns True if the graph is well-formed, else False
        """
        # Getters
        node_ids = self.get_node_ids()
        input_ids = self.get_input_ids()
        output_ids = self.get_output_ids()

        # Property 1: Check if each input and output node is in the graph
        for input_id in input_ids:  # inputs
            if input_id not in node_ids:
                return False
        for output_id in output_ids:  # outputs
            if output_id not in node_ids:
                return False

        # Property 2: Check if each input node has a single child and no parent
        for input_id in input_ids:
            input_node = self.get_node_by_id(input_id)
            children = input_node.get_children()
            parents = input_node.get_parents()
            if len(children) != 1 or len(parents) > 0:  # Wrong number of children or have parent(s)
                return False
            for child_multiplicity in children.values():  # At this step, it's exactly one value
                if child_multiplicity != 1:  # Wrong multiplicity
                    return False

        # Property 3: Check if each output node has a single parent and no children
        for output_id in output_ids:
            output_node = self.get_node_by_id(output_id)
            children = output_node.get_children()
            parents = output_node.get_parents()
            if len(children) > 0 or len(parents) != 1:  # Wrong number of parents or have child(ren)
                return False
            for parent_multiplicity in parents.values():  # At this step, it's exactly one value
                if parent_multiplicity != 1:    # Wrong multiplicity
                    return False

        # Property 4: Check if each key in nodes corresponds to a node which has the key as id
        for node_id, node in self.get_id_node_map().items():
            if node.get_id() != node_id:
                return False

        # Property 5: Check the relationship between parents and children
        for node_id, node in self.get_id_node_map().items():
            for child_id, multiplicity in node.get_children().items():  # child->parent
                child = self.get_node_by_id(child_id)
                parents = child.get_parents()
                if node_id not in parents or parents[node_id] != multiplicity:
                    return False
            for parent_id, multiplicity in node.get_parents().items():  # parent->child
                parent = self.get_node_by_id(parent_id)
                children = parent.get_children()
                if node_id not in children or children[node_id] != multiplicity:
                    return False

        return True

    def assert_is_well_formed(self) -> None:
        """
        Asserts if the graph is well-formed, raises an error if it's not
        """
        if not self.is_well_formed():
            raise ValueError("Graph not well-formed")
        
    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form="free") -> 'OpenDigraph':
        """
        Generates a random graph according to the constraints given by the user.
        :param n: int; number of nodes in the graph
        :param bound: int; maximum value for edge weights
        :param inputs: int; number of input nodes (if 0, randomly chosen)
        :param outputs: int; number of output nodes (if 0, randomly chosen)
        :param form: str; form of the graph
        :return: OpenDigraph; randomly generated graph
        """
        if inputs < 0 or outputs < 0 or n < inputs + outputs:
            raise ValueError("Invalid input/output values")

        # Generate adjacency matrix according to the specified form
        if form == "free":
            matrix = random_int_matrix(n, bound)
        elif form == "DAG":
            matrix = random_int_matrix(n, bound, dag=True)
        elif form == "oriented":
            matrix = random_int_matrix(n, bound, oriented=True)
        elif form == "loop-free":
            matrix = random_int_matrix(n, bound, null_diag=True)
        elif form == "undirected":
            matrix = random_int_matrix(n, bound, symmetric=True)
        elif form == "loop-free_undirected":
            matrix = random_int_matrix(n, bound, symmetric=True, null_diag=True)
        else:
            raise ValueError("Invalid graph form")

        # Create OpenDigraph instance from adjacency matrix
        graph = graph_from_adjacency_matrix(matrix)

        # Select inputs and outputs randomly (by checking for every node if it's a possible input/output node)
        node_ids = graph.get_node_ids()

        inputs_list = [i for i in node_ids if len(graph.get_node_by_id(i).get_parents()) == 0 and
                       len(graph.get_node_by_id(i).get_children()) == 1]
        if len(inputs_list) < inputs:
            raise ValueError("This graph has too few possibilities for inputs nodes")
        inputs_list = sample(node_ids, inputs)

        outputs_list = [i for i in node_ids if len(graph.get_node_by_id(i).get_children()) == 0 and
                        len(graph.get_node_by_id(i).get_parents()) == 1 and i not in inputs_list]
        if len(outputs_list) < outputs:
            raise ValueError("This graph has too few possibilities for outputs nodes")
        outputs_list = sample(node_ids, outputs)
        
        for node_id in inputs_list:
            graph.add_input_id(node_id)
        for node_id in outputs_list:
            graph.add_output_id(node_id)

        return graph
    
    def node_id_to_index_map(self) -> Dict[int, int]:
        """
        Returns a dictionary mapping each node ID to a unique integer index.
        The indices are in the range 0 ≤ i < n, where n is the number of nodes in the graph.
        :return: Dict[int, int];
        """
        node_ids = sorted(self.get_node_ids())  # Sort the node IDs
        node_index_map = {node_id: index for index, node_id in enumerate(node_ids)}  # Map each node ID to its index
        return node_index_map

    def adjacency_matrix(self) -> List[List[int]]:
        """
        Generates an adjacency matrix for the graph, ignoring inputs and outputs.
        Considers all nodes in the graph.
        :return: List[List[int]]; The adjacency matrix representing the connections between nodes.
        """
        # Get all nodes and their IDs
        nodes = self.get_nodes()
        node_ids = self.get_node_ids()
        
        # Initialize the adjacency matrix
        n = len(node_ids)
        adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        # Populate the adjacency matrix based on connections between nodes
        for node in nodes:
            node_id = node.get_id()
            children = node.get_children()
            for child_id, child_value in children.items():
                adj_matrix[node_id][child_id] = child_value  # Set the corresponding cell to 1
                
        return adj_matrix

    def save_as_dot_file(self, path, verbose=False) -> None:
        """
        Save the graph in .dot format at the specified path.
        :param path: str; the path where the .dot file will be saved
        :param verbose: bool; if True, includes both label and id for nodes
        """
        with open(path, 'w') as file:
            file.write("digraph G {\n")
            
            # Write nodes
            for node in self.get_nodes():
                label = node.get_label()
                if verbose:
                    label = f"{node.get_label()} (id: {node.get_id()})"
                file.write(f"v{node.get_id()} [label=\"{label}\"];\n")
            
            # Write edges
            for node in self.get_nodes():
                for child_id, multiplicity in node.get_children().items():
                    file.write(f"v{node.get_id()} -> v{child_id} [label=\"{multiplicity}\"];\n")
            
            file.write("}\n")
    
    @classmethod
    def from_dot_file(cls, path: str) -> 'OpenDigraph':
        """
        Construct an OpenDigraph from a .dot file.
        :param path: str; Path to the .dot file
        :return: OpenDigraph; An instance of OpenDigraph constructed from the .dot file
        """
        inputs = []
        outputs = []
        nodes = []
        
        with open(path, 'r') as file:
            lines = file.readlines()
        # Parse the lines to extract node information
            for line in lines:
                clean_line = line.strip()
                if clean_line.startswith("v"):
                    parts = clean_line.split('[label="')
                    node_id = parts[0].strip()
                    if node_id.isdigit():
                        node_id = int(node_id)
                    label_parts = parts[1].split('"')
                    if len(label_parts) > 1:
                        label = label_parts[1]
                    else:
                        label = None
                    if '"' in parts[1]:
                        verbose = True
                    else:
                        verbose = False
                    if verbose:
                        label += f" ({node_id})"
                    nodes.append(Node(identity=node_id, label=label, parents={}, children={}))

                elif "->" in clean_line:
                    parts = line.split('->')
                    src = int(parts[0].strip())
                    tgt = int(parts[1].split(';')[0].strip())
                    nodes[src - 1].add_child_id(tgt)
                    nodes[tgt - 1].add_parent_id(src)

        # Identify input and output nodes
        for node in nodes:
            if node.get_id() in node.get_parents():
                inputs.append(node.get_id())
            if node.get_id() in node.get_children():
                outputs.append(node.get_id())

        return cls(inputs=inputs, outputs=outputs, nodes=nodes)

    def display(self, verbose=False) -> None:
        """
        Displays the graph representation.
        :param verbose: bool; If True, includes both label and id for nodes in the graph
        """
        # Create a temporary location to store the .dot file
        dot_file = "temp_graph.dot"

        # Save the graph as a .dot file
        self.save_as_dot_file(dot_file, verbose)

        # Open the .dot file with a local viewer (assuming Graphviz is installed)
        os.system(f"dot -Tpdf {dot_file} -o temp_graph.pdf")
        os.system("xdg-open temp_graph.pdf")  # For Linux, opens the PDF file with the default viewer

        # Remove temporary files
        os.remove(dot_file)
        os.remove("temp_graph.pdf")

    def is_cyclic(self) -> bool:
        """
        Checks if the directed graph contains a cycle using depth-first search (DFS).
        Returns True if the graph has a cycle, otherwise False.
        :return: bool;
        """

        # Helper function for DFS traversal
        def dfs_util(node_id, v, s):
            v[node_id] = True
            s[node_id] = True

            # Recur for all neighbors
            for neighbor_id in self.get_node_by_id(node_id).get_children():
                if not v[neighbor_id]:
                    if dfs_util(neighbor_id, v, s):
                        return True
                elif s[neighbor_id]:
                    return True

            s[node_id] = False
            return False

        # Initialize visited and recursion stack
        visited = {node_id: False for node_id in self.get_node_ids()}
        stack = {node_id: False for node_id in self.get_node_ids()}

        # Perform DFS for each node in the graph
        for node_id in self.get_node_ids():
            if not visited[node_id]:
                if dfs_util(node_id, visited, stack):
                    return True

        return False

    def min_id(self) -> int:
        """
        Returns the minimum index of the graph nodes
        :return: int; minimum index
        """
        min_index = float('inf')
        for node in self.get_nodes():
            if node.id < min_index:
                min_index = node.id
        return min_index

    def max_id(self) -> int:
        """
        Returns the maximum index of the graph nodes
        :return: int; maximum index
        """
        max_index = float('-inf')
        for node in self.get_nodes():
            if node.id > max_index:
                max_index = node.id
        return max_index

    def shift_indices(self, n: int) -> None:
        """
        Shifts all indices in the graph by adding integer n (possibly negative)
        :param n: int; integer to be added to all indices
        """
        # Input list
        new_input = []
        for i in self.get_input_ids():
            new_input.append(i + n)
        self.inputs = new_input

        # Output list
        new_output = []
        for i in self.get_output_ids():
            new_output.append(i + n)
        self.outputs = new_output

        # ID, parents and children list for each node
        for node in self.get_nodes():
            node.id += n

            # Parents
            new_parents = {}
            for i in node.get_parents():
                new_parents[i + n] = node.parents[i]
            node.parents = new_parents

            # Children
            new_children = {}
            for i in node.get_children():
                new_children[i + n] = node.children[i]
            node.children = new_children

    def iparallel(self, g) -> None:
        """
        Appends the graph g to self in parallel without modifying g.
        :param g: OpenDigraph; the graph to be appended in parallel
        """
        # Find the maximum index in self and the minimum index in g
        max_self_index = self.max_id()
        min_g_index = g.min_id()

        # Translate the indices of g by max_self_index - min_g_index + 1
        m = max_self_index - min_g_index + 1
        g_copy = g.copy()
        if m > 0:
            g_copy.shift_indices(m)

        # Add the nodes and connections of g to self
        for node in g_copy.get_input_ids():
            self.inputs.append(node)
        for node in g_copy.get_output_ids():
            self.outputs.append(node)
        for node in g_copy.get_node_ids():
            self.nodes[node] = g_copy.nodes[node]

    def parallel(self, g1, g2) -> None:
        """
        Returns a new graph which is the parallel composition of g1 and g2 without modifying them.
        :param g1: OpenDigraph; the first graph
        :param g2: OpenDigraph; the second graph
        """
        # Find the maximum index in self and the minimum index in g
        max_g1_index = g1.max_id()
        min_g2_index = g2.min_id()

        # Translate the indices of g by max_self_index - min_g_index + 1
        m = max_g1_index - min_g2_index + 1
        g2_copy = g2.copy()
        if m > 0:
            g2_copy.shift_indices(m)

        # Add the nodes and connections of g1 to the new graph
        for node in g1.get_input_ids():
            self.inputs.append(node)
        for node in g1.get_output_ids():
            self.outputs.append(node)
        for node in g1.get_node_ids():
            self.nodes[node] = g1.nodes[node]

        # Add the nodes and connections of g2 to the new graph
        for node in g2_copy.get_input_ids():
            self.inputs.append(node)
        for node in g2_copy.get_output_ids():
            self.outputs.append(node)
        for node in g2_copy.get_node_ids():
            self.nodes[node] = g2_copy.nodes[node]

    def icompose(self, f) -> None:
        """
        Performs the sequential composition of self and f.
        The inputs of self should be connected to the outputs of f.
        :param f: OpenDigraph; the graph to be composed sequentially with self
        """
        # Check that the number of outputs of f = the number of inputs of self
        if len(self.get_input_ids()) != len(f.get_output_ids()):
            raise ValueError("Number of outputs from f doesn't match the number of inputs of self.")

        # Find the maximum index in self and the minimum index in g
        max_self_index = self.max_id()
        min_f_index = f.min_id()

        # Translate the indices of g by max_self_index - min_g_index + 1
        m = max_self_index - min_f_index + 1
        f_copy = f.copy()
        if m > 0:
            f_copy.shift_indices(m)

        # Add the nodes of f to self
        for node in f_copy.get_node_ids():
            self.nodes[node] = f_copy.nodes[node]

        # Connect outputs of f to inputs of self
        inputs = self.get_input_ids()
        outputs = f_copy.get_output_ids()
        for i in range(len(f.outputs)):
            self.get_node_by_id(inputs[i]).add_parent_id(outputs[i])
            self.get_node_by_id(outputs[i]).add_child_id(inputs[i])

        # New inputs are inputs of f
        self.inputs = f_copy.get_input_ids()

    def compose(self, f1, f2) -> None:
        """
        Returns a third graph, which is the composition of f1 and f2, without modifying them.
        :param f1: OpenDigraph; the first graph
        :param f2: OpenDigraph; the second graph
        """
        # Check that the number of outputs of f = the number of inputs of self
        if len(f1.get_input_ids()) != len(f2.get_output_ids()):
            raise ValueError("Number of outputs from f1 doesn't match the number of inputs of f2.")

        # Find the maximum index in self and the minimum index in g
        max_f1_index = f1.max_id()
        min_f2_index = f2.min_id()

        # Translate the indices of g by max_self_index - min_g_index + 1
        m = max_f1_index - min_f2_index + 1
        f2_copy = f2.copy()
        if m > 0:
            f2_copy.shift_indices(m)

        # Add the nodes of f1 to self
        for node in f1.get_node_ids():
            self.nodes[node] = f1.nodes[node]
        # Add the nodes of f2 to self
        for node in f2_copy.get_node_ids():
            self.nodes[node] = f2_copy.nodes[node]

        # Connect outputs of f2 to inputs of f1
        inputs = f1.get_input_ids()
        outputs = f2_copy.get_output_ids()
        for i in range(len(f2.get_output_ids())):
            self.get_node_by_id(inputs[i]).add_parent_id(outputs[i])
            self.get_node_by_id(outputs[i]).add_child_id(inputs[i])

        # New inputs are inputs of f2
        self.inputs = f2_copy.get_input_ids()
        # New outputs are outputs of f1
        self.outputs = f1.get_output_ids()

    @classmethod
    def identity(cls, n: int) -> 'OpenDigraph':
        """
        Creates an open_digraph representing the identity over n children.
        :param n: int; number of children
        :return: OpenDigraph; the idendity over n children graph
        """
        t = [i for i in range(n)]
        nodes = [Node(identity=i, label='&', parents={}, children={}) for i in range(n)]

        # Connect each node to itself
        for i in range(n):
            nodes[i].add_child_id(i)
            nodes[i].add_parent_id(i)

        return cls(inputs=t, outputs=t, nodes=nodes)

    def connected_components(self) -> Tuple[int, Dict[int, int], List['OpenDigraph']]:
        """
        Returns the number of connected components of the graph and a dictionary
        associating each node id with the number of the connected component it belongs to,
        plus a list of all components
        :return: Tuple[int, Dict[int, int], List[OpenDigraph]]; number of connected components, a
                 dictionary mapping node IDs to their connected component number,
                 and a list of OpenDigraph, each corresponding to a component
        """
        visited = set()
        dic = {}
        cpt = 0
        nodes = self.get_nodes()

        # Helper function for DFS traversal
        def dfs_util(node_id):
            if node_id in visited:
                return  # Node already visited
            visited.add(node_id)
            dic[node_id] = cpt

            # Explore all children of the current node
            for child_id in nodes[node_id].get_children():
                dfs_util(child_id)

            # Explore all parents of the current node
            for parent_id in nodes[node_id].get_parents():
                dfs_util(parent_id)

        # Start DFS for each node that is still unmarked
        for node in nodes:
            if node.get_id() not in visited:
                dfs_util(node.get_id())
                cpt += 1

        # Recreate all components
        res = []
        components = [i for i in range(cpt)]
        self_nodes = self.get_nodes()

        for component in components:
            # Get the nodes of the current component
            nodes = {i: self_nodes[i] for i in self.get_node_ids() if dic[i] == component}

            # Create new node IDs
            new_ids = {old_id: new_id for new_id, old_id in enumerate(sorted(nodes.keys()))}

            # Create new inputs and outputs
            new_inputs = [new_ids[i] for i in self.get_input_ids() if i in nodes]
            new_outputs = [new_ids[i] for i in self.get_output_ids() if i in nodes]

            # Create new nodes with news IDs and their respective connections
            new_nodes = []
            for old_id in nodes:
                new_id = new_ids[old_id]
                parents = nodes[old_id].get_parents()
                children = nodes[old_id].get_children()
                new_parents = {new_ids[i]: parents[i] for i in parents if i in new_ids}
                new_children = {new_ids[i]: children[i] for i in children if i in new_ids}
                new_nodes.append(Node(new_id, nodes[old_id].get_label(), new_parents, new_children))

            # Add the new subgraph
            res.append(OpenDigraph(new_inputs, new_outputs, new_nodes))

        return cpt, dic, res

    @staticmethod
    def min_distance(dist, q):
        min_dist = float('inf')
        min_node = None
        for node in q:
            if dist[node] < min_dist:
                min_dist = dist[node]
                min_node = node
        return min_node

    def dijkstra(self, src: int, direction=None, tgt=None) -> Tuple[Dict[int, int], Dict[int, int]]:
        """
        Implements Dijkstra algorithm for the graph,
        Returns a dictionary, which for each node, calculates the total distance to the source
        and one giving the previous nodes to go from src to the node
        :param src: int; the id of the source node
        :param direction: int; if None, go through parents and children
                               if -1 only the parents
                               if 1 only the children
        :param tgt: int; the id of the target node to stop early if found
        :return: Tuple[Dict[int, int], Dict[int, int]];
                 the dictionary mapping each node id to its distance from the source
                 and the one giving the previous node ids in the shortest path
        """
        # Stocke les noeuds que nous pouvons parcourir, en fonction de la direction
        q = [src]
        dist = {src: 0}
        prev = {}

        # Algorithme de Dijkstra
        while len(q) > 0:
            u = self.min_distance(dist, q)

            if u == tgt:
                return dist, prev

            if direction is None:
                neighbors = self.get_node_by_id(u).get_children()
                parents = self.get_node_by_id(u).get_parents()
                for p in parents:
                    neighbors[p] = parents[p]

            elif direction == -1:
                neighbors = self.get_node_by_id(u).get_parents()

            elif direction == 1:
                neighbors = self.get_node_by_id(u).get_children()

            else:
                raise ValueError("La direction doit être None, -1 ou 1")

            for v in neighbors:
                if v not in dist:
                    q.append(v)
                    dist[v] = float('inf')
                if dist[v] > dist[u] + 1:  # Ne tient pas compte du poids des arêtes
                    dist[v] = dist[u] + 1
                    prev[v] = u

            q.remove(u)

        return dist, prev

    def shortest_path(self, u, v):
        dist, prev = self.dijkstra(u, None, v)
        nodes = [v]
        while v != u:
            v = prev[v]
            nodes.insert(0, v)
        return nodes
        
    def common_ancestors_distances(self, node1_id: int, node2_id: int) -> Dict[int, Tuple[int, int]]:
        """
        Returns a dictionary associating each common ancestor of the two nodes with its distance
        from each of the two nodes.
        :param node1_id: int; ID of the first node
        :param node2_id: int; ID of the second node
        :return: Dict[int, Tuple[int, int]]; dictionary with common ancestor IDs
                                             as keys and distances from both nodes as values
        """
        # Perform Dijkstra's algorithm from both nodes
        dist1, prev1 = self.dijkstra(node1_id)
        dist2, prev2 = self.dijkstra(node2_id)

        # Find common ancestors
        common_ancestors = set(prev1.keys()) & set(prev2.keys())

        # Calculate distances from both nodes to common ancestors
        common_ancestors_distances = {}
        for ancestor in common_ancestors:
            distance_from_node1 = dist1[ancestor]
            distance_from_node2 = dist2[ancestor]
            common_ancestors_distances[ancestor] = (distance_from_node1, distance_from_node2)

        return common_ancestors_distances
    
    def topological_sort(self) -> Union[List[Set[int]], str]:
        """
        Performs a topological sort on the graph and returns a sequence of sets representing the sort.
        If the graph is cyclic, returns an error message.
        :return: Union[List[Set[int]], str]; sequence of sets
        """
        # Initialize result list
        topological_sequence = []

        # Initialize set of nodes with no parents (co-leaves)
        co_leaves = set(self.get_input_ids())

        # Perform topological sort
        while co_leaves:
            current_set = set()

            # Find co-leaves
            new_co_leaves = set()
            for node_id in co_leaves:
                current_set.add(node_id)
                for child_id in self.get_node_by_id(node_id).get_children():
                    if all(parent_id not in current_set for parent_id in self.get_node_by_id(child_id).get_parents()):
                        new_co_leaves.add(child_id)

            # If there are no new co-leaves but the graph is not empty, it's cyclic
            if not new_co_leaves and len(current_set) < len(self.get_node_ids()):
                raise ValueError("Graph is cyclic")

            # Add current set to the topological sequence
            topological_sequence.append(current_set)
            co_leaves = new_co_leaves

        return topological_sequence
    
    def graph_depth(self) -> int:
        """
        Calculates the depth of the graph, which is the number of sets in the topological sort.
        :return: int; depth of the graph
        """
        topological_sequence = self.topological_sort()
        if isinstance(topological_sequence, str):
            return 0  # Graph is cyclic, depth is 0
        else:
            return len(topological_sequence)

    @staticmethod
    def node_depth(node_id: int, topological_sort: List[Set[int]]) -> int:
        """
        Returns the depth of a given node in the graph based on the provided topological sort.
        :param node_id: int; id of the node
        :param topological_sort: List[Set[int]]; result of the topological sort
        :return: int; the depth of the node
        """
        for i, node_set in enumerate(topological_sort):
            if node_id in node_set:
                return i
        raise ValueError(f"Node {node_id} not found in the provided topological sort.")

    def longest_path(self, u: int, v: int, topological_sort: List[Set[int]]) -> Tuple[int, List[int]]:
        """
        Calculates the longest path from node u to node v in the graph using topological sorting.
        :param u: int; source node
        :param v: int; target node
        :param topological_sort: List[Set[int]]; result of the topological sort
        :return: Tuple[int, List[int]]; distance of the longest path and longest path itself
        """
        # Initialize distances and previous nodes
        dist = {node_id: -float('inf') for node_set in topological_sort for node_id in node_set}
        prev = {node_id: None for node_set in topological_sort for node_id in node_set}

        # Initialize distance of source node u to 0
        dist[u] = 0

        # Iterate through topological sort
        for node_set in topological_sort:
            for node_id in node_set:
                if node_id == v:
                    return dist[v], self.reconstruct_path(prev, v)
                for parent_id in self.nodes[node_id].get_parents():
                    if dist[parent_id] + 1 > dist[node_id]:
                        dist[node_id] = dist[parent_id] + 1
                        prev[node_id] = parent_id

    @staticmethod
    def reconstruct_path(prev: dict, v: int) -> List[int]:
        """
        Reconstructs the longest path from node u to node v based on the previous nodes.
        :param prev: dict; dict of the previous nodes
        :param v: int; current target node
        :return; List[int]; the path needed
        """
        path = []
        current = v
        while current is not None:
            path.insert(0, current)
            current = prev[current]
        return path

    def max_path_and_distance(self, u: int, v: int) -> Tuple[List[int], int]:
        """
        Calculates the maximum path and distance from node u to node v in the graph.
        :param u: int; source node
        :param v: int; target node
        :return: Tuple[List[int], int]; maximum path and distance
        """
        # Initialize distances and previous nodes
        dist = {node_id: -float('inf') for node_id in self.nodes}
        prev = {node_id: None for node_id in self.nodes}

        # Initialize distance of source node u to 0
        dist[u] = 0

        # Initialize maximum distance encountered and the node that leads to that distance
        max_distance = -float('inf')

        # Iterate through the graph using Dijkstra's algorithm
        for _ in range(len(self.nodes)):
            u = max(dist, key=dist.get)  # Node with maximum distance
            if u == v:
                break  # Reached target node v
            if dist[u] == -float('inf'):
                break  # Unreachable nodes remaining

            for v in self.nodes[u].get_children():
                if dist[u] + 1 > dist[v]:
                    dist[v] = dist[u] + 1
                    prev[v] = u
                    if dist[v] > max_distance:
                        max_distance = dist[v]

            del dist[u]  # Remove processed node from distances

        # Reconstruct the maximum path
        path = []
        current = v
        while current is not None:
            path.insert(0, current)
            current = prev[current]

        return path, max_distance

    def merge_nodes(self, node_id1: int, node_id2: int, label: str = None) -> int:
        """
        Merges two nodes in the graph by combining their attributes and edges.
        :param node_id1: int; ID of the first node to merge
        :param node_id2: int; ID of the second node to merge
        :param label: str; optional label for the merged node
        :return: int; ID of the merged node
        """
        # Ensure that both nodes exist in the graph
        nodes = self.nodes
        if node_id1 not in nodes or node_id2 not in nodes:
            raise ValueError("Node IDs must be valid nodes in the graph")

        # Choose the label for the merged node
        if label is None:
            self.nodes[node_id1].label = self.nodes[node_id1].label
        else:
            self.nodes[node_id1].label = label

        # Transfer edges from node2 to node1
        for child_id in self.nodes[node_id2].children:
            self.nodes[node_id1].add_child_id(child_id)
            self.nodes[child_id].add_parent_id(node_id1)

        for parent_id in self.nodes[node_id2].parents:
            self.nodes[node_id1].add_parent_id(parent_id)
            self.nodes[parent_id].add_child_id(node_id1)

        # Remove node2 from the graph
        del self.nodes[node_id2]

        return node_id1


class BoolCirc(OpenDigraph):
    # Constructors
    def __init__(self, g=OpenDigraph(), test=False) -> None:
        """
        Constructs a new BoolCirc object
        :param g: OpenDigraph; the associated open graph
        :param test: bool; True if we are testing the constructor (prevent the ValueError)
        """
        super().__init__()  # Initialize the superclass
        self.g = g
        if not test:
            if not(self.is_well_formed()):
                raise ValueError("BoolCirc isn't well-formed")

    # Methods
    def is_well_formed(self) -> bool:
        """
        Checks if a BoolCirc is well-formed or not
        :return: bool: True if it is well-formed, otherwise False
        """
        # List of allowed primitive operations
        allowed_primitives = {'0', '1', '~', '|', '&', '^'}

        # Check each node validity
        for node in self.g.get_nodes():
            label = node.get_label()
            if label == '':
                if node.indegree() != 1:
                    return False
            elif label not in allowed_primitives:
                return False  # Unknown type of node

        # Check if the graph itself is well-formed and acyclic
        return self.g.is_well_formed() and not self.g.is_cyclic()

    '''
    def parse_parentheses(self, s: str) -> None:
        """
        Session 9.1)
        Parses a propositional formula in completely parenthesized form and constructs a boolean circuit tree.
        :param s: str; the propositional formula in infix notation
        """
        current_node_id = self.max_id() + 1  # Start with a new node ID

        s2 = ''
        for char in s:
            if char == '(':
                # Add s2 to the label of the current node
                self.get_node_by_id(current_node_id).label += s2

                # Create a parent of current_node and make it current_node
                parent_node_id = self.max_id() + 1
                self.nodes[parent_node_id] = Node(identity=parent_node_id, label='', parents={}, children={})
                self.get_node_by_id(parent_node_id).add_child_id(current_node_id)
                self.get_node_by_id(current_node_id).add_parent_id(parent_node_id)
                current_node_id = parent_node_id
                s2 = ''

            elif char == ')':
                # Add s2 to the label of current_node
                self.get_node_by_id(current_node_id).label += s2

                # Change current_node so that it becomes its child
                current_node_id = self.get_node_by_id(current_node_id).get_parents().popitem()[0]
                s2 = ''

            else:
                # Add char to the end of s2
                s2 += char

        # Add the remaining characters in s2 to the label of the current node
        self.get_node_by_id(current_node_id).label += s2
    '''

    def parse_parentheses(self, s: str) -> Tuple['BoolCirc', List[str]]:
        """
        Session 9.3)
        Parses a propositional formula, merges nodes, and constructs a boolean circuit tree.
        :param s: str; the propositional formula in infix notation
        :return: Tuple[BoolCirc, List[str]]; the boolean circuit and list of variable names
        """
        current_node_id = self.max_id() + 1  # Start with a new node ID
        parent_node_id = self.max_id() + 2
        s2 = ''
        variables = []

        for char in s:
            if char == '(':
                # Add s2 to the label of the current node
                self.nodes[current_node_id].label += s2

                # Create a parent of current_node and make it current_node
                parent_node_id = self.max_id() + 1
                self.nodes[parent_node_id] = Node(identity=parent_node_id, label='', parents={}, children={})
                self.nodes[parent_node_id].add_child_id(current_node_id)
                self.nodes[current_node_id].add_parent_id(parent_node_id)
                current_node_id = parent_node_id
                s2 = ''

            elif char == ')':
                # Add s2 to the label of current_node
                self.nodes[current_node_id].label += s2

                # Change current_node so that it becomes its child
                current_node_id = list(self.nodes[current_node_id].parents)[0]
                s2 = ''

            elif char.isalpha():
                # Add char to variables if it's not already there
                if char not in variables:
                    variables.append(char)

                # Add char to the end of s2
                s2 += char

            elif char == ' ':
                # Merge nodes if s2 represents a variable
                if s2.isalpha():
                    self.merge_nodes(parent_node_id, current_node_id)
                    current_node_id = list(self.nodes[parent_node_id].parents)[0]
                    s2 = ''
                else:
                    s2 += char

        # Add the remaining characters in s2 to the label of the current node
        self.nodes[current_node_id].label += s2

        return self, variables

    @staticmethod
    def parse_parentheses_multiple(*args: str) -> 'BoolCirc':
        """
        Session 9.4)
        Parses multiple propositional formulas and constructs a single boolean circuit that implements the sequence.
        :param args: str; sequence of propositional formulas
        :return: BoolCirc; the boolean circuit implementing the sequence
        """
        circuits = []  # List to store individual circuits for each formula
        merged_circuit = BoolCirc()  # Initialize the merged circuit

        for formula in args:
            # Parse each formula and obtain the boolean circuit
            circuit, _ = merged_circuit.parse_parentheses(formula)
            circuits.append(circuit)

        # Combine circuits side by side
        for circuit in circuits:
            # Connect the outputs of the current circuit to the inputs of the merged circuit
            output_id = list(circuit.nodes.keys())[-1]  # Get the output node ID of the current circuit
            input_id = merged_circuit.max_id() + 1  # Get the next available ID in the merged circuit

            # Add the output node of the current circuit as a child of the input node of the merged circuit
            merged_circuit.nodes[input_id] = Node(identity=input_id, label='', parents={}, children={})
            merged_circuit.nodes[input_id].add_child_id(output_id)
            merged_circuit.nodes[output_id].add_parent_id(input_id)

        return merged_circuit

    def random_bool_circ(self, unary_operators: str, binary_operators: str, inputs: int, outputs: int) -> None:
        """
        Creates a random bool circ with specified number of inputs and outputs
        :param unary_operators: str; list of unary operators
        :param binary_operators: str; list of binary operators
        :param inputs: int; number of inputs
        :param outputs: int; number of outputs
        """
        # Label the nodes based on their in-degree and out-degree
        for node in self.g.get_node_ids():
            indegree = self.g.get_node_by_id(node).indegree()
            outdegree = self.g.get_node_by_id(node).outdegree()

            if indegree == outdegree == 1:
                # Assign unary operator
                self.g.get_node_by_id(node).set_label(choice(unary_operators))

            elif indegree == 1 and outdegree > 1:
                # Do nothing, node represents a copy
                pass

            elif indegree > 1 and outdegree == 1:
                # Assign binary operator
                self.g.get_node_by_id(node).set_label(choice(binary_operators))

            elif indegree > 1 and outdegree > 1:
                # Split the node into two nodes
                new_node1 = len(self.g.get_nodes())
                new_node2 = len(self.g.get_nodes()) + 1
                self.g.get_node_by_id(new_node1).set_label(choice(binary_operators))
                self.g.get_node_by_id(new_node2).set_label("")

                for parent in self.g.get_node_ids():
                    self.g.get_node_by_id(parent).remove_parent_id(node)
                    self.g.get_node_by_id(parent).add_parent_id(new_node1)

                for child in self.g.get_node_ids():
                    self.g.get_node_by_id(child).remove_child_id(node)
                    self.g.get_node_by_id(new_node2).add_child_id(child)

                self.g.get_node_by_id(new_node2).set_label("")

        # Add inputs and outputs if necessary
        node_ids = self.get_node_ids()
        inputs_list = [i for i in node_ids if len(self.g.get_node_by_id(i).get_parents()) == 0 and
                       len(self.g.get_node_by_id(i).get_children()) == 1]
        if len(inputs_list) < inputs:
            raise ValueError("This graph has too few possibilities for inputs nodes")
        inputs_list = sample(node_ids, inputs)

        outputs_list = [i for i in node_ids if len(self.g.get_node_by_id(i).get_children()) == 0 and
                        len(self.g.get_node_by_id(i).get_parents()) == 1 and i not in inputs_list]
        if len(outputs_list) < outputs:
            raise ValueError("This graph has too few possibilities for outputs nodes")
        outputs_list = sample(node_ids, outputs)

        for node_id in inputs_list:
            self.g.add_input_id(node_id)
        for node_id in outputs_list:
            self.g.add_output_id(node_id)

    def half_adder(self, n: int) -> None:
        """
        Constructs a Boolean Half-Adder circuit for a register of size 2^n.
        :param n: int; size of the register
        """
        if n == 0:
            # Base case: Constructing the Half-Adder for a register of size 1
            self.parse_parentheses("~a ~b Addern 0 :=")
        else:
            # Recursive construction of the Half-Adder
            self.half_adder(n - 1)
            self.parse_parentheses(f"Addern 0 := {n - 1} p")

    def adder(self, n: int) -> None:
        """
        Constructs a Boolean Adder circuit for a register of size 2^n.
        :param n: int; size of the register
        """
        if n == 0:
            # Base case: Constructing the Adder for a register of size 1
            self.parse_parentheses("~a ~b Addern 0 :=")
        else:
            # Recursive construction of the Adder
            self.adder(n - 1)
            self.parse_parentheses(f"Addern {n} 0 := {n - 1} p")

    def carry_lookahead_adder_4(self) -> None:
        """
        Constructs a Carry-Lookahead Adder for registers of size 4.
        :return: BoolCirc; the constructed Carry-Lookahead Adder circuit
        """
        self.adder(4)

    def carry_lookahead_adder(self, n: int) -> None:
        """
        Constructs a Carry-Lookahead Adder for registers of size 4n.
        :param n: int; size of the register 4n
        """
        if not n % 4 and n > 0:
            raise ValueError("n must be a multiple of 4")

        if n == 0:
            # Base case: Constructing the Adder for a register of size 1
            self.carry_lookahead_adder_4()
        else:
            # Recursive construction of the Adder
            self.carry_lookahead_adder(n-1)
            self.carry_lookahead_adder_4()

    def int_to_register_circuit(self, number: int, register_size: int) -> None:
        """
        Creates a Boolean circuit representing the given integer instantiated in a register
        :param number: int; the integer value to be represented.
        :param register_size: int; the size of the register (number of bits). Default is 8
        """
        # Convert the integer to binary representation
        binary_str = bin(number)[2:]

        # Pad the binary string with leading zeros if necessary
        padded_binary_str = binary_str.zfill(register_size)

        # Create nodes for each bit of the binary representation
        for bit in padded_binary_str:
            self.g.add_node(bit)

        # Connect the nodes in the circuit to represent the binary value
        for i in range(register_size - 1):
            self.g.add_edge(int(padded_binary_str[i]), int(padded_binary_str[i + 1]))

    def rule_not(self) -> None:
        """
        Applies transformation for NOT gates: ~0 -> 1, ~1 -> 0
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.get_label() == '∼':
                pred = node.get_parents()[0]
                pred_label = self.g.nodes[pred].get_label()
                if pred_label == '0':
                    self.g.nodes[node_id].set_label('1')
                elif pred_label == '1':
                    self.g.nodes[node_id].set_label('0')
                self.g.remove_edge(pred, node_id)

    def rule_and(self) -> None:
        """
        Applies transformation for AND gates: 0 & x -> 0, x & 0 -> 0, 1 & x -> x, x & 1 -> x
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.get_label() == '&':
                inputs = [self.g.nodes[n].get_label() for n in node.get_parents()]
                if '0' in inputs:
                    self.g.nodes[node_id].set_label('0')
                elif '1' in inputs:
                    inputs.remove('1')
                    self.g.nodes[node_id].set_label(inputs[0])
                for pred in node.get_parents():
                    self.g.remove_edge(pred, node_id)

    def rule_or(self) -> None:
        """
        Applies transformation for OR gates: 0 | x -> x, x | 0 -> x, 1 | x -> 1, x | 1 -> 1
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.get_label() == '|':
                inputs = [self.g.nodes[n].get_label() for n in node.get_parents()]
                if '1' in inputs:
                    self.g.nodes[node_id].set_label('1')
                elif '0' in inputs:
                    inputs.remove('0')
                    self.g.nodes[node_id].set_label(inputs[0])
                for pred in node.get_parents():
                    self.g.remove_edge(pred, node_id)

    def rule_xor(self) -> None:
        """
        Applies transformation for XOR gates and neutral elements: 0 ˆ x -> x, x ˆ 0 -> x, 1 ˆ x -> ~x, x ˆ 1 -> ~x
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.get_label() == 'ˆ':
                inputs = [self.g.nodes[n].get_label() for n in node.get_parents()]
                if '0' in inputs:
                    inputs.remove('0')
                    self.g.nodes[node_id].set_label(inputs[0])
                elif '1' in inputs:
                    inputs.remove('1')
                    self.g.nodes[node_id].set_label('∼' + inputs[0])
                for pred in node.get_parents():
                    self.g.remove_edge(pred, node_id)

    def evaluate_rule_neutral(self) -> None:
        """
        Applies transformation for neutral elements in OR gates: x | ~x -> 1, ~x | x -> 1
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.get_label() == '|':
                inputs = [self.g.nodes[n].get_label() for n in node.get_parents()]
                if len(inputs) == 2 and '∼' + inputs[0] == inputs[1]:
                    self.g.nodes[node_id].set_label('1')
                elif len(inputs) == 2 and '∼' + inputs[1] == inputs[0]:
                    self.g.nodes[node_id].set_label('1')
                for pred in node.get_parents():
                    self.g.remove_edge(pred, node_id)

    def rule_copy(self) -> None:
        """
        Applies transformation for copying without output: x -> x, x | x -> x
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.indegree() == 1 and node.outdegree() == 0:
                pred = node.get_parents()[0]
                self.g.nodes[node_id].set_label(self.g.nodes[pred].get_label())
                self.g.remove_edge(pred, node_id)

    def rule_erase(self) -> None:
        """
        Applies transformation for erasing a node with a unary operator.
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.indegree() == 1 and node.outdegree() == 1:
                pred = node.get_parents()[0]
                self.g.add_edge(pred, node.get_parents()[0])
                self.g.remove_id(node_id)

    def rule_involution(self) -> None:
        """
        Applies transformation for involution of XOR gates with more than two inputs.
        """
        node_ids = self.g.get_node_ids()
        for node_id in node_ids:
            node = self.g.nodes[node_id]
            if node.get_label() == 'ˆ' and node.indegree() > 2:
                inputs = [self.g.nodes[n] for n in node.get_parents()]
                even_inputs = inputs[::2]
                odd_inputs = inputs[1::2]
                for i in range(len(even_inputs)):
                    self.g.add_node('ˆ')
                    self.g.add_edge(even_inputs[i].get_id(), len(self.g.nodes) - 1)
                    self.g.add_edge(odd_inputs[i].get_id(), len(self.g.nodes) - 1)
                    if i == len(even_inputs) - 1 and len(odd_inputs) > len(even_inputs):
                        self.g.add_edge(odd_inputs[-1].get_id(), len(self.g.nodes) - 1)

    def evaluate(self):
        """
        Applies transformation rules iteratively until there are no more transformations to apply.
        """
        # Set to keep track of nodes directly connected to an output
        output_nodes: Set[int] = set()
        for node_id in self.g.get_node_ids():
            if self.g.nodes[node_id].outdegree() == 0:
                output_nodes.add(node_id)

        # Loop until there are no more transformations to apply
        transformed = True
        while transformed:
            transformed = False  # Flag to check if any transformation was applied in the current iteration
            # Loop through each node
            for node_id in list(self.g.get_node_ids()):
                node = self.g.nodes[node_id]

                # Check if the node is a co-leaf (not directly connected to an output)
                if node_id not in output_nodes:
                    # Apply transformation rules
                    if node.get_label() == '∼':
                        self.rule_not()
                        transformed = True
                    elif node.get_label() == '&':
                        self.rule_and()
                        transformed = True
                    elif node.get_label() == '|':
                        self.rule_or()
                        transformed = True
                    elif node.get_label() == 'ˆ':
                        self.rule_xor()
                        transformed = True
                    elif node.indegree() == 1 and node.outdegree() == 0:
                        self.rule_copy()
                        transformed = True
                    elif node.indegree() == 1 and node.outdegree() == 1:
                        self.rule_erase()
                        transformed = True
                    elif node.get_label() == 'ˆ' and node.indegree() > 2:
                        self.rule_involution()
                        transformed = True

    def hamming_encoder(self):
        """
        Constructs the Boolean circuit for the Hamming decoder.
        """
        self.parse_parentheses("(x0 & (~x2 ~x4 ~x5) & ((x1 & ~x4) ^ (~x2 & x6)))")

    def hamming_decoder(self):
        """
        Constructs the Boolean circuit for the Hamming encoder.
        """
        self.parse_parentheses("(x0 & (~x2 ~x4 ~x5) & ((x1 & ~x4) ^ (~x2 & x6))) ^ (x0 ~x1 ~x3)) & "
                               "((~x2 x4 ~x5) ^ (~x4 ~x5 x6)) & (x0 x1 ~x3))")


def random_int_list(n: int, bound: int, unique=False) -> List[int]:
    """
    Returns a list of n random integers between 0 and n
    :param n: int; numbers of integers wanted
    :param bound: int; maximum value of the integers
    :param unique: bool; set True if you want only unique integers
    :return: List[int]; a list of random numbers
    """
    if unique and n > bound + 1:
        raise ValueError("Bound too small compared to n")
    res = []
    for _ in range(n):
        tmp = randint(0, bound)
        if unique:
            while tmp in res:  # All numbers must be different to be IDs
                tmp = randint(0, bound)
        res.append(tmp)
    return res


def random_int_matrix(n: int, bound: int, unique=False, null_diag=True, symmetric=False,
                      oriented=False, dag=False) -> List[List[int]]:
    """
    Returns a matrix of nxn random integers between 0 and n
    :param n: int; numbers of rows and columns wanted
    :param bound: int; maximum value of the integers
    :param unique: bool; set True if you want only unique integers
    :param null_diag: bool; set True if you want the diagonal to be zeros
    :param symmetric: bool; set True if you want the matrix to be symmetric
    :param oriented: bool; set True if you want the matrix to define an oriented graph
    :param dag: bool; set True if you want the matrix to define an acyclic graph
    :return: List[List[int]]; a random matrix
    """
    if symmetric and (oriented or dag):
        raise ValueError("Matrix cannot be symmetric and oriented/acyclic")

    res = []
    for _ in range(n):
        res.append(random_int_list(n, bound, unique))

    if null_diag:
        for i in range(n):
            res[i][i] = 0

    if symmetric:
        for i in range(n):
            for j in range(i+1, n):
                res[j][i] = res[i][j]

    if oriented:
        for i in range(n):
            for j in range(i+1, n):
                if res[i][j] > 0:
                    res[j][i] = 0

    if dag:
        for i in range(n):
            for j in range(i+1, n):
                res[j][i] = 0

    return res


def graph_from_adjacency_matrix(matrix: List[List[int]]) -> OpenDigraph:
    """
    Returns an OpenDigraph from an adjency matrix
    :param matrix: List[List[int]]; the ajdency matrix
    :return: OpenDigraph; an OpenDigraph made from the matrix
    """
    n = len(matrix)
    nodes = []
    for identity in range(n):
        children = {}
        parents = {}
        for i in range(n):
            if len(matrix[i]) != n or len(matrix[identity]) != n:
                raise ValueError("The matrix is not a squared matrix")

            if matrix[identity][i]:
                children[i] = matrix[identity][i]

            if matrix[i][identity]:
                parents[i] = matrix[i][identity]

        node = Node(identity, str(identity), parents, children)
        nodes.append(node)

    return OpenDigraph([], [], nodes)


def min_distance(dic: Dict[int, int], nodes: List[int]) -> int:
    """
    Returns the node whose distance is the smallest
    :param dic: Dict[int, int];
    :param nodes: List[int];
    :return: int; node with the smallest distance
    """
    mini = None
    for node in dic:
        if node in nodes:
            if mini is None:
                mini = node
            else:
                if dic[node] < dic[mini]:
                    mini = node
    return mini
