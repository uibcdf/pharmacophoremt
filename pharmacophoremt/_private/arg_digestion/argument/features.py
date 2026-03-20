def digest_features(features, ctx=None):
    if isinstance(features, str):
        return [features]
    if isinstance(features, (list, tuple)):
        return [str(ii) for ii in features]
    raise TypeError(f"Expected str or list of str for features, got {type(features)}")
