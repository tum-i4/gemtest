def wrong_skip_method_used(*_, **__):
    raise SystemExit("The usage of pytest.skip() is prohibited. Use gmt.skip() instead.")
