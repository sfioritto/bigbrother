from fabric.api import *

env.hosts = ['nymbus.org']
env.approot = "/var/nymbus/www"
env.prodhome = "/var/nymbus"


def test():
    # run tests here if you got 'em
    # local("nosetests tests/")
    pass


def pack(hash):

    """
    Creates a clean copy of the code
    """
    archivename = "%s.tar.gz" % hash
    local("git archive --format=tar %s | gzip > /tmp/%s;" % (hash, archivename))
    return archivename


def prepare(hash):

    """
    Test and archive postosaurus.
    """

    test()
    pack(hash)


def upload(archive):
    put('/tmp/%s' % archive, '/tmp/')


def untar(archive, hash):
    with settings(warn_only=True):
        with cd(env.prodhome):
            sudo("rm -rf snapshots/%s" % hash)
            sudo("mkdir snapshots/%s" % hash)
            sudo("cd snapshots/%s; tar -xvf '/tmp/%s'" % (hash,archive))


def upload_untar(archive, hash):
    upload(archive)
    untar(archive, hash)


def switch(hash):
    with cd(env.prodhome):
        sudo("ln -s %s/snapshots/%s/webapp /tmp/live_tmp && sudo mv -Tf /tmp/live_tmp %s" % (env.prodhome, hash, env.approot))
        with settings(warn_only=True):
            sudo("rm bigbrother")
        sudo("ln -s %s/snapshots/%s bigbrother" % (env.prodhome, hash))
        sudo("ln -s %s/config.json %s/bigbrother/config/config.json" % (env.prodhome, env.prodhome))


def stop():
    #TODO: this will break when there are multiple hosts, need to dynamically lookup uid and gid
    #This assert makes sure I know when it breaks
    assert len(env.hosts) == 1, "This script only works with one host."

    with settings(warn_only=True):
        sudo("/etc/init.d/nginx stop")
        run('kill `pgrep -f "python /var/nymbus/www/prod.py"`')
        #todo: stop fcgi processes


def start():
    #TODO: this will break when there are multiple hosts, need to dynamically lookup uid and gid
    #This assert makes sure I know when it breaks
    assert len(env.hosts) == 1, "This script only works with one host"

    with settings(warn_only=True):
        sudo("/etc/init.d/nginx start")
        run("spawn-fcgi -d /var/nymbus/www -f /var/nymbus/www/prod.py -a 127.0.0.1 -p 9002 -F 10")


def reboot():
    stop()
    start()

    
def deploy(hash):
    
    test()
    archive = pack(hash)
    upload(archive)
    untar(archive, hash)
    switch(hash)
