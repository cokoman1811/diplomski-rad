"""Formal experiment protocol descriptions for thesis reproducibility."""

from __future__ import annotations

from dataclasses import dataclass

from .config import (
    ALL_METHODS,
    CLASSICAL_METHODS,
    DEGRADATION_FACTORS,
    ML_METHODS,
    QUICK_DEGRADATION_FACTORS,
    QUICK_SAMPLE_SIZE,
    TEST_START,
    TRAIN_END,
)


@dataclass(frozen=True)
class ProtocolStep:
    """One documented step in the experiment protocol."""

    order: int
    title: str
    description: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]


FULL_PROTOCOL: tuple[ProtocolStep, ...] = (
    ProtocolStep(
        1,
        "Učitavanje podataka",
        "Učitaj Jena Climate CSV iz data/raw/ i provjeri stupce temperature i covariates.",
        ("jena_climate_2009_2016.csv",),
        ("temperature series", "covariate frame"),
    ),
    ProtocolStep(
        2,
        "Sezonska podjela",
        f"Treniraj na podacima do {TRAIN_END}, evaluiraj uklonjene točke od {TEST_START}.",
        ("datetime index",),
        ("train_mask", "test_mask"),
    ),
    ProtocolStep(
        3,
        "Degradacija",
        "Za svaki faktor zadrži svaki n-ti uzorak; ostalo označi kao missing.",
        ("degradation factor",),
        ("degraded series", "removed_mask"),
    ),
    ProtocolStep(
        4,
        "Rekonstrukcija",
        "Primijeni klasične metode ili treniraj ML modele na train dijelu.",
        ("method name", "features"),
        ("reconstructed series",),
    ),
    ProtocolStep(
        5,
        "Evaluacija",
        "Izračunaj MAE, RMSE i R² samo na uklonjenim točkama u testnom razdoblju.",
        ("original", "reconstructed", "removed_mask"),
        ("metrics dict",),
    ),
    ProtocolStep(
        6,
        "Izvoz",
        "Spremi tablice u results/tables/ i figure u results/figures/.",
        ("results dataframe",),
        ("csv files", "png figures"),
    ),
)


def list_protocol_steps() -> list[ProtocolStep]:
    """Return ordered protocol steps."""
    return list(FULL_PROTOCOL)


def protocol_markdown() -> str:
    """Render the full protocol as markdown."""
    lines = ["# Protokol eksperimenta", ""]
    for step in FULL_PROTOCOL:
        lines.append(f"## {step.order}. {step.title}")
        lines.append("")
        lines.append(step.description)
        lines.append("")
        lines.append(f"- Ulazi: {', '.join(step.inputs)}")
        lines.append(f"- Izlazi: {', '.join(step.outputs)}")
        lines.append("")
    return "\n".join(lines)


def quick_run_protocol_summary() -> str:
    """Describe the reduced quick experiment configuration."""
    factors = ", ".join(str(f) for f in QUICK_DEGRADATION_FACTORS)
    return (
        f"Brzi run koristi zadnjih {QUICK_SAMPLE_SIZE} uzoraka, faktore {factors} "
        f"i sve metode ({len(ALL_METHODS)} ukupno) bez produženog GridSearch-a."
    )


def full_run_protocol_summary() -> str:
    """Describe the full experiment configuration."""
    factors = ", ".join(str(f) for f in DEGRADATION_FACTORS)
    return (
        f"Puni run evaluira faktore {factors}, "
        f"{len(CLASSICAL_METHODS)} klasičnih i {len(ML_METHODS)} ML metoda "
        f"s opcionalnim hiperparametarskim podešavanjem."
    )


def validate_protocol_methods(methods: list[str]) -> list[str]:
    """Return unknown method names from a custom protocol list."""
    known = set(ALL_METHODS)
    return [method for method in methods if method not in known]
