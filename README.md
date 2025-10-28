## Description

This is an illustrative simulation of the flood-based multicasting technique. A set of nodes are spawned as threads with workloads representing their activity, in which the node is sleeping on a condition variable and waiting for broadcast trigger from a neighbour node.

## Usage

```bash
uv run src/main.py
```

## Todo

- Emphasize “real” parallelism for running nodes.
- Support a simple way to define graph structure.
- Support “random graphs” (i.e graphs that have a probability whether node `A` is connected to node `B`).
