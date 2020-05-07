import numpy as np

from pge.ranks.extrem_onl import NodeExInfo


class WayEx(NodeExInfo):
    @staticmethod
    def get_exes(gr, root, params):
        res = []
        nodes = gr.get_ids(stable=True)

        for params_ in params:
            levels = gr.get_attributes(params_[0])
            node_level = gr.get_attr(root, params_[0])

            ex = 1
            for u in np.unique(levels)[::-1]:
                if node_level <= u:
                    ts = np.array(gr.get_short_paths(root, nodes[levels <= u])[1])
                else:
                    ts = np.array(gr.get_short_paths(root, nodes[levels > u])[1])

                if ts.size == 0:
                    continue

                if np.max(ts) > 2:
                    ex = min([1, 2 * np.sum(ts - 1) ** 2 / (ts.size * np.sum(np.multiply(ts - 1, ts - 2)))])
                else:
                    ex = min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])
                if ex < 1:
                    break
            res.append((ex, params_[2]))
        return res

    @staticmethod
    def get_exes_comm(gr, nodes, params):
        res = []
        for params_ in params:
            cls = gr.get_attributes(params_[0], nodes)
            ex = 1
            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u])[1])
                if ts.size == 0:
                    continue

                if np.max(ts) > 2:
                    ex = min([1, 2 * np.sum(ts - 1) ** 2 / (ts.size * np.sum(np.multiply(ts - 1, ts - 2)))])
                else:
                    ex = min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])
                if ex < 1:
                    break
            res.append(ex)
        return res
