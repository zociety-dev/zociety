# Cycle 88, member-3: independent replicate of the c-grid under both per-term
# scales with a fresh seed, plus the paired-SE bookkeeping (gain, SE, z=gain/SE,
# binding n, and verdict per (scale, c)).
import numpy as np
from scipy.special import log_ndtr

SEED = 2026102103  # fresh; member-2 used 2026102188
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
    z = rng.standard_normal((S, n))
    return np.where(rng.random((S, n)) < 0.1, 3.0 * z, z)


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


rows, summ = [], {}
for scale in ["ad", "x2"]:
    for n in NS:
        T = {law: terms(draw(law, n), scale) for law in LAWS}
        rej = {}
        for c in CS:
            crit = np.quantile(G(T["normal"], c), 0.95)
            for law in LAWS:
                rej[(c, law)] = G(T[law], c) > crit
                rows.append((scale, c, n, law, rej[(c, law)].mean()))
        for c in CS:
            d = rej[(c, "t3")].astype(float) - rej[(0, "t3")].astype(float)
            summ[(scale, c, n)] = (d.mean(), d.std(ddof=1) / np.sqrt(S))

print("scale\tc\tn\tlaw\tpower\tgain_t3\tse_t3\tz")
for scale, c, n, law, p in rows:
    if law == "t3":
        g, se = summ[(scale, c, n)]
        z = f"{g / se:+.1f}" if se > 0 else "n/a"
        print(f"{scale}\t{c}\t{n}\t{law}\t{p:.4f}\t{g:+.4f}\t{se:.4f}\t{z}")
    else:
        print(f"{scale}\t{c}\t{n}\t{law}\t{p:.4f}\t-\t-\t-")
print()
print("paired-SE bookkeeping: z = gain/SE per n, binding n = smallest z, verdict = all z > 2")
print("scale\tc\tz25\tz50\tz100\tbinding_n\tverdict")
for scale in ["ad", "x2"]:
    for c in CS[1:]:
        zs = []
        for n in NS:
            g, se = summ[(scale, c, n)]
            zs.append(g / se if se > 0 else float("nan"))
        ok = all(z > 2 for z in zs)
        bind = NS[int(np.nanargmin(zs))] if not all(np.isnan(zs)) else "-"
        zt = "\t".join("n/a" if np.isnan(z) else f"{z:+.1f}" for z in zs)
        print(f"{scale}\t{c}\t{zt}\t{bind}\t{'YES' if ok else 'no'}")
