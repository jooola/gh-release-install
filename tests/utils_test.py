from gh_release_install.utils import Log


def test_log(capsys):
    Log.level = 2

    Log.info("hello")
    Log.error("hello")
    Log.debug("hello")

    Log.level = 3
    Log.debug("nope")

    captured = capsys.readouterr()
    assert captured.out == ("info: hello\n" "error: hello\n" "debug: nope\n")
