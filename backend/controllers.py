from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import current_app as app
from helpfunction import getinfluencers
from backend.models import *
from helpfunction import getcurrentuser
from helpfunction import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, date
import os

directory = os.path.join(app.root_path, 'static', 'img', 'graphs')

if not os.path.exists(directory):
    os.makedirs(directory)

app.config['SECRET_KEY'] = 'secret!'

@app.route("/")
def index():
    try:
        return render_template("index.html", userinfo=None)
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route("/register", methods=["POST", "GET"])
def register():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            fullname = request.form.get("fullname")
            email = request.form.get("email")
            password = request.form.get("cpassword")
            userinfo = UserInfo.query.filter_by(username=username).first()
            if userinfo:
                flash("Username already exists")
                return redirect(url_for("register"))
            else:
                userinfo = UserInfo.query.filter_by(email=email).first()
                if userinfo:
                    flash("Email already exists")
                    return redirect(url_for("register"))
                else:
                    userinfo = UserInfo(username=username, fullname=fullname, email=email, password=password)
                    db.session.add(userinfo)
                    db.session.commit()
                    return redirect(url_for("login"))
        return render_template("register.html", userinfo=None)
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route("/influencer/register", methods=["POST", "GET"])
def influencerregister():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            platformpresence = request.form.getlist("platforms")
            userinfo = UserInfo.query.filter_by(username=username, password=password).first()
            if userinfo:
                userinfo.usertype = 'Influencer'
                for i in platformpresence:
                    platformpresence = PlatformPresence(username=userinfo.username, platformname=i)
                    db.session.add(platformpresence)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                return "Check Password"
        platforms = Platforms.query.all()
        return render_template("influencerregistration.html", userinfo=None, platforms=platforms)
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route("/sponsor/register", methods=["POST", "GET"])
def sponsorregister():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            platformpresence = request.form.getlist("platforms")
            userinfo = UserInfo.query.filter_by(username=username, password=password).first()
            if userinfo:
                userinfo.usertype = 'Influencer'
                for i in platformpresence:
                    platformpresence = PlatformPresence(username=userinfo.username, platformname=i)
                    db.session.add(platformpresence)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                return "Check Password"
        industries = Industries.query.all()
        return render_template("sponsorregistration.html", userinfo=None, industries=industries)
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            userinfo = UserInfo.query.filter_by(username=username, password=password).first()
            if userinfo and not userinfo.isblacklisted:
                session['id'] = userinfo.userid
                return redirect(url_for("profile"))
            else:
                flash("Invalid Credentials")
                return redirect(url_for("login"))
        return render_template("login.html", userinfo=None)
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route("/logout")
def logout():
    try:
        session.pop('id', None)
        return redirect(url_for('index'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route("/home")
def home():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            campaigns = Campaigns.query.all()
            ads = AdRequests.query.all()
            return render_template("./admin/adminhome.html", userinfo=userinfo, campaigns=campaigns, ads=ads)
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/somethingwentwrong")
def somethingwentwrong():
    try:
        return render_template("somethingwentwrong.html", userinfo=None)
    except Exception:
        return redirect(url_for("index"))

@app.route("/profile")
def profile():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            category = Category.query.all()
            platforms = Platforms.query.all()
            if userinfo.usertype == 'Sponsor':
                campaigns = Campaigns.query.filter_by(campaigncreatedby=userinfo.userid).all()
                return render_template("sponsorprofile.html", userinfo=userinfo, campaigns=campaigns, category=category)
            elif userinfo.usertype == 'Influencer':
                influencer = Influencers.query.filter_by(influencerusername=userinfo.username).first()
                negotiations = Negotiations.query.filter_by(influencerid=influencer.influencerid).all()
                userplatform = PlatformPresence.query.filter_by(username=influencer.influencerusername).all()
                niche = Niches.query.filter_by(categoryid=influencer.cate.categoryid).all()
                return render_template("./influencers/influencerprofile.html", userinfo=userinfo, negotiations=negotiations, influencer=influencer, userplatform=userplatform, niche=niche, category=category, platforms=platforms)
            elif userinfo.usertype == 'Admin':
                return redirect(url_for('home'))
            else:
                return redirect(url_for('somethingwentwrong'))
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route('/profile/edit/<username>', methods=["POST", "GET"])
def profileedit(username):
    try:
        userinfo = getcurrentuser()
        if userinfo:
            influencer = Influencers.query.filter_by(influencerusername=username).first()
            platformpresence = PlatformPresence.query.filter_by(username=username).all()
            influencer.influencercategory = request.form.get("influencercategory")
            influencer.influencerreach = request.form.get("influencerreach")
            influencer.influencerdescription = request.form.get("influencerdescription")
            platforms = request.form.getlist("platform")
            existingplatform = [platform.platformname for platform in platformpresence]
            for platform_name in platforms:
                if platform_name not in existingplatform:
                    new_platform = PlatformPresence(username=influencer.influencerusername, platformname=platform_name)
                    db.session.add(new_platform)
            for platform in platformpresence:
                if platform.platformname not in platforms:
                    db.session.delete(platform)
            ispublic = request.form.get('ispublic')
            influencer.lastupdated = datetime.today()
            if ispublic == 'True':
                influencer.ispublic = True
            else:
                influencer.ispublic = False

            db.session.commit()
            return redirect(url_for("profile"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route('/workspace', methods=["POST", "GET"])
def workspace():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            negotiations = Negotiations.query.filter_by(influencerid=userinfo.userid).all()
            campaigns = Campaigns.query.filter_by(iscampaignactive=True, iscampaignblacklisted=False, ispublic=True).all()
            return render_template("./influencers/influencerworkspace.html", userinfo=userinfo, negotiations=negotiations, campaigns=campaigns)
        return render_template("index.html", userinfo={})
    except Exception:
        return redirect(url_for("somethingwentwrong"))

#################################################################################################
@app.route('/campaigns', methods=["POST", "GET"])
def campaigns():
    try:
        if request.method == "POST":
            userinfo = getcurrentuser()
            campaignname = request.form.get("campaigntitle")
            campaigndescription = request.form.get("campaigndescription")
            campaignstartdate = str(date.today())
            campaignenddate = str(request.form.get("campaignenddate"))
            campaignbudget = request.form.get("campaignbudget")
            ispublic = request.form.get('campaignvisibility') == 'True'
            campaigngoals = request.form.get("campaigngoals")
            iscampaignactive = True
            iscampaignflagged = False
            iscampaignblacklisted = False
            campaigntargetaudience = request.form.get("campaigntargetaudience")
            campaigntargetreach = request.form.get("campaigntargetreach")
            campaigncreatedon = date.today()
            campaigncreatedby = userinfo.userid
            campaign = Campaigns(campaignname=campaignname, campaigndescription=campaigndescription, campaignstartdate=campaignstartdate,
                                 campaignenddate=campaignenddate, campaignbudget=campaignbudget, ispublic=ispublic,
                                 campaigngoals=campaigngoals, iscampaignactive=iscampaignactive, iscampaignflagged=iscampaignflagged,
                                 iscampaignblacklisted=iscampaignblacklisted, campaigntargetaudience=campaigntargetaudience,
                                 campaigncreatedon=campaigncreatedon, campaigncreatedby=campaigncreatedby, campaigntargetreach=campaigntargetreach)
            db.session.add(campaign)
            db.session.commit()
            existingcampaigns = Campaigns.query.filter_by(campaigncreatedby=userinfo.userid).all()
            categorylist = Category.query.all()
            return render_template("campaigns.html", userinfo=userinfo, existingcampaigns=existingcampaigns, categorylist=categorylist)

        userinfo = getcurrentuser()
        if userinfo:
            existingcampaigns = Campaigns.query.filter_by(campaigncreatedby=userinfo.userid).all()
            categorylist = Category.query.all()
            if existingcampaigns:
                return render_template("campaigns.html", userinfo=userinfo, existingcampaigns=existingcampaigns, categorylist=categorylist)
            else:
                existingcampaigns = ""
                categorylist = Category.query.all()
                return render_template("campaigns.html", userinfo=userinfo, existingcampaigns=existingcampaigns, categorylist=categorylist)
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/campaigns/edit/<int:campaignid>', methods=["POST", "GET"])
def campaignsedit(campaignid):
    try:
        if request.method == "POST":
            userinfo = getcurrentuser()
            if userinfo:
                campaign = Campaigns.query.filter_by(campaignid=campaignid).first()
                campaign.campaignname = request.form.get("campaigntitle")
                campaign.campaigndescription = request.form.get("campaigndescription")
                campaign.campaignstartdate = str(datetime.now())
                campaign.campaignenddate = request.form.get("campaignenddate")
                campaign.campaignbudget = request.form.get("campaignbudget")
                campaign.campaignvisibility = request.form.get("campaignvisibility")
                campaign.campaigngoals = request.form.get("campaigngoals")
                campaign.iscampaignactive = True
                campaign.iscampaignflagged = False
                campaign.iscampaignblacklisted = False
                campaign.campaigntargetaudience = request.form.get("campaigntargetaudience")
                campaign.campaigncreatedon = str(datetime.now())
                campaign.campaigncreatedby = userinfo.userid
                db.session.commit()
                return redirect(url_for('campaigns'))
            else:
                return redirect(url_for("index"))
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/campaigns/delete/<int:campaignid>', methods=["POST", "GET"])
def campaignsdelete(campaignid):
    try:
        if request.method == "POST":
            userinfo = getcurrentuser()
            if userinfo:
                campaign = Campaigns.query.filter_by(campaignid=campaignid).first()
                db.session.delete(campaign)
                db.session.commit()
                return redirect(url_for('campaigns'))
            else:
                return redirect(url_for("index"))
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/viewcampaign/<int:campaignid>', methods=["POST", "GET"])
def viewcampaign(campaignid):
    try:
        if request.method == "POST":
            return redirect(url_for('campaigns'))
        userinfo = getcurrentuser()
        if userinfo:
            campaign = Campaigns.query.filter_by(campaignid=campaignid).first()
            nichelist = getnichelist(campaign.campaigntargetaudience)
            categorylist = getcategorylist()
            return render_template("viewcampaign.html", campaign=campaign, userinfo=userinfo, ads=campaign.adRequests, categorylist=categorylist, nichelist=nichelist)
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/createad/<int:userid>/<int:campaignid>', methods=["POST", "GET"])
def createad(userid, campaignid):
    try:
        if request.method == "POST":
            userinfo = getcurrentuser()
            if userinfo:
                adtitle = request.form.get('adtitle')
                requirements = request.form.get('Requirements')
                paymentamount = request.form.get('paymentamount')
                ispublic = request.form.get('advisibility') == 'True'
                adtargetreach = request.form.get('targetreach')
                AdRequest = AdRequests(adtitle=adtitle, campaignid=campaignid, requirements=requirements, paymentamount=paymentamount, isactive=True, ispublic=ispublic, isblacklisted=False, isassigned=False, adtargetreach=adtargetreach)
                db.session.add(AdRequest)
                db.session.commit()
                return redirect(url_for('viewcampaign', campaignid=campaignid))
            else:
                return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

####################
@app.route('/modifyad/<int:userid>/<int:campaignid>/<int:adid>', methods=["POST", "GET"])
def modifyad(userid, campaignid, adid):
    try:
        if request.method == "POST":
            userinfo = getcurrentuser()
            if userinfo:
                ad = AdRequests.query.filter_by(adrequestid=adid, campaignid=campaignid).first()
                if ad:
                    ad.adtitle = request.form.get('adtitle')
                    ad.requirements = request.form.get('Requirements')
                    ad.paymentamount = request.form.get('paymentamount')
                    ad.ispublic = request.form.get('advisibility') == 'True'
                    ad.adtargetreach = request.form.get('targetreach')
                    db.session.commit()
                    return redirect(url_for('viewcampaign', campaignid=campaignid))
                else:
                    flash("Ad not found", "error")
                    return redirect(url_for('viewcampaign', campaignid=campaignid))
            else:
                return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/ad/delete/<int:campaignid>/<int:adrequestid>', methods=["POST", "GET"])
def addelete(campaignid, adrequestid):
    try:
        userinfo = getcurrentuser()
        if userinfo:
            ad = AdRequests.query.filter_by(adrequestid=adrequestid).first()
            db.session.delete(ad)
            db.session.commit()
            return redirect(url_for('viewcampaign', campaignid=campaignid))
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/adrequests", methods=["GET", "POST"])
def adrequests():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            campaigns = getcampaignlist()
            categorylist = getcategorylist()
            influencer = getinfluencers()
            conversationids = conversationidformsg(userinfo.userid)
            conversation = {}
            messages = []
            negotiations = Negotiations.query.filter_by(sponsorid=userinfo.userid).all()
            # for conversationid in conversationids:
            #     if conversationid in conversation.keys():
            #         conversation[conversationid].extend(Messages.query.filter_by(conversationid=conversationid).all())
            #     else:
            #         conversation[conversationid] = Messages.query.filter_by(conversationid=conversationid).all()
            # for message_list in conversation.values():
            #     for message in message_list:
            #         messages.append(message)
            return render_template("adrequest1.html", userinfo=userinfo, campaigns=campaigns, categorylist=categorylist, influencerlist=influencer, negotiations=negotiations)
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/negotiations", methods=["POST"])
def negotiations():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if request.method == 'POST':
                conversationid = getconversationid(request.form.get('influencerid'))
                sponsorid = userinfo.userid
                influencerid = getuserid(request.form.get('influencerid'))
                adrequestid = int(request.form.get('adrequestid'))
                adrequirement = request.form.get('adrequirement')
                adgoal = request.form.get('adgoal')
                adtargetreach = int(request.form.get('adtargetreach'))
                adbudget = request.form.get('adbudget')
                lastmodifiedby = userinfo.userid
                negotiation = Negotiations(conversationid=conversationid, sponsorid=sponsorid, influencerid=influencerid, adrequestid=adrequestid, negotiationstatus='In Progress', adrequirement=adrequirement, adgoal=adgoal, adtargetreach=adtargetreach, adbudget=adbudget, lastmodifiedby=lastmodifiedby)
                db.session.add(negotiation)
                db.session.commit()
                return redirect(url_for("adrequests"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/negotiations/i", methods=["POST"])
def inegotiations():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if request.method == 'POST':
                conversationid = getconversationid(userinfo.userid)
                sponsorid = request.form.get('sponsorid')
                influencerid = userinfo.userid
                adrequestid = int(request.form.get('adrequestid'))
                adrequirement = request.form.get('adrequirement')
                adgoal = request.form.get('adgoal')
                adtargetreach = int(request.form.get('adtargetreach'))
                adbudget = request.form.get('adbudget')
                lastmodifiedby = userinfo.userid
                negotiation = Negotiations(conversationid=conversationid, sponsorid=sponsorid, influencerid=influencerid, adrequestid=adrequestid, negotiationstatus='In Progress', adrequirement=adrequirement, adgoal=adgoal, adtargetreach=adtargetreach, adbudget=adbudget, lastmodifiedby=lastmodifiedby)
                db.session.add(negotiation)
                db.session.commit()
                return redirect(url_for("workspace"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/negotiations/modify/<int:negotiationid>", methods=["POST"])
def negotiationsmodify(negotiationid):
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if request.method == 'POST':
                negotiation = Negotiations.query.filter_by(negotiationid=negotiationid).first()
                negotiation.adtargetreach = request.form.get('adtargetreach')
                negotiation.adbudget = request.form.get('adbudget')
                negotiation.adrequirement = request.form.get('adrequirement')
                negotiation.adgoal = request.form.get('adgoal')
                negotiation.negotiationstatus = 'In Progress'
                negotiation.lastmodifiedby = userinfo.userid
                db.session.commit()
                if userinfo.usertype == 'Influencer':
                    return redirect(url_for("workspace"))
                else:
                    return redirect(url_for("adrequests"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/negotiations/reject/<int:negotiationid>", methods=["POST"])
def negotiationsreject(negotiationid):
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if request.method == 'POST':
                negotiation = Negotiations.query.filter_by(negotiationid=negotiationid).first()
                negotiation.finaltarget = request.form.get('adtargetreach')
                negotiation.finalbudget = request.form.get('adbudget')
                negotiation.finalrequirement = request.form.get('adrequirement')
                negotiation.finalgoal = request.form.get('adgoal')
                if negotiation.negotiationstatus == 'Rejected':
                    negotiation.negotiationstatus = 'Declined'
                else:
                    negotiation.negotiationstatus = 'Rejected'
                negotiation.lastmodifiedby = userinfo.userid
                db.session.commit()
                if userinfo.usertype == 'Influencer':
                    return redirect(url_for("workspace"))
                return redirect(url_for("adrequests"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/negotiations/accept/<int:negotiationid>", methods=["POST"])
def negotiationsaccept(negotiationid):
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if request.method == 'POST':
                negotiation = Negotiations.query.filter_by(negotiationid=negotiationid).first()
                if negotiation.negotiationstatus != 'Accepted':
                    negotiation.finaltarget = request.form.get('adtargetreach')
                    negotiation.finalbudget = request.form.get('adbudget')
                    negotiation.finalrequirement = request.form.get('adrequirement')
                    negotiation.finalgoal = request.form.get('adgoal')
                    negotiation.lastmodifiedby = userinfo.userid
                    negotiation.negotiationstatus = 'Accepted'
                else:
                    negotiation.finaltarget = request.form.get('adtargetreach')
                    negotiation.finalbudget = request.form.get('adbudget')
                    negotiation.finalrequirement = request.form.get('adrequirement')
                    negotiation.finalgoal = request.form.get('adgoal')
                    negotiation.negotiationstatus = 'Confirmed'
                    negotiation.lastmodifiedby = userinfo.userid
                    negobackup = NegotiationsBackup(sponsorid=negotiation.sponsorid, influencerid=negotiation.influencerid, campaignid=negotiation.adrequests.campaigns.campaignid, campaignname=negotiation.adrequests.campaigns.campaignname, adrequestid=negotiation.adrequestid, adtitle=negotiation.adrequests.adtitle, negotiationstatus='Confirmed', finaltarget=negotiation.finaltarget, finalbudget=negotiation.finalbudget, finalrequirement=negotiation.finalrequirement, finalgoal=negotiation.finalgoal, lastmodifiedby=userinfo.userid, conversationid=negotiation.conversationid, lastmodifiedtime=datetime.now())
                    campaignprogress(negotiation.adrequests.campaigns.campaignid, negotiation.adrequestid, negotiation.finaltarget, negotiation.influencerid)
                    db.session.add(negobackup)
                db.session.commit()
                if userinfo.usertype == 'Influencer':
                    return redirect(url_for("workspace"))
                return redirect(url_for("adrequests"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/find/a")
def afind():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if request.method == "GET" and request.args.get("influencersearch"):
                searchterm = request.args.get("influencersearch")
                users = UserInfo.query.filter(UserInfo.username.like(f"%{searchterm}%")).all()
                if users:
                    return render_template("./admin/find.html", userinfo=userinfo, influencerlist=users)
                else:
                    return render_template("./find.html", userinfo=userinfo, noresult=True)
            return render_template("./admin/find.html", userinfo=userinfo)
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/find")
def sfind():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            categories = Category.query.all()
            if userinfo.usertype == 'Sponsor':
                myinfluencers = myInfluencers.query.filter_by(myid=userinfo.userid).all()
                if request.method == "GET" and request.args.get("influencersearch"):
                    searchterm = request.args.get("influencersearch")
                    influencer = Influencers.query.filter(Influencers.influencerusername.like(f"%{searchterm}%")).all()
                    if influencer:
                        return render_template("find.html", userinfo=userinfo, influencerlist=influencer, myinfluencers=myinfluencers)
                    else:
                        return render_template("find.html", userinfo=userinfo, noresult=True)
                myinfluencers = myInfluencers.query.filter_by(myid=userinfo.userid).all()
                return render_template("find.html", userinfo=userinfo, myinfluencers=myinfluencers)
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/find/i")
def ifind():
    try:
        userinfo = getcurrentuser()
        if userinfo:
            title = request.args.get("title")
            budget = request.args.get("budget")
            category = request.args.get("category")
            query = AdRequests.query
            if title:
                query = query.filter(AdRequests.adtitle.like(f"%{title}%"))
            if budget:
                query = query.filter(AdRequests.paymentamount >= int(budget))
            if category:
                query = query.filter(AdRequests.campaigns.has(Campaigns.cate.has(Category.categoryname == category)))
            ads = query.all()
            if ads:
                return render_template("./influencers/find.html", userinfo=userinfo, ads=ads)
            else:
                return render_template("./influencers/find.html", userinfo=userinfo, noresult=True)
        else:
            return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route("/find/addinfluencer/<influencerusername>")
def addinfluencer(influencerusername):
    try:
        userinfo = getcurrentuser()
        if userinfo:
            if userinfo.usertype == 'Sponsor':
                addinfluencer = myInfluencers.query.filter_by(myinfluencerid=influencerusername).first()
                if not addinfluencer:
                    newinflu = myInfluencers(myid=userinfo.userid, myinfluencerid=influencerusername)
                    db.session.add(newinflu)
                    db.session.commit()
                return redirect(url_for("sfind"))
            if userinfo.usertype == 'Influencer':
                return redirect(url_for("adrequests"))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/stats/sponsors')
def statssponsors():
    try:
        userinfo = getcurrentuser()
        if userinfo and userinfo.usertype == 'Sponsor':
            sponsor = Sponsors.query.filter_by(sponsorusername=userinfo.username).first()
            sponsor_id = sponsor.sponsorid
            negobackups = NegotiationsBackup.query.filter_by(sponsorid=sponsor_id).all()
            campaignspending = {}
            campaignreach = {}
            campaignads = {}
            influencerperformance = {}

            for nego in negobackups:
                if nego.campaignname in campaignspending:
                    campaignspending[nego.campaignname] += nego.finalbudget
                    campaignreach[nego.campaignname] += nego.finaltarget
                    campaignads[nego.campaignname] += 1
                else:
                    campaignspending[nego.campaignname] = nego.finalbudget
                    campaignreach[nego.campaignname] = nego.finaltarget
                    campaignads[nego.campaignname] = 1

                influencer = Influencers.query.filter_by(influencerid=nego.influencerid).first()
                if influencer:
                    if influencer.influencerusername in influencerperformance:
                        influencerperformance[influencer.influencerusername] += nego.finaltarget
                    else:
                        influencerperformance[influencer.influencerusername] = nego.finaltarget

            campaignnames = list(campaignspending.keys())
            campaignspend = list(campaignspending.values())
            campaignreach = list(campaignreach.values())
            campaignads_values = list(campaignads.values())
            influencers = list(influencerperformance.keys())
            influencertargets = list(influencerperformance.values())

            totalmoneyspent = sum(campaignspend)
            totalviews = sum(campaignreach)
            totalads = sum(campaignads_values)
            campaignscount = len(campaignnames)
            averagebudget = totalmoneyspent / campaignscount if campaignscount > 0 else 0

            directory = os.path.join('static', 'img', 'graphs')
            if not os.path.exists(directory):
                os.makedirs(directory)

            if campaignspend and campaignreach and influencertargets:
                plt.figure()
                plt.bar(campaignnames, campaignspend, color='orange')
                plt.xticks(rotation=45, ha='right')
                for i in range(len(campaignnames)):
                    plt.text(i, campaignspend[i], campaignspend[i], ha='center', va='bottom')
                plt.title('Total Spend by Campaign(₹)')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'sgraph1.jpg'))
                plt.close()

                plt.figure()
                plt.bar(campaignnames, campaignreach, color='blue')
                plt.xticks(rotation=45, ha='right')
                for i in range(len(campaignnames)):
                    plt.text(i, campaignreach[i], campaignreach[i], ha='center', va='bottom')
                plt.title('Audience Reach by Campaign')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'sgraph2.jpg'))
                plt.close()

                plt.figure()
                plt.bar(influencers, influencertargets, color='purple')
                plt.xticks(rotation=45, ha='right')
                for i in range(len(influencers)):
                    plt.text(i, influencertargets[i], influencertargets[i], ha='center', va='bottom')
                plt.title('Top Performing Influencers by Audience Reach')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'sgraph3.jpg'))
                plt.close()
            else:
                graphs = ['sgraph1.jpg', 'sgraph2.jpg', 'sgraph3.jpg']
                for graph in graphs:
                    path = os.path.join(directory, graph)
                    if os.path.exists(path):
                        os.remove(path)
            return render_template("sponsorstats.html", userinfo=userinfo, totalmoneyspent=totalmoneyspent, totalviews=totalviews, totalads=totalads)
        return redirect(url_for('index'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/stats/influencers')
def statsinfluencers():
    try:
        userinfo = getcurrentuser()
        if userinfo and userinfo.usertype == 'Influencer':
            influencer_id = userinfo.userid
            negobackups = NegotiationsBackup.query.filter_by(influencerid=influencer_id).all()
            campaignearnings = {}
            campaigntarget = {}

            for nego in negobackups:
                if nego.campaignname in campaignearnings:
                    campaignearnings[nego.campaignname] += nego.finalbudget
                    campaigntarget[nego.campaignname] += nego.finaltarget
                else:
                    campaignearnings[nego.campaignname] = nego.finalbudget
                    campaigntarget[nego.campaignname] = nego.finaltarget

            campaignnames = list(campaignearnings.keys())
            campaignearning = list(campaignearnings.values())
            target = list(campaigntarget.values())
            campaignscount = len(campaignnames)
            averagebudget = sum(campaignearning) / campaignscount if campaignscount > 0 else 0
            totalads = len(negobackups)
            totalearn = sum(campaignearning)
            if campaignearning and target:
                plt.figure()
                plt.bar(campaignnames, campaignearning, color='blue')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, max(campaignearning) * 1.5)
                for i in range(len(campaignnames)):
                    plt.text(i, campaignearning[i], campaignearning[i], ha='center', va='bottom')
                plt.title('Total Earnings by Campaign(₹)')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'graph1.jpg'))
                plt.close()

                plt.figure()
                plt.bar(campaignnames, target, color='green')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, max(target) * 1.5)
                for i in range(len(campaignnames)):
                    plt.text(i, target[i], target[i], ha='center', va='bottom')
                plt.title('Views Target by Campaign')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'graph2.jpg'))
                plt.close()

                plt.figure()
                plt.pie(campaignearning, labels=campaignnames, autopct='%1.5f%%')
                plt.title('Campaign Budgets')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'graph3.jpg'))
                plt.close()
            else:
                graph_files = ['graph1.jpg', 'graph2.jpg', 'graph3.jpg']
                for file in graph_files:
                    file_path = os.path.join(directory, file)
                    if os.path.exists(file_path):
                        os.remove(file_path)

            return render_template("./influencers/influencerstats.html", userinfo=userinfo, averagebudget=round(averagebudget, 2), totalads=totalads, totalearn=totalearn)
        return redirect(url_for('index'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/admin/flag/campaign', methods=['POST'])
def adminflagcampaign():
    try:
        if request.method == 'POST':
            campaignid = request.form.get('campaignid')
            action = request.form.get('action')
            reason = request.form.get('reason')
            campaign = Campaigns.query.get(campaignid)
            if action == 'Removeflag':
                campaign.iscampaignflagged = False
            elif action == 'blacklist':
                campaign.iscampaignflagged = True
                campaign.iscampaignblacklisted = True
                campaign.reason = reason
            db.session.commit()
            return redirect(url_for('home'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/admin/flag/users', methods=['POST'])
def adminflagusers():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            action = request.form.get('action')
            userdetails = UserInfo.query.filter_by(username=username).first()
            if action == 'Removeflag':
                userdetails.isflagged = False
            elif action == 'blacklist':
                userdetails.isflagged = True
                userdetails.isblacklisted = True
            db.session.commit()
            return redirect(url_for('afind'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/admin/flag/ad', methods=['POST'])
def adminflagad():
    try:
        if request.method == 'POST':
            adrequestid = request.form.get('adrequestid')
            action = request.form.get('action')
            reason = request.form.get('reason')
            ad = AdRequests.query.get(adrequestid)
            if action == 'remove_flag':
                ad.isflagged = False
                ad.reportreason = None
                db.session.commit()
            elif action == 'blacklist':
                ad.isflagged = True
                ad.isblacklisted = True
                ad.reportreason = reason
                db.session.commit()
            return redirect(url_for('home'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/influencer/flagadrequest/<int:adrequestid>', methods=['POST'])
def flagadrequest(adrequestid):
    try:
        if request.method == 'POST':
            ad = AdRequests.query.get(adrequestid)
            if ad:
                ad.isflagged = True
                ad.reportreason = request.form.get('reason')
                db.session.commit()
                return redirect(url_for('workspace'))
            return 'Campaign not found'
    except Exception:
        return redirect(url_for("somethingwentwrong"))

@app.route('/stats/admin')
def statsadmin():
    try:
        userinfo = getcurrentuser()
        if userinfo and userinfo.usertype == 'Admin':
            negobackups = NegotiationsBackup.query.all()
            campaigns = Campaigns.query.all()
            users = UserInfo.query.all()

            campaignearnings = {}
            campaigntarget = {}
            campblacklisted = 0
            campwhitelisted = 0
            userswhitelisted = 0
            usersblacklisted = 0
            influencerscount = 0
            sponsorscount = 0
            campaignnames = []
            campaignspend = []
            campaignearnings = {}
            campaigntarget = {}
            campaignfinaltarget = []
            campaigncount = 0
            totaladrequests = 0

            for nego in negobackups:
                totaladrequests += 1
                if nego.campaignname in campaignearnings:
                    campaignearnings[nego.campaignname] += nego.finalbudget
                    campaigntarget[nego.campaignname] += nego.finaltarget
                else:
                    campaignearnings[nego.campaignname] = int(nego.finalbudget)
                    campaigntarget[nego.campaignname] = int(nego.finaltarget)

            for campaigns in campaigns:
                if campaigns.iscampaignblacklisted:
                    campblacklisted += 1
                else:
                    campwhitelisted += 1

            for user in users:
                if user.usertype == 'Sponsor':
                    sponsorscount += 1
                if user.usertype == 'Influencer':
                    influencerscount += 1
                if user.isblacklisted:
                    usersblacklisted += 1
                else:
                    userswhitelisted += 1

            for (key, value) in campaignearnings.items():
                campaignnames.append(key)
                campaignspend.append(value)
                campaigncount = + 1

            for (key, value) in campaigntarget.items():
                campaignfinaltarget.append(value)

            totalviews = sum(campaignfinaltarget)

            totalearning = sum(campaignspend)

            if campaigncount > 0:
                averagebudget = totalearning / campaigncount
            else:
                averagebudget = 0

            if totalearning and campaignfinaltarget:
                plt.figure()
                plt.bar(campaignnames, campaignspend, color='blue')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, max(campaignspend) * 1.5)
                for i in range(len(campaignnames)):
                    plt.text(i, campaignspend[i], campaignspend[i], ha='center', va='bottom')
                plt.title('Total Earnings by Campaign(₹)')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'agraph1.jpg'))
                plt.close()

                plt.figure()
                plt.bar(campaignnames, campaignfinaltarget, color='green')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, max(campaignfinaltarget) * 1.5)
                for i in range(len(campaignnames)):
                    plt.text(i, campaignfinaltarget[i], campaignfinaltarget[i], ha='center', va='bottom')
                plt.title('Views Target by Campaign')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'agraph2.jpg'))
                plt.close()

                plt.figure()
                plt.pie(campaignspend, labels=campaignnames, autopct='%1.5f%%')
                plt.title('Campaign Budgets')
                plt.tight_layout()
                plt.savefig(os.path.join(directory, 'agraph3.jpg'))
                plt.close()
            else:
                graphs = ['agraph1.jpg', 'agraph2.jpg', 'agraph3.jpg']
                for file in graphs:
                    path = os.path.join(directory, file)
                    if os.path.exists(path):
                        os.remove(path)

            return render_template("./admin/adminstats.html", userinfo=userinfo, averagebudget=round(averagebudget, 2), totaladrequests=totaladrequests, totalearning=totalearning, totalviews=totalviews, sponsorscount=sponsorscount, influencerscount=influencerscount, userswhitelisted=userswhitelisted, usersblacklisted=usersblacklisted, campblacklisted=campblacklisted, campwhitelisted=campwhitelisted)
        return redirect(url_for('index'))
    except Exception:
        return redirect(url_for("somethingwentwrong"))
