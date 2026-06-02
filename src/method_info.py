"""Metadata and descriptions for interpolation methods."""

from .config import CLASSICAL_METHODS, ML_METHODS

METHOD_DESCRIPTIONS = {
    "forward_fill": {
        "name": "Forward fill",
        "category": "classical",
        "description": "Propagates the last observed value forward in time.",
        "uses_covariates": False,
        "needs_training": False,
    },
    "linear": {
        "name": "Linear interpolation",
        "category": "classical",
        "description": "Connects observed points with straight lines.",
        "uses_covariates": False,
        "needs_training": False,
    },
    "time": {
        "name": "Time interpolation",
        "category": "classical",
        "description": "Linear interpolation based on actual time distance.",
        "uses_covariates": False,
        "needs_training": False,
    },
    "cubic": {
        "name": "Cubic interpolation",
        "category": "classical",
        "description": "Uses cubic polynomials between observed points.",
        "uses_covariates": False,
        "needs_training": False,
    },
    "spline": {
        "name": "Spline interpolation",
        "category": "classical",
        "description": "Uses spline curves to reconstruct missing values.",
        "uses_covariates": False,
        "needs_training": False,
    },
    "random_forest": {
        "name": "Random Forest",
        "category": "ml",
        "description": "Ensemble of decision trees trained on engineered features.",
        "uses_covariates": True,
        "needs_training": True,
    },
    "mlp": {
        "name": "MLP Regressor",
        "category": "ml",
        "description": "Feed-forward neural network trained on scaled features.",
        "uses_covariates": True,
        "needs_training": True,
    },
}


CROATIAN_THESIS_NOTES = {
    "forward_fill": (
        "Metoda forward fill prepisuje posljednju poznatu vrijednost unaprijed u vremenu. "
        "Jednostavna je i brza, ali lošije rekonstruira promjene između udaljenih uzoraka."
    ),
    "linear": (
        "Linearna interpolacija spaja susjedne poznate točke pravcima. "
        "Dobro radi kada serija ima glatke promjene između uzoraka."
    ),
    "time": (
        "Vremenska interpolacija koristi stvarno vremensko razmicanje između točaka. "
        "Posebno je prikladna za neredovite intervale, iako Jena dataset ima regularan interval."
    ),
    "cubic": (
        "Kubna interpolacija koristi polinome trećeg stupnja između poznatih točaka. "
        "Može postići glatke rekonstrukcije, ali ponekad overshoota u naglim promjenama."
    ),
    "spline": (
        "Spline interpolacija koristi spline krivulje trećeg reda. "
        "U praksi je osjetljiva na distribuciju poznatih točaka i rubne uvjete."
    ),
    "random_forest": (
        "Random Forest je ansambl stabala odluke treniran na inženjerski izvedenim značajkama "
        "i pomoćnim meteorološkim varijablama iz Jena dataseta."
    ),
    "mlp": (
        "MLP regresor je jednostavna neuronska mreža koja u ovom radu koristi skalirane značajke "
        "i zahtijeva pažljiv odabir hiperparametara."
    ),
}


ENGLISH_THESIS_NOTES = {
    "forward_fill": "Forward fill repeats the last observed value until the next observation appears.",
    "linear": "Linear interpolation connects known points with straight segments.",
    "time": "Time interpolation weights values according to actual elapsed time.",
    "cubic": "Cubic interpolation fits third-order polynomials between known points.",
    "spline": "Spline interpolation uses piecewise cubic splines between observations.",
    "random_forest": "Random Forest combines many decision trees trained on engineered features.",
    "mlp": "The MLP regressor is a feed-forward neural network trained on scaled features.",
}


def get_croatian_thesis_note(method: str) -> str:
    """Return a Croatian thesis paragraph for a method."""
    return CROATIAN_THESIS_NOTES[method]


def get_english_thesis_note(method: str) -> str:
    """Return an English thesis paragraph for a method."""
    return ENGLISH_THESIS_NOTES[method]


def build_bilingual_method_appendix() -> str:
    """Build bilingual appendix text for all methods."""
    lines = ["# Bilingual method appendix", ""]
    for method in CLASSICAL_METHODS + ML_METHODS:
        info = METHOD_DESCRIPTIONS[method]
        lines.append(f"## {info['name']} (`{method}`)")
        lines.append("")
        lines.append("### Hrvatski")
        lines.append(get_croatian_thesis_note(method))
        lines.append("")
        lines.append("### English")
        lines.append(get_english_thesis_note(method))
        lines.append("")
    return "\n".join(lines)


def get_method_description(method: str) -> dict:
    """Return metadata for a method."""
    if method not in METHOD_DESCRIPTIONS:
        raise KeyError(f"Unknown method: {method}")
    return METHOD_DESCRIPTIONS[method]


def list_methods_with_descriptions() -> list[dict]:
    """Return all methods with metadata."""
    return [
        {"key": key, **value}
        for key, value in METHOD_DESCRIPTIONS.items()
    ]


def classical_method_docs() -> str:
    """Return markdown documentation for classical methods."""
    lines = ["## Classical methods", ""]
    for method in CLASSICAL_METHODS:
        info = METHOD_DESCRIPTIONS[method]
        lines.append(f"### {info['name']} (`{method}`)")
        lines.append("")
        lines.append(info["description"])
        lines.append("")
    return "\n".join(lines)


def ml_method_docs() -> str:
    """Return markdown documentation for ML methods."""
    lines = ["## Machine learning methods", ""]
    for method in ML_METHODS:
        info = METHOD_DESCRIPTIONS[method]
        lines.append(f"### {info['name']} (`{method}`)")
        lines.append("")
        lines.append(info["description"])
        lines.append("")
        lines.append(f"- Uses covariates: {info['uses_covariates']}")
        lines.append(f"- Requires training: {info['needs_training']}")
        lines.append("")
    return "\n".join(lines)


def full_method_catalog_markdown() -> str:
    """Return complete method catalog for thesis appendix notes."""
    return "\n".join([
        "# Method catalog",
        "",
        classical_method_docs(),
        ml_method_docs(),
    ])
