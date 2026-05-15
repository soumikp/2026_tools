import pytest


def test_data_generation_correlation():
    """
    Within each arm, sample correlation between baseline_covariate and outcome
    should equal `covariate_corr` within sampling error.
    Use n_per_arm=5000, covariate_corr=0.5, no dropout, seed fixed.
    Tolerance: |corr_hat - 0.5| < 0.03 per arm.
    """
    pytest.skip("not yet implemented")


def test_data_generation_dropout():
    """
    With dropout_rate_control=0.1, dropout_rate_treatment=0.2, n_per_arm=5000,
    seed fixed:
      - proportion missing in control arm within ±0.02 of 0.10
      - proportion missing in treatment arm within ±0.02 of 0.20
      - baseline_covariate has zero missing values
    """
    pytest.skip("not yet implemented")


def test_reproducibility():
    """Same seed → identical DataFrame."""
    pytest.skip("not yet implemented")


def test_outcome_scale():
    """
    With effect_size_d=0, covariate_corr=0, no dropout, n_per_arm=5000:
    sample variance of outcome within each arm is within ±0.05 of 1.0.
    """
    pytest.skip("not yet implemented")
