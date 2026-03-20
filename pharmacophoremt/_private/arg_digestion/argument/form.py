def digest_form(form, ctx=None):
    if form is not None:
        if form not in ['pharmer', 'ligandscout']:
            raise ValueError(f"Invalid form: {form}")
    return form
