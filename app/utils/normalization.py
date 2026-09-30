_TRANSLATION = str.maketrans(
    {
        **{chr(0x0660 + index): str(index) for index in range(10)},
        **{chr(0x06F0 + index): str(index) for index in range(10)},
        "٫": ".",
        "٬": None,
        "−": "-",
        "×": "*",
        "÷": "/",
        "²": "**2",
        "³": "**3",
        "\u00a0": " ",
    }
)


def normalize_text(text: str) -> str:
    return text.translate(_TRANSLATION).strip()
