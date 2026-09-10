from infrastructure.gateways.transcoding import (
    SourceTranscoder,
    load_transcoders_by_slug,
)


def test_transcoder_translates_known_code(tmp_path):
    (tmp_path / "types_de_contrat.csv").write_text(
        "intitule;code_client;mappe_sur_code_client_dgafp\n"
        "CDI;CDI;NAT_TITULAIRE_CONTRACTUEL\n",
        encoding="utf-8",
    )

    transcoder = SourceTranscoder.from_directory(tmp_path)

    assert (
        transcoder.translate("types_de_contrat", "CDI") == "NAT_TITULAIRE_CONTRACTUEL"
    )


def test_transcoder_returns_none_for_unknown_code(tmp_path):
    (tmp_path / "types_de_contrat.csv").write_text(
        "intitule;code_client;mappe_sur_code_client_dgafp\n"
        "CDI;CDI;NAT_TITULAIRE_CONTRACTUEL\n",
        encoding="utf-8",
    )

    transcoder = SourceTranscoder.from_directory(tmp_path)

    assert transcoder.translate("types_de_contrat", "UNKNOWN") is None


def test_transcoder_returns_none_for_unknown_field(tmp_path):
    transcoder = SourceTranscoder.from_directory(tmp_path)

    assert transcoder.translate("types_de_contrat", "CDI") is None


def test_transcoder_ignores_csv_without_target_column(tmp_path):
    (tmp_path / "regions.csv").write_text(
        "intitule;code_client;some_other_column\nBretagne;ARS_CO_Region_Bretagne;R53\n",
        encoding="utf-8",
    )

    transcoder = SourceTranscoder.from_directory(tmp_path)

    assert transcoder.translate("regions", "ARS_CO_Region_Bretagne") is None


def test_load_transcoders_by_slug_discovers_ars_directory():
    transcoders = load_transcoders_by_slug()

    assert "ars" in transcoders
    assert (
        transcoders["ars"].translate("types_de_contrat", "TC02")
        == "TITULAIRE_CONTRACTUEL"
    )
