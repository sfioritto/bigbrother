import bigbrother.webapp.model as model

def test_build_raw_data():
    environ = {"HTTP_test": "lolz",
               "fake": "oops"}
    partial = {"part": "one"}
    ip = "192.168.1.1"
    rd = dict(model.build_raw_data(partial, environ, ip))
    assert rd["part"] == "one"
    assert rd["HTTP_test"] == "lolz"
    assert not rd.has_key("fake")

def test_get_whorls():
    test_create_get_whorls() #creates some whorls to get
    assert False

def test_create_get_whorls():
    assert False


def test_create_hashes():

    whorls = {
        "test": "basic",
        "list": [{1:2, 3:4}, {"a": "b"}],
        "dict": {5:6, 7:8,
                  9:{"deep": 6}}
        }

    hashes = dict([(key, value) for key, value, hashed in model.create_hashes(whorls)])

    assert hashes["test"] == "basic"
    assert hashes["list:1"] == "2"
    assert hashes["list:3"] == "4"
    assert hashes["list:a"] == "b"
    assert hashes["dict:5"] == "6"
    assert hashes["dict:7"] == "8"
    assert hashes["dict:9:deep"] == "6"
    

