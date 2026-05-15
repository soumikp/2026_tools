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
    raise NotImplementedError
