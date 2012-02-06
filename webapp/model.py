from hashlib import sha512

def create_hashes(whorls, prefix=None):
    
    hashes = []

    for key, value in whorls.items():
                    
        if prefix:
            key = prefix + ":" + key

        if type(value) == dict:
            hashes.extend(create_hashes(value, prefix=key))            
            
        elif type(value) == list:
            for item in value:
                hashes.extend(create_hashes(item, prefix=key))
                
        else:
            
            if type(value) != unicode:
                value = unicode(value)

            hashes.append((key,
                            value,
                            sha512((key + value).encode("utf-8")).hexdigest()))
            
    return hashes


def learn(whorls, identity):
    
    """
    increment the count for whorlID probability, whorl, total_visits
    and identity.
    """

    db = web.ctx.db
    identity.count = identity.count + 1
    total_visits = db.query(Stat).filter_by(key="total_visits").one()
    total_visits.value = total_visits.value + 1

    for whorl in whorls:
        whorl.count = whorl.count + 1
        try:
            wgi = db.query(WhorlIdentity).\
                filter_by(whorl_hashed=whorl.hashed).\
                filter_by(identity_id=identity.id).\
                one()
            wgi.count = wgi.count + 1
            
        except NoResultFound:
            wgi = WhorlIdentity(whorl_hashed=whorl.hashed,
                                     identity_id = identity.id)
            db.add(wgi)
            db.flush()
                
def identify_from(whorls):

    db = web.ctx.db
    stats = stats_obj(db)
    minprob = float(1) / stats["total_visits"]
    whorl_hashes = list(set([whorl.hashed for whorl in whorls]))

    # this is a dictionary of dictionaries. The inner dictionaries
    # contain probabilities of the whorl given the user.
    whorlids = defaultdict(lambda : defaultdict(lambda : minprob))
    for wid in db.query(WhorlIdentity).\
        filter(WhorlIdentity.whorl_hashed.in_(whorl_hashes)).\
        all():

        whorlids[wid.identity][wid.whorl_hashed] =\
            min(1, float(wid.count) / wid.identity.count)

    # The probabilities above are then used to create a list
    # of probabilities per user for every whorl passed in.
    # The inner dictionary above defaults to a reasonable
    # minimum if we've never seen a whorl for a given user
    givenid = defaultdict(list)
    for identity, idprobs in whorlids.items():
        for whorl in whorls:
            givenid[identity].append(idprobs[whorl.hashed])

    # These are all the probabilities put into a list of tuples so
    # it can be sorted by probability.
    probs = [(\
               # calculate the posterior probability p(whorl|identity)p(identity)
               reduce(mul, idprobs) * (float(identity.count) / stats["total_visits"]),\

               # identity id as a tie breaker in sorting. this is arbitrary. If there
               # is a tie, we just guess. could put a random number here I suppose.
               identity.id,\

               # the identity tied to this probability.
               identity) \
               
               for identity, idprobs in givenid.items()]

    probs.sort()
    return probs[-1][2] # the most likely identity (third element is the identity)

