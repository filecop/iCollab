from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy() #Instance of SQLAlchemy


class Status(db.Model):
    __tablename__="status"
    statusid=db.Column(db.Integer, primary_key=True)
    statusname=db.Column(db.String(10),nullable=False, unique=True)

class Roles(db.Model):
    __tablename__="roles"
    roleid=db.Column(db.Integer, primary_key=True)
    rolename=db.Column(db.String(20),nullable=False, unique=True)
    
class UserType(db.Model):
    __tablename__="userType"
    usertypeid=db.Column(db.Integer, primary_key=True)
    usertypename=db.Column(db.String(50),nullable=False, unique=True)

class Platforms(db.Model):
    __tablename__="platforms"
    platformid=db.Column(db.Integer, primary_key=True)
    platformname=db.Column(db.String(50), nullable=False, unique=True)

class Industries(db.Model):
    __tablename__="industries"
    industryid=db.Column(db.Integer, primary_key=True)
    industryname=db.Column(db.String(50), nullable=False, unique=True)


class AdRequests(db.Model):
    __tablename__="adrequests"
    adrequestid=db.Column(db.Integer,primary_key=True)
    adtitle=db.Column(db.String(25))
    campaignid=db.Column(db.Integer,db.ForeignKey("campaigns.campaignid"),nullable=False)
    influencerid=db.Column(db.Integer,db.ForeignKey("userinfo.userid"))
    requirements=db.Column(db.String(1000))
    paymentamount=db.Column(db.Integer)
    adprogress=db.Column(db.Float, default=0)
    adtargetreach=db.Column(db.Integer, default=0)
    isactive=db.Column(db.Boolean, default=True)
    ispublic=db.Column(db.Boolean, default=False)
    isflagged=db.Column(db.Boolean, default=False)
    isblacklisted=db.Column(db.Boolean, default=False)
    isassigned=db.Column(db.Boolean, default=False)
    reportreason=db.Column(db.String(1000))
    negotiations = db.relationship('Negotiations', backref='adrequests', lazy=True, cascade="all, delete, delete-orphan")



class UserInfo(db.Model):
    __tablename__="userinfo"
    userid=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    fullname=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    role=db.Column(db.Integer,db.ForeignKey("roles.roleid"),default=2)
    usertype=db.Column(db.String(50),db.ForeignKey("userType.usertypename"),nullable=True)
    isprofilepublic=db.Column(db.Boolean, default=True)
    isactive=db.Column(db.Boolean, default=True)
    isflagged=db.Column(db.Boolean, default=False)
    isblacklisted=db.Column(db.Boolean, default=False)
    campaign=db.relationship('Campaigns', backref='userinfo', lazy=True)
    platformpresence=db.relationship('PlatformPresence',backref='userinfo', lazy=True)
    adrequests=db.relationship('AdRequests',backref='userinfo', lazy=True)
    sent_messages = db.relationship('Messages', foreign_keys='Messages.senderid', backref='sender_user', lazy=True)
    received_messages = db.relationship('Messages', foreign_keys='Messages.receiverid', backref='receiver_user', lazy=True)



# class Influencers(db.Model):
#     __tablename__="influencers"
#     influencerid=db.Column(db.Integer,primary_key=True)
#     influencerusername=db.Column(db.String(50),db.ForeignKey("userInfo.username"),nullable=False)
#     influencercategory=db.Column(db.String(50),db.ForeignKey("categories.categoryname"),nullable=False),nullable=False)
#     influencerniche=db.Column(db.String(1000))
#     influencerreach=db.Column(db.Integer)

# class Sponsors(db.Model):
#     __tablename__="sponsors"
#     sponsorid=db.Column(db.Integer,primary_key=True)
#     sponsorusername=db.Column(db.String(50),db.ForeignKey("userInfo.username"),nullable=False)
#     sponsorcategory=db.Column(db.String(50),db.ForeignKey("categories.categoryname"),nullable=False)
#     sponsorbudget=db.Column(db.Integer)


# class PlatformPresence(db.Model):
#     __tablename__="platformPresence"
#     platformpresenceid=db.Column(db.Integer, primary_key=True)
#     username=db.Column(db.String(50), db.ForeignKey("userInfo.username"),nullable=False)
#     platformname=db.Column(db.String(50), db.ForeignKey("platforms.platformname"))


class Campaigns(db.Model):
    __tablename__="campaigns"
    campaignid=db.Column(db.Integer,primary_key=True)
    campaignname=db.Column(db.String(50),nullable=False,unique=True)
    campaigndescription=db.Column(db.String(1000))
    campaignstartdate=db.Column(db.String(10))
    campaignenddate=db.Column(db.String(10))
    campaignbudget=db.Column(db.Integer)
    ispublic=db.Column(db.Boolean, default=False)
    campaigngoals=db.Column(db.String(1000))
    iscampaignactive=db.Column(db.Boolean, default=True)
    iscampaignflagged=db.Column(db.Boolean, default=False) #After approval, will be Blacklisted or Whitelisted
    iscampaignblacklisted=db.Column(db.Boolean, default=False)
    campaigntargetaudience=db.Column(db.Integer, db.ForeignKey("categories.categoryid"))
    campaigntargetreach=db.Column(db.Integer)
    campaignprogress=db.Column(db.Float, default=0)
    campaigncreatedon=db.Column(db.String(50))
    campaigncreatedby=db.Column(db.Integer,db.ForeignKey("userinfo.userid"),nullable=False)
    reportreason=db.Column(db.String(1000))
    adRequests=db.relationship('AdRequests', backref='campaigns', lazy=True, cascade="all, delete-orphan")


