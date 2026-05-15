import pandas as pd
from src.sim import generate_trial_data


def test_data_generation_correlation():
    """
    Within each arm, sample correlation between baseline_covariate and outcome
    should equal `covariate_corr` within sampling error.
    Use n_per_arm=5000, covariate_corr=0.5, no dropout, seed fixed.
    Tolerance: |corr_hat - 0.5| < 0.03 per arm.
    """
    data = generate_trial_data(
        n_per_arm=5000,
        effect_size_d=0.0,
        covariate_corr=0.5,
        dropout_rate_control=0.0,
        dropout_rate_treatment=0.0,
        seed=42,
    )
    for arm in [0, 1]:
        arm_data = data[data["treatment"] == arm]
        corr_hat = arm_data["baseline_covariate"].corr(arm_data["outcome"])
        assert abs(corr_hat - 0.5) < 0.03, (
            f"arm={arm}: corr_hat={corr_hat:.4f}, expected 0.5 ± 0.03"
        )


def test_data_generation_dropout():
    """
    With dropout_rate_control=0.1, dropout_rate_treatment=0.2, n_per_arm=5000,
    seed fixed:
      - proportion missing in control arm within ±0.02 of 0.10
      - proportion missing in treatment arm within ±0.02 of 0.20
      - baseline_covariate has zero missing values
    """
    data = generate_trial_data(
        n_per_arm=5000,
        effect_size_d=0.0,
        covariate_corr=0.0,
        dropout_rate_control=0.1,
        dropout_rate_treatment=0.2,
        seed=42,
    )
    control = data[data["treatment"] == 0]
    treatment = data[data["treatment"] == 1]

    prop_missing_control = control["outcome"].isna().mean()
    prop_missing_treatment = treatment["outcome"].isna().mean()

    assert abs(prop_missing_control - 0.10) <= 0.02, (
        f"control dropout={prop_missing_control:.4f}, expected 0.10 ± 0.02"
    )
    assert abs(prop_missing_treatment - 0.20) <= 0.02, (
        f"treatment dropout={prop_missing_treatment:.4f}, expected 0.20 ± 0.02"
    )
    assert data["baseline_covariate"].isna().sum() == 0, (
        "baseline_covariate should have zero missing values"
    )


def test_reproducibility():
    """Same seed → identical DataFrame."""
    kwargs = dict(
        n_per_arm=200,
        effect_size_d=0.3,
        covariate_corr=0.4,
        dropout_rate_control=0.05,
        dropout_rate_treatment=0.10,
        seed=99,
    )
    df1 = generate_trial_data(**kwargs)
    df2 = generate_trial_data(**kwargs)
    pd.testing.assert_frame_equal(df1, df2)


def test_outcome_scale():
    """
    With effect_size_d=0, covariate_corr=0, no dropout, n_per_arm=5000:
    sample variance of outcome within each arm is within ±0.05 of 1.0.
    """
    data = generate_trial_data(
        n_per_arm=5000,
        effect_size_d=0.0,
        covariate_corr=0.0,
        dropout_rate_control=0.0,
        dropout_rate_treatment=0.0,
        seed=42,
    )
    for arm in [0, 1]:
        var_hat = data[data["treatment"] == arm]["outcome"].var()
        assert abs(var_hat - 1.0) <= 0.05, (
            f"arm={arm}: var(outcome)={var_hat:.4f}, expected 1.0 ± 0.05"
        )
