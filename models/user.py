import mongoengine as me

class User(me.Document):

    class JoinSource(object):
        FACEBOOK = 1

    meta = {
        'indexes': [
            'fb_access_token',
            'fbid',
        ],
    }

    # id = me.ObjectIdField(primary_key=True)

    # TODO(mack): join_date should be encapsulate in _id, but store it
    # for now, just in case; can remove it when sure that info is in _id
    join_time = me.DateTimeField(required=True)
    join_source = me.IntField(required=True, choices=[JoinSource.FACEBOOK])

    # eg. Mack (can include middle name)
    first_name = me.StringField(required=True)

    # eg. Duan
    last_name = me.StringField(required=True)

    # eg. 1647810326
    fbid = me.StringField(required=True, unique=True)

    # http://stackoverflow.com/questions/4408945/what-is-the-length-of-the-access-token-in-facebook-oauth2
    fb_access_token = me.StringField(max_length=255, required=True, unique=True)
    fb_access_token_expiry_time = me.DateTimeField(required=True)

    email = me.EmailField()

    # eg. list of user objectids, could be friends from sources besides facebook
    friend_ids = me.ListField(me.ObjectIdField())
    # eg. list of fbids of friends from facebook, not necessarily all of whom
    # use the site
    friend_fbids = me.ListField(me.StringField())

    birth_date = me.DateTimeField()

    last_login_time = me.DateTimeField()
    # TODO(mack): consider using SequenceField()
    num_visits = me.IntField(min_value=0, default=0)

    # eg. mduan or 20345619 ?
    student_id = me.StringField()
    # eg. university_of_waterloo ?
    school_id = me.StringField()
    # eg. software_engineering ?
    program_id = me.StringField()


    @property
    def name(self):
        return '%s %s' % (self.first_name , self.last_name)

    def add_friend_fbids(self, fbids):
        new_fbids = set(fbids) - set(self.friend_fbids)
        self.friend_fbids.extend(new_fbids)
        friend_ids = [u.id for u in User.objects(fbid__in=new_fbids).only('id')]
        self.friend_ids.extend(friend_ids)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)