class PlatformPresence(db.Model):
    __tablename__="platformpresence"
    platformpresenceid=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), db.ForeignKey("userinfo.username"),nullable=False)
    platformname=db.Column(db.String(50), db.ForeignKey("platforms.platformname"))



class Messages(db.Model):
    __tablename__="messages"
    messageid=db.Column(db.Integer, primary_key=True)
    conversationid=db.Column(db.Integer,db.ForeignKey("conversation.conversationid"),nullable=False)
    senderid=db.Column(db.Integer, db.ForeignKey("userinfo.userid"),nullable=False)
    receiverid=db.Column(db.Integer, db.ForeignKey("userinfo.userid"),nullable=False)
    message=db.Column(db.String(1000))
    messagesentdate=db.Column(db.DateTime)
    messageseen=db.Column(db.Boolean, default=False)




class Category(db.Model):
    __tablename__ = 'categories'
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(50), unique=True, nullable=False)
    categorydescription = db.Column(db.String(255))
    niches = db.relationship('Niches', backref='category', lazy=True)
    campaigncategory=db.relationship('Campaigns', backref='cate', lazy=True)
    influecer=db.relationship('Influencers', backref='cate', lazy=True)


class Niches(db.Model):
    __tablename__ = 'niches'
    nicheid = db.Column(db.Integer, primary_key=True)
    nichename = db.Column(db.String(50), unique=True, nullable=False)
    nichedescription = db.Column(db.String(255))
    categoryid = db.Column(db.Integer, db.ForeignKey('categories.categoryid'), nullable=False)
    influencers = db.relationship('Influencers', backref='niches', lazy=True)


class Influencers(db.Model):
    __tablename__ = 'influencers'
    influencerid = db.Column(db.Integer, primary_key=True)
    influencerusername = db.Column(db.String(50), db.ForeignKey("userinfo.username"), nullable=False)
    influencerdescription = db.Column(db.String(255))
    influencercategory = db.Column(db.String(50), db.ForeignKey('categories.categoryname'), nullable=False)
    influencerniche = db.Column(db.String(50), db.ForeignKey('niches.nichename'), nullable=False)
    influencerreach = db.Column(db.Integer)
    influencerearnings=db.Column(db.Integer)
    influencertenure=db.Column(db.Float, default=0.1)
    ispublic=db.Column(db.Boolean, default=False)
    lastupdated=db.Column(db.DateTime)
    negotiation=db.relationship('Negotiations', backref='influencers', lazy=True)



class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    sponsorid = db.Column(db.Integer, primary_key=True)
    sponsorusername = db.Column(db.String(50), db.ForeignKey("userinfo.username"), nullable=False)
    sponsorcategory = db.Column(db.String(50), db.ForeignKey('categories.categoryname'), nullable=False)
    negotiation = db.relationship('Negotiations', backref='sponsors', lazy=True)
    userinfo = db.relationship('UserInfo', backref='sponsors', lazy=True)

class Negotiations(db.Model):
    __tablename__="negotiations"
    negotiationid=db.Column(db.Integer, primary_key=True)
    sponsorid=db.Column(db.Integer, db.ForeignKey("sponsors.sponsorid"),nullable=False)
    influencerid=db.Column(db.Integer, db.ForeignKey("influencers.influencerid"),nullable=False)
    adrequestid=db.Column(db.Integer, db.ForeignKey("adrequests.adrequestid"),nullable=False)
    negotiationstatus=db.Column(db.String(50))
    conversationid=db.Column(db.Integer, db.ForeignKey("conversation.conversationid"),nullable=False)
    adtargetreach=db.Column(db.Integer)
    adbudget=db.Column(db.Integer)
    adrequirement=db.Column(db.String(1000))
    adgoal=db.Column(db.String(1000))
    finalgoal=db.Column(db.String(1000))
    finalrequirement=db.Column(db.String(1000))
    finalbudget=db.Column(db.Integer)
    finaltarget=db.Column(db.Integer)
    lastmodifiedby=db.Column(db.Integer, db.ForeignKey("userinfo.userid"),nullable=False)
    # adrequest = db.relationship("AdRequests", backref="negotiations",cascade="all", lazy=True)



class myInfluencers(db.Model):
    __tablename__="myinfluencers"
    id=db.Column(db.Integer, primary_key=True)
    myid=db.Column(db.String(50), db.ForeignKey("userinfo.username"),nullable=False)
    myinfluencerid=db.Column(db.String(50), db.ForeignKey("influencers.influencerusername"),nullable=False)



class Conversation(db.Model):
    __tablename__='conversation'
    conversationid=db.Column(db.Integer,primary_key=True)
    user1=db.Column(db.Integer, db.ForeignKey("userinfo.userid"),nullable=False)
    user2=db.Column(db.Integer, db.ForeignKey("userinfo.userid"),nullable=False)
    messages=db.relationship('Messages', backref='conversation', lazy=True, cascade="all")
    negotiations=db.relationship('Negotiations', backref='conversation', lazy=True, cascade="all")




class NegotiationsBackup(db.Model):
    __tablename__ = "negobackup"
    negotiationid = db.Column(db.Integer, primary_key=True)
    sponsorid = db.Column(db.Integer)
    influencerid = db.Column(db.Integer)
    campaignid=db.Column(db.Integer)
    campaignname=db.Column(db.String(50))
    adrequestid = db.Column(db.Integer)
    adtitle=db.Column(db.String(50))
    negotiationstatus = db.Column(db.String(50))
    conversationid = db.Column(db.Integer)
    finalgoal = db.Column(db.String(1000))
    finalrequirement = db.Column(db.String(1000))
    finalbudget = db.Column(db.Integer)
    finaltarget = db.Column(db.Integer)
    lastmodifiedby = db.Column(db.Integer)
    lastmodifiedtime = db.Column(db.DateTime, default=datetime.now)
