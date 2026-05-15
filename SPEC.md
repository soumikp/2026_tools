# Specification: Monte Carlo Power Calculator for 2-Arm Parallel RCT

## 1. Overview
A Monte Carlo power calculator for a 2-arm parallel RCT with a continuous primary endpoint. The system simulates trial data, evaluates statistical power, Type I error, and treatment-effect bias for ANCOVA (adjusting for a baseline covariate), and compares against an unadjusted Welch t-test.

## 2. Parameter Space
- **Sample size per arm (`n`)**: 20 to 500
- **True effect size (`d`)**: 0 to 1 (Cohen's d, on unit-variance outcome scale — see §4.1)
- **Baseline covariate correlation (`r`)**: 0 to 0.8 (within-arm correlation between baseline covariate and outcome)
- **Differential dropout rate**: 0% to 30% per arm

## 3. Directory Structure
```text
.
├── src/
│   ├── __init__.py
│   ├── sim.py          # Simulation engine for data generation
│   └── analyze.py      # Estimators and statistical analysis
├── tests/
│   ├── __init__.py
│   ├── test_sim.py
│   └── test_analyze.py
├── app.py              # Streamlit UI
└── requirements.txt
```

## 4. Statistical Specification

### 4.1 Data-Generating Process

Outcomes are unit-variance (σ = 1) throughout, so `effect_size_d` is interpretable as Cohen's d.

For each subject *i* in arm *a* ∈ {0, 1}, independently:
- Baseline covariate: Xᵢ ~ N(0, 1)
- Outcome (pre-dropout): Yᵢ = r · Xᵢ + d · 𝟙(a = 1) + εᵢ,   εᵢ ~ N(0, 1 − r²),  εᵢ ⊥ Xᵢ

This implies, within each arm:
- Var(X) = Var(Y) = 1
- Cor(X, Y) = r
- E[Y | a=1] − E[Y | a=0] = d

### 4.2 Missingness Mechanism

**MCAR.** For each subject in arm *a*, independently set the outcome to NaN with probability `dropout_rate_a`. Baseline covariate is always observed. Dropout is independent of X, Y, and ε. (MAR/MNAR extensions are deferred to a future iteration.)

### 4.3 Analysis Models

**Unadjusted t-test.** Welch's two-sample t-test on complete cases (subjects with observed outcomes), two-sided, α = 0.05 default. Estimate = mean(Y_treatment) − mean(Y_control).

**ANCOVA.** OLS regression `outcome ~ treatment + baseline_covariate` on complete cases, fit via statsmodels. Two-sided test on the treatment coefficient. Estimate = coefficient on `treatment`. SE = OLS standard error on the treatment coefficient.

### 4.4 Operating Characteristics

Across n_sim replicates, compute:
- **Power / Type I error**: proportion of replicates with p ≤ α. Reported as Type I error when `effect_size_d = 0`, otherwise as power.
- **Bias**: mean(estimate) − `effect_size_d`.
- **MC 95% CI for power**: Wald interval, p̂ ± 1.96 · √(p̂(1−p̂)/n_sim), clamped to [0, 1].
- **Mean SE** for each method: average of within-replicate standard errors, used for the variance-reduction sanity check (Criterion C).

## 5. Function Signatures

### `src/sim.py`
```python
import pandas as pd

def generate_trial_data(
    n_per_arm: int,
    effect_size_d: float,
    covariate_corr: float,
    dropout_rate_control: float,
    dropout_rate_treatment: float,
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Generate a synthetic 2-arm parallel RCT dataset per §4.1–4.2.

    Returns a DataFrame with columns:
      - subject_id: int
      - treatment: int (0 control, 1 treatment)
      - baseline_covariate: float (always observed)
      - outcome: float (NaN for dropouts, MCAR per arm)
    """
```

### `src/analyze.py`
```python
import pandas as pd
from typing import Dict

def analyze_trial(data: pd.DataFrame, alpha: float = 0.05) -> Dict[str, float]:
    """
    Per §4.3. Returns:
      - t_test_p_value, t_test_effect_estimate, t_test_se
      - ancova_p_value, ancova_effect_estimate, ancova_se
    All two-sided. Complete-case analysis.
    """

def run_monte_carlo(
    n_sim: int,
    n_per_arm: int,
    effect_size_d: float,
    covariate_corr: float,
    dropout_rate_control: float,
    dropout_rate_treatment: float,
    alpha: float = 0.05,
    seed: int | None = None,
) -> Dict[str, float]:
    """
    Returns aggregates over n_sim iterations:
      - ancova_power, ancova_type1_error (if d==0), ancova_bias
      - ttest_power,  ttest_type1_error  (if d==0), ttest_bias
      - ancova_power_ci_lower, ancova_power_ci_upper   (Wald, §4.4)
      - ttest_power_ci_lower,  ttest_power_ci_upper
      - mean_ancova_se, mean_ttest_se                  (for Criterion C)
    """
```

### `app.py`
```python
def main():
    """
    Streamlit UI.
    Sidebar inputs: effect_size_d, covariate_corr, dropout rates, n_sim, alpha.
    Outputs:
      - Power curves over n_per_arm grid {20, 30, 50, 75, 100, 150, 200, 300, 500},
        with MC 95% CI shaded bands for both methods on one figure.
      - Type I error panel (shown only when d == 0).
      - Bias panel for both methods, with MC CI (±1.96 · SD / sqrt(n_sim)).
    Cache run_monte_carlo with @st.cache_data keyed on all parameters.
    """
```

## 6. Acceptance Tests (`tests/test_analyze.py`)

### Criterion A — Type I Error Under H0
With `effect_size_d=0`, `covariate_corr=0.3`, no dropout, `n_per_arm=100`, `n_sim=5000`, `seed=42`:
```python
assert abs(results['ancova_type1_error'] - 0.05) <= 0.01
assert abs(results['ttest_type1_error']  - 0.05) <= 0.01
```
(MC SE ≈ 0.003 at p=0.05; tolerance ±0.01 is ~3 SE.)

### Criterion B — Unadjusted Power Matches Analytical
With `effect_size_d=0.5`, `covariate_corr=0`, no dropout, `n_per_arm=64`, `n_sim=5000`, `seed=42`:
```python
assert abs(results['ttest_power'] - 0.80) <= 0.02
```
(`pwr.t.test(n=64, d=0.5, sig.level=0.05, type="two.sample")` gives 0.802.)

### Criterion C — ANCOVA Variance Reduction
With `effect_size_d=0`, `covariate_corr=0.5`, no dropout, `n_per_arm=100`, `n_sim=2000`, `seed=42`:
```python
expected_ratio = (1 - 0.5**2) ** 0.5  # ≈ 0.866
observed_ratio = results['mean_ancova_se'] / results['mean_ttest_se']
assert abs(observed_ratio - expected_ratio) <= 0.05
```
Sanity-checks that ANCOVA is actually buying variance reduction — the entire pedagogical point of the comparison.

## 7. Engine Tests (`tests/test_sim.py`)

```python
def test_data_generation_correlation():
    """
    Within each arm, sample correlation between baseline_covariate and outcome
    should equal `covariate_corr` within sampling error.
    Use n_per_arm=5000, covariate_corr=0.5, no dropout, seed fixed.
    Tolerance: |corr_hat - 0.5| < 0.03 per arm.
    """

def test_data_generation_dropout():
    """
    With dropout_rate_control=0.1, dropout_rate_treatment=0.2, n_per_arm=5000,
    seed fixed:
      - proportion missing in control arm within ±0.02 of 0.10
      - proportion missing in treatment arm within ±0.02 of 0.20
      - baseline_covariate has zero missing values
    """

def test_reproducibility():
    """Same seed → identical DataFrame."""

def test_outcome_scale():
    """
    With effect_size_d=0, covariate_corr=0, no dropout, n_per_arm=5000:
    sample variance of outcome within each arm is within ±0.05 of 1.0.
    """
```

## 8. Dependencies (`requirements.txt`)
```
numpy
scipy
pandas
statsmodels
pytest
streamlit
```