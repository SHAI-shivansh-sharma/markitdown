import io

from markitdown import MarkItDown, StreamInfo


def test_extensionless_log_text_is_not_rendered_as_csv_table() -> None:
    content = (
        "2026-09-12 18:00:01 INFO boot ok\n" "2026-09-12 18:00:02 ERROR disk full\n"
    )

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content.encode("utf-8"))
    )

    assert result.markdown == content


def test_extensionless_comma_csv_is_still_rendered_as_table() -> None:
    content = "name,age\nAlice,30\n"

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content.encode("utf-8"))
    )

    assert result.markdown == "| name | age |\n| --- | --- |\n| Alice | 30 |"


def test_explicit_csv_mimetype_keeps_single_column_csv() -> None:
    content = b"name\nAlice\nBob\n"

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content), stream_info=StreamInfo(mimetype="application/csv")
    )

    assert result.markdown == "| name |\n| --- |\n| Alice |\n| Bob |"


def test_log_extension_without_delimiters_stays_plain_text() -> None:
    content = b"2026-09-12 18:00:01 INFO boot ok\n2026-09-12 18:00:02 ERROR disk full\n"

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content), stream_info=StreamInfo(extension=".log")
    )

    assert result.markdown == content.decode()
