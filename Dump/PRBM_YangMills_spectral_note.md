# Spectral Statistics of Yang–Mills Glueball Masses: A Falsifiable Question, Honestly Scoped

*Independent research note — v1.2*

---

## Abstract

We ask whether the low-lying glueball spectrum of SU(3) Yang–Mills theory shows
deviations from Gaussian Unitary Ensemble (GUE) statistics, using power-law random
banded matrices (PRBM) as a one-parameter family of comparison ensembles. This
question sits within an existing line of work — chiral random matrix theory
(chRMT), developed since the early 1990s by Verbaarschot, Shuryak, and others —
that already studies spectral universality classes in QCD. We do not claim
novelty at the level of "is QCD spectral data described by random matrix theory";
that question is established. What we scope more narrowly is whether the specific
PRBM family, rather than the standard Dyson/chiral classes, offers a useful
description. We state plainly that current lattice glueball datasets (~10–20
reliably resolved states) are too small to fit a continuous parameter with any
statistical power. This is not a limitation to be waved at in a "future work"
section — it is the reason the numerical program below is currently infeasible,
and any version of this note that doesn't say so upfront is not being honest
about its own status.

---

## 1. Background

- Riemann zeros ($t_n$) closely match GUE pair-correlation statistics
  (Montgomery–Odlyzko). This is long-established and not in question here.
- Lattice QCD spectra — of the Dirac operator, and separately of hadron/glueball
  mass spectra — have been studied for spectral statistics since the early
  1990s under the heading of chiral random matrix theory. That literature
  already identifies which Dyson/chiral symmetry class governs QCD spectra
  under various conditions (Verbaarschot & Zahed 1993; Shuryak & Verbaarschot
  1993; see Verbaarschot & Wettig, *Annu. Rev. Nucl. Part. Sci.* 2000, for a
  review).
- This note is *not* about Riemann zeros. An earlier version of this project
  attempted to connect Riemann zeros and Yang–Mills spectra through a shared
  fractal parameter; that construction was trivial (fitting a scale parameter
  to Riemann zeros, which are already known to match pure GUE, effectively
  fixes the parameter before the Yang–Mills side is even tested). Dropping
  that connection is a correction, not a loss — the question below stands on
  its own without needing to touch RH.

---

## 2. The PRBM Ensemble

Power-law random banded matrices are defined by

$$
H_{ij} = \frac{X_{ij}}{(1 + |i-j|)^{\alpha}}, \qquad X_{ij} \sim \mathcal{N}(0,1),
$$

with the following established behavior (Mirlin & Fyodorov, and subsequent
literature on PRBM criticality):

| range of α | regime |
|---|---|
| α = 0 | fully delocalized, GUE-like |
| 0 < α < 1 | extended, GUE-like |
| α = 1 | critical point — multifractal eigenstates |
| α > 1 | localized, Poisson-like |

α = 1 is a single critical point, not a broad intermediate region.

---

## 3. The Question

> Do glueball spacing/correlation statistics from lattice QCD match pure GUE
> (α = 0), or do they show measurable deviation consistent with α > 0?

This is falsifiable in principle: a clean fit would return α ≈ 0 (no
deviation) or a nonzero value with a defensible confidence interval.

**It is not, however, testable in practice with current data**, for a
specific quantitative reason, not a vague caveat:

- A two-point correlation function requires enough level spacings to
  distinguish a correlation shape from sampling noise. With ~10–20 levels
  you have on the order of 10 independent spacings — nowhere near enough to
  distinguish, say, α = 0 from α = 0.3, whose correlation functions differ
  only in their tails.
- This isn't solved by cleverer fitting. It's a statistical power problem
  inherent to the size of existing lattice glueball datasets. Any fit
  performed today would have a confidence interval wide enough to be
  consistent with almost any α, making the result uninformative regardless
  of the point estimate.

So: **the question is well-posed; the data to answer it does not yet exist
at sufficient volume.** This should be stated as a blocking precondition, not
mentioned once and then set aside.

---

## 4. What Would Be Needed

1. Lattice QCD glueball spectra with O(100+) reliably resolved excited
   states in a single channel — well beyond what current computations
   target, since most lattice studies aim for a handful of low-lying,
   phenomenologically relevant states rather than a dense spectrum.
2. A pre-registered analysis (fit procedure, confidence interval method)
   to avoid post-hoc parameter tuning.
3. A literature check — not assumed but actually done — of whether chRMT
   papers already address PRBM-type deviations or an equivalent parameter
   within the chiral symmetry class framework, so this doesn't duplicate
   existing results under a different name.

---

## 5. Honest Scope of a Positive or Negative Result

Even in the best case, with sufficient future data and a clean α ≠ 0 fit:

- This would **not** bear on the Riemann Hypothesis.
- This would **not** bear on the Yang–Mills mass gap problem (existence of a
  mass gap is a statement about the bottom of the spectrum and the
  continuum limit of the theory; spacing statistics of already-computed
  discrete levels are a separate question).
- This would be a modest, well-defined statement about which random-matrix
  universality class best describes glueball spectral fluctuations —
  worth knowing, but adjacent to, not a step toward, either Millennium
  Problem.

## 6. Conclusion

The question of whether Yang–Mills glueball spectra deviate from GUE
statistics is a legitimate, falsifiable, narrowly-scoped question that sits
inside an existing research tradition (chRMT) rather than opening a new one.
It cannot currently be tested due to insufficient lattice data, and even a
clean result would not touch either RH or the Yang–Mills mass gap. Framed
this way, it's a small, honest research note — not a unifying framework.
