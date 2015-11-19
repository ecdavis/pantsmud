import os.path
import random
import string

import networkx as nx

from pantsmud.world import node, link, persist, world, zone


WORLD_PATH = os.path.abspath("../data/world/world.json")
ZONE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "zones")
NODE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "nodes")
LINK_PATH = os.path.join(os.path.dirname(WORLD_PATH), "links")


def generate_node_name():
    letter_count = random.randint(2, 3)
    digit_count = random.randint(3, 4)
    letters = ''.join((random.choice(string.ascii_uppercase) for _ in range(letter_count)))
    digits = ''.join((random.choice(string.digits) for _ in range(digit_count)))
    return letters + "-" + digits


def generate_node(w, z):
    n = node.Node()
    n.name = generate_node_name()
    z.add_node(n)
    w.add_node(n)
    return n


def generate_link(w, n, d):
    l1 = link.Link()
    l1.name = d.name
    l1.dest = d
    l1.node = n
    w.add_link(l1)

    l2 = link.Link()
    l2.name = n.name
    l2.dest = n
    l2.node = d
    w.add_link(l2)


w = world.World()
z = zone.Zone()
z.name = "test_gen"
w.add_zone(z)

ns = []
g = nx.connected_watts_strogatz_graph(100, 2, 0.3)
for n in g.nodes_iter():
    ns.append(generate_node(w, z))
for node_index, dest_index in g.edges_iter():
    generate_link(w, ns[node_index], ns[dest_index])

persist.save_links(LINK_PATH, w)
persist.save_nodes(NODE_PATH, w)
persist.save_zones(ZONE_PATH, w)
persist.save_world(WORLD_PATH, w)
