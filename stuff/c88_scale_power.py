import numpy as np
from scipy.special import log_ndtr

SEED = 20261021_88
S = 20000
CS = [0, 1, 5, 20, 40]
NS = [25, 50, 100]
LAWS = ["normal", "t3", "t5", "mix"]
rng = np.random.default_rng(SEED)


def draw(law, n):
    if law == "normal":
        return rng.standard_normal((S, n))
    if law == "t3":
        return rng.standard_t(3, (S, n))
    if law == "t5":
        return rng.standard_t(5, (S, n))
    if law == "mix":
        z = rng.standard_normal((S, n))
        w = rng.random((S, n)) < 0.1
        return np.where(w, 3.0 * z, z)


def terms(x, scale):
    n = x.shape[1]
    z = (x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True)
    if scale == "x2":
        return z * z
    zs = np.sort(z, axis=1)
    i = np.arange(1, n + 1)
    return -((2 * i - 1) / n) * (log_ndtr(zs) + log_ndtr(-zs[:, ::-1]))


def G(t, c):
    if c == 0:
        return np.round(t.sum(1), 9)
    return (np.log1p(c * t) / c).sum(1)


rows = []
summary = {}
for scale in ["ad", "x2"]:
    for n in NS:
        data = {law: draw(law, n) for law in LAWS}
        T = {law: terms(data[law], scale) for law in LAWS}
        rej = {}
        for c in CS:
            g0 = G(T["normal"], c)
            crit = np.quantile(g0, 0.95)
            for law in LAWS:
                r = G(T[law], c) > crit
                rej[(c, law)] = r
                rows.append((scale, c, n, law, r.mean()))
        for c in CS:
            d = rej[(c, "t3")].astype(float) - rej[(0, "t3")].astype(float)
            summary[(scale, c, n)] = (d.mean(), d.std(ddof=1) / np.sqrt(S))

print("scale\tc\tn\tlaw\tpower\tgain_t3\tse_t3")
for scale, c, n, law, p in rows:
    if law == "t3":
        g, se = summary[(scale, c, n)]
        print(f"{scale}\t{c}\t{n}\t{law}\t{p:.4f}\t{g:+.4f}\t{se:.4f}")
    else:
        print(f"{scale}\t{c}\t{n}\t{law}\t{p:.4f}\t\t")
print()
print("pairs clearing 2 SE at every n:")
for scale in ["ad", "x2"]:
    for c in CS[1:]:
        ok = all(summary[(scale, c, n)][0] > 2 * summary[(scale, c, n)][1] for n in NS)
        zs = " ".join(f"{summary[(scale, c, n)][0] / summary[(scale, c, n)][1]:+.1f}" for n in NS)
        print(f"  {scale} c={c}: {'YES' if ok else 'no'}  (gain/SE at n=25,50,100: {zs})")
