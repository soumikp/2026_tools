import pandas as pd
from typing import Dict


def analyze_trial(data: pd.DataFrame, alpha: float = 0.05) -> Dict[str, float]:
    """
    Per §4.3. Returns:
      - t_test_p_value, t_test_effect_estimate, t_test_se
      - ancova_p_value, ancova_effect_estimate, ancova_se
    All two-sided. Complete-case analysis.
    """
    raise NotImplementedError


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
    raise NotImplementedError
