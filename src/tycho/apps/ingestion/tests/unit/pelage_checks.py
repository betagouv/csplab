"""Custom pelage checks for corps cleaning validation."""

import pelage as plg
import polars as pl


def has_valid_decree_format(df: pl.DataFrame, column: str) -> pl.DataFrame:
    """Check that decree IDs have valid format (YYYY-NNNN or YY-NNNN)."""
    pattern = r"^\d{2,4}-\d+$"

    invalid_decrees = df.filter(
        pl.col(column).is_not_null() & ~pl.col(column).str.contains(pattern)
    )

    if len(invalid_decrees) > 0:
        raise plg.PolarsAssertError(
            invalid_decrees.select(column),
            f"Column '{column}' contains invalid decree formats",
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


def has_only_fpe_type(df: pl.DataFrame, column: str = "fp_type") -> pl.DataFrame:
    """Check that only FPE type is present."""
    non_fpe_rows = df.filter(pl.col(column) != "FPE")

    if len(non_fpe_rows) > 0:
        raise plg.PolarsAssertError(
            non_fpe_rows.select(column),
            f"Found non-FPE types in column '{column}' - should be filtered out",
        )

    return df


def has_valid_category_mapping(
    df: pl.DataFrame, column: str = "category"
) -> pl.DataFrame:
    """Check that category values are properly mapped."""
    valid_categories = ["A", "B", "C"]
    invalid_categories = df.filter(
        pl.col(column).is_not_null() & ~pl.col(column).is_in(valid_categories)
    )

    if len(invalid_categories) > 0:
        raise plg.PolarsAssertError(
            invalid_categories.select(column),
            f"Column '{column}' contains invalid category values",
        )

    return df
