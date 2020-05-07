import numpy as np

from joblib import Parallel, delayed
from statsmodels.tsa.stattools import adfuller

from pge.ranks.extrem_onl import NodeExInfo


class LineEx(NodeExInfo):
    @staticmethod
    def get_exes(gr, root, params):
        paths, di = gr.get_short_line_paths(root)
        res = []
        cls1 = gr.get_attr(root, "cls")
        cls2 = gr.get_attr(root, "cls2")

        for params_ in params:
            xs, lv = gr.get_ln_attrs(params_[0], paths)
            ps = [adfuller(xs_)[1] for xs_ in xs if len(xs_) > 10]
            ex1, ex2 = LineEx.estimate(xs, lv, cls1, cls2, gr.get_attributes(params_[0]))
            res.append((ex1, ex2, np.mean(ps), params_[1]))
        return res

    @staticmethod
    def estimate(xs, lv, cls1, cls2, us):
        exes = []
        qs = []

        for t1 in [True, False]:
            ex = 1
            q = 1

            if t1:
                res1 = np.array(Parallel(n_jobs=2, backend="multiprocessing")(delayed(LineEx.ex_estimate)(xs, u,
                                                                                                         t1) for u in
                                                                              lv if np.sum(us > u)/us.size - cls1 > 0))
                res2 = np.array([min([1, 2 * cls1 / (cls2*(np.sum(us > u)/us.size - cls1))]) for u in lv if np.sum(us > u)/us.size - cls1 > 0])
            else:
                res1 = np.array(Parallel(n_jobs=2, backend="multiprocessing")(delayed(LineEx.ex_estimate)(xs, u,
                                                                                                         t1) for u in
                                                                              lv if
                                                                              np.sum(us <= u) / us.size - cls1 > 0))
                res2 = np.array([min([1, 2 * cls1 / (cls2*(np.sum(us <= u)/us.size - cls1))]) for u in lv if np.sum(us <= u)/us.size - cls1 > 0])
            res1, res2 = res1[res1 < 1], res2[res1 < 1]
            if res1.size > 0:
                test = np.subtract(res1, res2)
                if test[test >= 0].size > 0:
                    res1, res2 = res1[test >= 0], res2[test >= 0]

                ex = res1[-1]
                q = res2[-1]

            exes.append(ex)
            qs.append(q)
        return (exes[0], qs[0]), (exes[1], qs[1])

    @staticmethod
    def ex_estimate(xs, lv, t1):
        ts = np.array([])
        qs = 0
        ns = 0
        for xs_ in xs:
            if t1:
                ts_ = np.where(xs_ > lv)[0]
                qs += ts_.size
            else:
                ts_ = np.where(xs_ <= lv)[0]
                qs += xs_.size - ts_.size

            if ts_.size > 1:
                ts = np.append(ts, np.diff(ts_))
            ns += xs_.size

        if ts.size == 0:
            return 1

        if np.max(ts) > 2:
            return min([1, 2 * np.sum(ts - 1) ** 2 / (ts.size * np.sum(np.multiply(ts - 1, ts - 2)))])
        else:
            return min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])
