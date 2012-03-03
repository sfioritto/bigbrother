import bigbrother.webapp.model as model
from google.appengine.ext import testbed
from google.appengine.ext import db
from google.appengine.datastore import datastore_stub_util
from nose.tools import with_setup


class TestModels(object):
    
    def setup(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
        self.testbed.init_datastore_v3_stub(consistency_policy=policy)    
        
    def teardown(self):
        self.testbed.deactivate()

    def test_build_raw_data(self):
        environ = {"HTTP_test": "lolz",
                   "fake": "oops"}
        partial = {"part": "one",
                   "name": "sean"}
        ip = "192.168.1.1"
        rd = dict(model.build_raw_data(partial, environ, ip))
        assert rd["part"] == "one"
        assert rd["HTTP_test"] == "lolz"
        assert not rd.has_key("fake")
        return rd

    
    def test_get_whorls(self):
        rd = self.test_build_raw_data()
        self.test_create_get_whorls() #creates some whorls to get
        whorls = model.get_whorls(rd)
        assert len(whorls) == 4
        return whorls
    

    def test_create_get_whorls(self):
        rd = self.test_build_raw_data()
        whorls = model.create_get_whorls(rd)
        assert len(whorls) == 4
        return whorls
    
    
    def test_create_hashes(self):

        whorls = {
            "test": "basic",
                    "list": [{1:2, 3:4}, {"a": "b"}],
                  "dict": {5:6, 7:8,
                            9:{"deep": 6}}}

        hashes = dict([(key, value) for key, value, hashed in model.create_hashes(whorls)])

        assert hashes["test"] == "basic"
        assert hashes["list:1"] == "2"
        assert hashes["list:3"] == "4"
        assert hashes["list:a"] == "b"
        assert hashes["dict:5"] == "6"
        assert hashes["dict:7"] == "8"
        assert hashes["dict:9:deep"] == "6"
    
    def test_learn(self, identity=None, whorls=None):
        whorls = self.test_create_get_whorls()
        identity = identity or self.test_create_identity()
        model.learn(whorls, identity)
        for whorl in whorls:
            assert whorl.count >= 1, "Count is actually %s" % whorl.count

        return whorls, identity


    def test_create_identity(self):
        u1 = model.create_identity("sean fioritto")
        assert u1.name == "sean fioritto", "expected 'sean fioritto', name is actually %s" % u1.name
        u2 = model.create_identity("sean fioritto")
        assert u2.id > u1.id, "expected id to be less than %s, id is actually" % (u1.id, u2.id)
        return u2


    def test_stats_obj(self):
        stats = model.stats_obj(Session())
        assert stats["total_visits"] == 0


    def test_identify_from(self):
        
        whorls, identity1 = self.test_learn()
        whorls, identity2 = self.test_learn()
        whorls, identity2 = self.test_learn(identity2, whorls)
        assert model.identify_from(whorls) is identity2
        assert model.identify_from(whorls) is not identity1
	
        
    def test_get_whorl_identities(self):
	
        whorls, identity = self.test_learn()
        wis = model.get_whorl_identities(whorls, identity)
        assert len(wis) == 4

