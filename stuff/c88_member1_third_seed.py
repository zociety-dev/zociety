# Cycle 88, member-1: third independent seed for the c-grid under both per-term
# scales, with paired Monte Carlo SEs on the t(3) power gain over c=0 and the
# two-SE-at-every-n verdict per (scale, c). Also reports the AD c=0 power at
# each law as the reference the gains are measured against.
# Run: uv run --with numpy --with scipy python stuff/c88_member1_third_seed.py
import numpy as np
from scipy.special import log_ndtr

SEED = 2026102111  # fresh; member-2 used 2026102188, member-3 used 2026102103
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
    # z: sample standardized by its own mean and SD (ddof=1).
    n = x.shape[1]
    z = (x - x.mean(1, keepdims=True)) / x.std(1, ddof=1, keepdims=True)
    if scale == "x2":
        return z * z
    zs = np.sort(z, axis=1)
    i = np.arange(1, n + 1)
    # t_i = -((2i-1)/n) [ln Phi(z_(i)) + ln(1 - Phi(z_(n+1-i)))]
    return -((2 * i - 1) / n) * (log_ndtr(zs) + log_ndtr(-zs[:, ::-1]))


def stat(t, c):
    if c == 0:
        return t.sum(1)
    return np.log1p(c * t).sum(1) / c


rows = []
verdict = {}
for scale in ["ad", "x2"]:
    for n in NS:
        T = {law: terms(draw(law, n), scale) for law in LAWS}
        rej = {}
        for c in CS:
            g0 = stat(T["normal"], c)
            crit = np.quantile(g0, 0.95)
            rej[c] = {law: stat(T[law], c) > crit for law in LAWS}
        for c in CS:
            d = rej[c]["t3"].astype(float) - rej[0]["t3"].astype(float)
            gain, se = d.mean(), d.std(ddof=1) / np.sqrt(S)
            for law in LAWS:
                rows.append((scale, c, n, law, rej[c][law].mean(),
                             gain if law == "t3" else None,
                             se if law == "t3" else None))
            verdict.setdefault((scale, c), []).append(gain > 2 * se)

print("| scale | c | n | law | power | t3 gain vs c=0 | paired SE |")
print("|---|---|---|---|---|---|---|")
for scale, c, n, law, p, g, se in rows:
    gs = "" if g is None else f"{g:+.4f}"
    ss = "" if se is None else f"{se:.4f}"
    print(f"| {scale} | {c} | {n} | {law} | {p:.4f} | {gs} | {ss} |")
print()
print("| scale | c | clears 2 SE at n=25,50,100 | every n |")
print("|---|---|---|---|")
for (scale, c), v in verdict.items():
    if c == 0:
        continue
    print(f"| {scale} | {c} | {', '.join('yes' if b else 'no' for b in v)} | "
          f"{'YES' if all(v) else 'no'} |")
