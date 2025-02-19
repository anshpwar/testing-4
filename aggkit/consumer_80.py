"""Consumer added independently of the base-side change (scenario 80)."""


from .deps import textfmt


def column(text):
    return textfmt.pad_left(text, 12)
