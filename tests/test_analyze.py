from src.analyze import run_monte_carlo


def test_criterion_a_type1_error():
    """
    Criterion A — Type I Error Under H0.
    With effect_size_d=0, covariate_corr=0.3, no dropout, n_per_arm=100,
    n_sim=5000, seed=42:
      assert abs(results['ancova_type1_error'] - 0.05) <= 0.01
      assert abs(results['ttest_type1_error']  - 0.05) <= 0.01
    (MC SE ≈ 0.003 at p=0.05; tolerance ±0.01 is ~3 SE.)
    """
    results = run_monte_carlo(
        n_sim=5000,
        n_per_arm=100,
        effect_size_d=0.0,
        covariate_corr=0.3,
        dropout_rate_control=0.0,
        dropout_rate_treatment=0.0,
        alpha=0.05,
        seed=42,
    )
    assert abs(results["ancova_type1_error"] - 0.05) <= 0.01, (
        f"ANCOVA type I error={results['ancova_type1_error']:.4f}, expected 0.05 ± 0.01"
    )
    assert abs(results["ttest_type1_error"] - 0.05) <= 0.01, (
        f"t-test type I error={results['ttest_type1_error']:.4f}, expected 0.05 ± 0.01"
    )


def test_criterion_b_unadjusted_power():
    """
    Criterion B — Unadjusted Power Matches Analytical.
    With effect_size_d=0.5, covariate_corr=0, no dropout, n_per_arm=64,
    n_sim=5000, seed=42:
      assert abs(results['ttest_power'] - 0.80) <= 0.02
    (pwr.t.test(n=64, d=0.5, sig.level=0.05, type="two.sample") gives 0.802.)
    """
    results = run_monte_carlo(
        n_sim=5000,
        n_per_arm=64,
        effect_size_d=0.5,
        covariate_corr=0.0,
        dropout_rate_control=0.0,
        dropout_rate_treatment=0.0,
        alpha=0.05,
        seed=42,
    )
    assert abs(results["ttest_power"] - 0.80) <= 0.02, (
        f"t-test power={results['ttest_power']:.4f}, expected 0.80 ± 0.02"
    )


def test_criterion_c_ancova_variance_reduction():
    """
    Criterion C — ANCOVA Variance Reduction.
    With effect_size_d=0, covariate_corr=0.5, no dropout, n_per_arm=100,
    n_sim=2000, seed=42:
      expected_ratio = (1 - 0.5**2) ** 0.5  # ≈ 0.866
      observed_ratio = results['mean_ancova_se'] / results['mean_ttest_se']
      assert abs(observed_ratio - expected_ratio) <= 0.05
    Sanity-checks that ANCOVA is actually buying variance reduction — the
    entire pedagogical point of the comparison.
    """
    results = run_monte_carlo(
        n_sim=2000,
        n_per_arm=100,
        effect_size_d=0.0,
        covariate_corr=0.5,
        dropout_rate_control=0.0,
        dropout_rate_treatment=0.0,
        alpha=0.05,
        seed=42,
    )
    expected_ratio = (1 - 0.5**2) ** 0.5  # ≈ 0.866
    observed_ratio = results["mean_ancova_se"] / results["mean_ttest_se"]
    assert abs(observed_ratio - expected_ratio) <= 0.05, (
        f"SE ratio={observed_ratio:.4f}, expected {expected_ratio:.4f} ± 0.05"
    )
