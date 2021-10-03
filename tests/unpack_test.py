from pathlib import Path

from gh_release_install.unpack import _unpack_bz2

here = Path(__file__).parent


def test_unpack_bz2(tmp_path):
    src = Path(here / "fixtures/test.txt.bz2")
    dest = Path(tmp_path / "test.txt")

    _unpack_bz2(src, tmp_path)

    assert dest.is_file
    assert dest.read_text(encoding="utf-8") == "Hello World\n"
