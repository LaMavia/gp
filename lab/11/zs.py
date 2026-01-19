# Tree node class
from typing import Optional
import sys
import math
from itertools import batched


# https://www.geeksforgeeks.org/dsa/sparse-table/
def buildSparseTable(arr):
    n = len(arr)

    # create the 2d table
    lookup = [[0] * (int(math.log(n, 2)) + 1) for _ in range(n + 1)]

    # Initialize for the intervals with length 1
    for i in range(n):
        lookup[i][0] = arr[i]

    # Compute values from smaller to bigger intervals
    for j in range(1, int(math.log(n, 2)) + 1):
        for i in range(0, n - (1 << j) + 1):
            lookup[i][j] = min(lookup[i][j - 1], lookup[i + (1 << (j - 1))][j - 1])

    return lookup


class Node:
    # tpl_or_lab - tuple=internal node
    #           or string=a leaf (label)
    # parent - defines a parent of a non-root node
    def __init__(self, tpl_or_lab, parent=None):
        self.left = None
        self.right = None

        if type(tpl_or_lab) is tuple:
            self.left = Node(tpl_or_lab[0], self)
            self.right = Node(tpl_or_lab[1], self)
            self.label = None
        else:
            self.label = tpl_or_lab
        self.parent = parent
        self.src = tpl_or_lab

    # is a leaf
    def leaf(self):
        return self.label

    def __str__(self):
        if self.leaf():
            return self.label or "-"
        return f"({self.left},{self.right})"

    def make_rmq(self):
        def aux(
            node: "Node",
            current_depth: int,
            path: list["Node"],
            depth: list[int],
            leaf_index_map: dict[str, int],
        ):
            path.append(node)
            depth.append(current_depth)
            if node.label is not None:
                leaf_index_map[node.label] = len(depth) - 1

            for child in [node.left, node.right]:
                if child is None:
                    continue
                aux(child, current_depth + 1, path, depth, leaf_index_map)
                path.append(node)
                depth.append(current_depth)

        aux(self, 0, path := [], depth := [], leaf_index_map := {})

        return path, depth, leaf_index_map


class LCA:
    def __init__(self, root: Node) -> None:
        self.path, self.depth, self.lim = root.make_rmq()

        n = len(self.depth)
        self.block_size = int(math.log2(n) + 1) // 2
        depth_blocks = [list(block) for block in batched(self.depth, self.block_size)]
        self.depth_tables = [buildSparseTable(block) for block in depth_blocks]
        self.block_mask = self._build_block_mask()

    def _block_of_index(self, i: int) -> int:
        return i // self.block_size

    def _min_by_h(self, i: int, j: int) -> int:
        if self.depth[i] <= self.depth[j]:
            return i

        return j

    # https://cp-algorithms.com/graph/lca_farachcoltonbender.html
    def _build_block_mask(self):
        block_mask = [0] * len(self.depth_tables)

        j = 0
        b = 0
        m = len(self.path)

        for i in range(m):
            if j == self.block_size:
                j = 0
                b += 1
            if j > 0 and (i >= m or self._min_by_h(i - 1, i) == i - 1):
                block_mask[b] += 1 << (j - 1)

            j += 1

        return block_mask

    def lca_in_block(self, b: int, l: int, r: int) -> int:
        return self.depth_tables[self.block_mask[b]][l][r] + b * self.block_size

    def __call__(self, x_label: str, y_label: str):
        x_idx = self.lim[x_label]
        y_idx = self.lim[y_label]

        if x_idx > y_idx:
            x_idx, y_idx = y_idx, x_idx

        x_block_idx = self._block_of_index(x_idx)
        y_block_idx = self._block_of_index(y_idx)

        if x_block_idx == y_block_idx:
            return self.path[
                self.lca_in_block(
                    x_block_idx, x_idx % self.block_size, y_idx % self.block_size
                )
            ]

        # int ans1 = lca_in_block(bl, l % block_size, block_size - 1);
        ans1 = self.lca_in_block(x_block_idx, x_idx % self.block_size, self.block_size - 1)
        # int ans2 = lca_in_block(br, 0, r % block_size);
        ans2 = self.lca_in_block(y_block_idx, 0, y_idx % self.block_size)
        # int ans = min_by_h(ans1, ans2);
        ans = self._min_by_h(ans1, ans2)

        # if (bl + 1 < br) {
        #     int l = log_2[br - bl - 1];
        #     int ans3 = st[bl+1][l];
        #     int ans4 = st[br - (1 << l)][l];
        #     ans = min_by_h(ans, min_by_h(ans3, ans4));
        # }
        # return euler_tour[ans];

        if x_block_idx + 1 < y_block_idx:
            l = math.log2(x_block_idx - y_block_idx - 1)
            an3 = 


def main():
    tree = Node((("C", ("D", "E")), ("A", "G")))


if __name__ == "__main__":
    main()
