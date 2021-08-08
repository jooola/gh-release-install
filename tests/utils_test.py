from gh_release_install.utils import Log


def test_log(capsys):
    Log.set_level(1)

    Log.info("hello")
    Log.error("hello")
    Log.debug("hello")

    Log.set_level(2)
    Log.debug("nope")

    captured = capsys.readouterr()
    assert captured.out == ("info: hello\n" "error: hello\n" "debug: nope\n")
