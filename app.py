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
    raise NotImplementedError


if __name__ == "__main__":
    main()
