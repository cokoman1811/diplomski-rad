"""Thesis chapter skeletons and methodology text generators."""

from __future__ import annotations

import pandas as pd

from .analysis import best_method_per_factor, build_method_leaderboard, compare_classical_vs_ml
from .config import CLASSICAL_METHODS, DEGRADATION_FACTORS, ML_METHODS, TEMPERATURE_COLUMN
from .method_info import build_bilingual_method_appendix

CHAPTER_TITLES_HR = {
    1: "Uvod",
    2: "Pregled literature",
    3: "Metodologija",
    4: "Rezultati i analiza",
    5: "Zaključak",
}

METHODOLOGY_SECTIONS_HR = [
    "Opis dataseta i varijabli",
    "Procedura umjetne degradacije podataka",
    "Klasične metode interpolacije",
    "Metode strojnog učenja",
    "Metrike evaluacije",
    "Statistička usporedba metoda",
]

EXPERIMENT_STEPS_HR = [
    "Učitavanje visokorezolucijskog vremenskog niza temperature iz Jena Climate dataseta.",
    "Podjela podataka na razdoblje treniranja i testno razdoblje (2015–2016).",
    "Umjetna degradacija zadržavanjem svakog n-tog uzorka za faktore 2, 3, 6 i 12.",
    "Rekonstrukcija uklonjenih vrijednosti klasičnim metodama i modelima strojnog učenja.",
    "Evaluacija točnosti na uklonjenim vrijednostima u testnom razdoblju.",
    "Statistička analiza razlika između metoda i izvoz tablica te figura.",
]


def generate_chapter_outline() -> str:
    """Return a markdown outline for all thesis chapters."""
    lines = ["# Struktura rada", ""]
    for number, title in CHAPTER_TITLES_HR.items():
        lines.append(f"{number}. {title}")
    lines.append("")
    lines.append("## Poglavlje 3 — podpoglavlja")
    for section in METHODOLOGY_SECTIONS_HR:
        lines.append(f"- {section}")
    return "\n".join(lines)


def generate_dataset_description() -> str:
    """Return Croatian dataset description paragraph."""
    return (
        f"Glavni dataset u ovom radu je Jena Climate dataset, visokorezolucijski "
        f"meteorološki vremenski niz. Ciljana varijabla je temperatura (`{TEMPERATURE_COLUMN}`), dok se "
        f"kao pomoćne (covariate) varijable koriste tlak, relativna vlažnost i brzina vjetra. "
        f"Podaci pokrivaju više godina kontinuiranog mjerenja u regularnom vremenskom intervalu."
    )


def generate_degradation_description() -> str:
    """Return Croatian degradation procedure description."""
    factors = ", ".join(str(factor) for factor in DEGRADATION_FACTORS)
    return (
        "Umjetna degradacija simulira rijetko uzorkovanje zadržavanjem svakog n-tog "
        f"promatranja. U eksperimentu su korišteni faktori {factors}. "
        "Sve vrijednosti koje nisu zadržane tretiraju se kao nedostajuće i moraju se "
        "rekonstruirati odabranim metodom interpolacije ili strojnog učenja."
    )


def generate_evaluation_description() -> str:
    """Return Croatian evaluation metrics description."""
    return (
        "Točnost rekonstrukcije procjenjuje se isključivo na uklonjenim vrijednostima "
        "u testnom razdoblju. Koriste se metrike srednja apsolutna pogreška (MAE), "
        "korijen srednje kvadratne pogreške (RMSE) i koeficijent determinacije (R²). "
        "Time se osigurava objektivna usporedba metoda na istim točkama gdje su "
        "vrijednosti namjerno uklonjene."
    )


def generate_methodology_chapter() -> str:
    """Build full methodology chapter draft in Croatian."""
    sections = [
        "# Metodologija",
        "",
        "## Dataset",
        generate_dataset_description(),
        "",
        "## Degradacija podataka",
        generate_degradation_description(),
        "",
        "## Klasične metode",
        f"Implementirane klasične metode: {', '.join(CLASSICAL_METHODS)}.",
        "",
        "## Metode strojnog učenja",
        f"Implementirane ML metode: {', '.join(ML_METHODS)}.",
        "",
        "## Evaluacija",
        generate_evaluation_description(),
        "",
        "## Koraci eksperimenta",
    ]
    for index, step in enumerate(EXPERIMENT_STEPS_HR, start=1):
        sections.append(f"{index}. {step}")
    return "\n".join(sections)


