"""Custom pelage checks for corps cleaning validation."""

import pelage as plg
import polars as pl


def has_only_fpe_type(df: pl.DataFrame, column: str = "fp_type") -> pl.DataFrame:
    """Check that only FPE type is present."""
    non_fpe_rows = df.filter(pl.col(column) != "FPE")

    if len(non_fpe_rows) > 0:
        raise plg.PolarsAssertError(
            non_fpe_rows.select(column),
            f"Found non-FPE types in column '{column}' - should be filtered out",
        )

    return df


def has_no_minarm_ministry(df: pl.DataFrame, column: str = "ministry") -> pl.DataFrame:
    """Check that no MINARM ministry is present (should be filtered out)."""
    minarm_rows = df.filter(pl.col(column) == "MINARM")

    if len(minarm_rows) > 0:
        raise plg.PolarsAssertError(
            minarm_rows.select(column),
            f"Found MINARM ministry in column '{column}' - should be filtered out",
        )

    return df


def has_only_civil_servants(
    df: pl.DataFrame, column: str = "population"
) -> pl.DataFrame:
    """Check that no MINARM ministry is present (should be filtered out)."""
    minarm_rows = df.filter(pl.col(column) == "MINARM")

    if len(minarm_rows) > 0:
        raise plg.PolarsAssertError(
            minarm_rows.select(column),
            f"Found MINARM ministry in column '{column}' - should be filtered out",
        )

    return df