def generate_results_discussion(results: pd.DataFrame) -> str:
    """Generate Croatian results discussion from an experiment table."""
    if results.empty:
        return "Rezultati eksperimenta nisu dostupni."

    best = best_method_per_factor(results)
    leaderboard = build_method_leaderboard(results)
    classical_vs_ml = compare_classical_vs_ml(results)

    lines = [
        "# Rezultati i analiza",
        "",
        "## Sažetak performansi",
        f"Analizirano je {len(results)} kombinacija metode i faktora degradacije.",
        f"Najbolji prosječni rang prema leaderboardu ima metoda `{leaderboard.iloc[0]['method']}`.",
        "",
        "## Najbolja metoda po faktoru",
    ]
    for _, row in best.iterrows():
        lines.append(
            f"- Faktor {int(row['factor'])}: `{row['method']}` "
            f"(MAE = {row['mae']:.4f}, RMSE = {row['rmse']:.4f}, R² = {row['r2']:.4f})"
        )

    lines.extend(["", "## Klasične metode naspram strojnog učenja"])
    for factor in sorted(classical_vs_ml["factor"].unique()):
        factor_rows = classical_vs_ml[classical_vs_ml["factor"] == factor]
        classical = factor_rows[factor_rows["group"] == "classical"]
        ml = factor_rows[factor_rows["group"] == "ml"]
        if classical.empty or ml.empty:
            continue
        lines.append(
            f"- Faktor {int(factor)}: klasične MAE = {classical.iloc[0]['mean']:.4f}, "
            f"ML MAE = {ml.iloc[0]['mean']:.4f}"
        )
    return "\n".join(lines)


def generate_conclusion_paragraphs(results: pd.DataFrame | None = None) -> list[str]:
    """Return Croatian conclusion paragraphs."""
    paragraphs = [
        "U radu je uspoređena točnost rekonstrukcije temperature nakon umjetne degradacije "
        "podataka klasičnim metodama interpolacije i odabranim modelima strojnog učenja.",
        "Eksperimentalni okvir omogućuje ponovljivu evaluaciju na istim uklonjenim točkama "
        "u testnom razdoblju, što olakšava objektivnu usporedbu metoda.",
    ]
    if results is not None and not results.empty:
        best = best_method_per_factor(results)
        top = best.iloc[0]
        paragraphs.append(
            f"Prema dobivenim rezultatima, metoda `{top['method']}` postigla je najbolju "
            f"MAE za faktor {int(top['factor'])}, što ukazuje na njezinu robusnost u "
            f"promatranom scenariju."
        )
    paragraphs.append(
        "Budući rad može proširiti usporedbu dodatnim metodama, drugim meteorološkim "
        "varijablama ili drugačijim shemama degradacije podataka."
    )
    return paragraphs


def generate_introduction_paragraphs() -> list[str]:
    """Return Croatian introduction paragraphs."""
    return [
        "Vremenske serije visoke frekvencije često se u praksi pojavljuju u rijetko "
        "uzorkovanom obliku zbog ograničenja prijenosa, pohrane ili senzora.",
        "Interpolacija nedostajućih vrijednosti klasičnim metodama široko je korištena, "
        "ali modeli strojnog učenja mogu iskoristiti dodatne varijable i nelinearne obrasce.",
        "Cilj ovog rada je sustavno usporediti obje grupe metoda na istom eksperimentu "
        "s umjetno uklonjenim vrijednostima temperature iz Jena Climate dataseta.",
    ]


def generate_literature_outline() -> str:
    """Return literature review bullet outline."""
    topics = [
        "Klasične metode interpolacije vremenskih serija",
        "Forward fill i piecewise linearne metode",
        "Spline i polinomna interpolacija",
        "Strojno učenje za predikciju i imputaciju",
        "Random Forest i neuronske mreže u regresiji",
        "Metrike MAE, RMSE i R² u evaluaciji modela",
        "Statistički testovi za usporedbu više metoda",
    ]
    lines = ["# Pregled literature — predložena struktura", ""]
    for topic in topics:
        lines.append(f"- {topic}")
    return "\n".join(lines)


def build_full_thesis_skeleton(results: pd.DataFrame | None = None) -> str:
    """Assemble a full thesis skeleton with optional results section."""
    parts = [
        generate_chapter_outline(),
        "",
        "---",
        "",
        "# Uvod",
        "",
        "\n\n".join(generate_introduction_paragraphs()),
        "",
        "---",
        "",
        generate_literature_outline(),
        "",
        "---",
        "",
        generate_methodology_chapter(),
        "",
        "---",
        "",
        build_bilingual_method_appendix(),
    ]
    if results is not None and not results.empty:
        parts.extend(["", "---", "", generate_results_discussion(results)])
    parts.extend([
        "",
        "---",
        "",
        "# Zaključak",
        "",
        "\n\n".join(generate_conclusion_paragraphs(results)),
    ])
    return "\n".join(parts)


def list_methodology_sections() -> list[str]:
    """Return methodology section titles."""
    return list(METHODOLOGY_SECTIONS_HR)


def list_experiment_steps() -> list[str]:
    """Return ordered experiment steps."""
    return list(EXPERIMENT_STEPS_HR)
