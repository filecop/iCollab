from app import *
from flask import session, request, render_template, redirect, url_for
from backend.models import *
import matplotlib.pyplot as plt
from datetime import datetime, date

def getcurrentuser():
        if 'id' in session:
            userid = session['id']
            userinfo = UserInfo.query.filter_by(userid=userid).first()
            if userinfo:
                return userinfo
        return None

def getmessages():
        if 'id' in session:
            userid = session['id']
            messages = Messages.query.filter_by(receiverid=userid).all()
            return messages
        return None

def getinfluencers():
      influencers = UserInfo.query.filter_by(role=2).all()
      return influencers

def getcampaignlist():
    if 'id' in session:
        userid = session['id']
        campaigns = Campaigns.query.filter_by(campaigncreatedby=userid).all()
        return campaigns
    return None
      
def getadslist():
    if 'id' in session:
        userid = session['id']
        campaigns = Campaigns.query.filter_by(campaigncreatedby=userid).all()
        ads={}
        for campaign in campaigns:
            if campaign.campaignname in ads.keys():
                ads[campaign.campaignname].append(campaign.adRequests.adtitle)
            else:
                ads[campaign.campaignname]=[campaign.adRequests.adtitle]
        return ads
    return None


def getcategorylist():
    categorylist=Category.query.all()
    return categorylist

def getuserid(givenid):
    if 'id' in session:
        influ=Influencers.query.filter_by(influencerid=givenid).first()
        userid=UserInfo.query.filter_by(username=influ.influencerusername).first()
        return userid.userid


def getinfluencers():
    if 'id' in session:
        userid = session['id']
        influencers = Influencers.query.all()
        return influencers
    return None

def getconversationid(influencerid):
     if 'id' in session:
        userid = session['id']
        conversationilist = Conversation.query.all()
        for conversation in conversationilist:
            if conversation.user1 == userid or conversation.user2 == userid:
                if conversation.user2 == influencerid or conversation.user1 == influencerid:
                    return conversation.conversationid
        conversation = Conversation(user1=userid,user2=influencerid)
        db.session.add(conversation)
        db.session.commit()
        return conversation.conversationid
 

def conversationidformsg(userid):
    if 'id' in session:
        userid = session['id']
        conversationilist = Conversation.query.all()
        conversationidlist = []
        for conversation in conversationilist:
            if conversation.user1 == userid or conversation.user2 == userid:
                conversationidlist.append(conversation.conversationid)
        return conversationidlist
    else:
        return None
    

def graphs():
    plt.bar([1, 3, 5, 7, 9], [5, 2, 7, 8, 2])
    plt.savefig('./static/bargraph.png')
    plt.close()

    plt.pie([5,2,7,8,2],labels=[1,3,5,7,9],autopct='%.1f%%')
    plt.savefig('./static/piegraph.png')
    plt.close()
    return 'static/bargraph.png'






def campaignprogress(campaignid,adrequestid,finaltarget,influencerid):
    campaign = Campaigns.query.filter_by(campaignid=campaignid).first()
    ad = AdRequests.query.filter_by(adrequestid=adrequestid).first()
    campaign.campaignprogress = float(campaign.campaignprogress)+(((int(finaltarget))/int(campaign.campaigntargetreach))*100)
    ad.adprogress = float(ad.adprogress)+(((int(finaltarget))/int(ad.adtargetreach))*100)
    ad.isassigned = 1
    ad.influencerid=influencerid
    db.session.commit()

def campaignstats(userinfo):
    campaigns = Campaigns.query.filter_by(campaigncreatedby=userinfo.userid).all()
    campaignnames=[]
    campaignbudget={}
    campaignsblacklisted={}
    campaignprogress={}
    campaigntotalbudget=0
    campaignsstatus={'active':0,'inactive':0}
    for campaign in campaigns:
        campaignnames.append(campaign.campaignname)
        campaignprogress[campaign.campaignname]=campaign.campaignprogress
        campaigntotalbudget=campaigntotalbudget+int(campaign.campaignbudget)
        campaignbudget[campaign.campaignname]=campaign.campaignbudget
        campaignsblacklisted[campaign.campaignname]=campaign.iscampaignblacklisted
        date = datetime.strptime(campaign.campaignenddate, '%Y-%m-%d')
        if date <= datetime.now():
            campaignsstatus['active']=campaignsstatus['active']+1
        else:
            campaignsstatus['inactive']=campaignsstatus['inactive']+1
    return campaignnames,campaignprogress,campaigntotalbudget,campaignsstatus,campaignbudget,campaignsblacklisted
        
def getnichelist(categoryid):
    nichelist=Niches.query.filter_by(categoryid=categoryid).all()
    return nichelist

#     # Generate the plot
#     fig, ax = plt.subplots()
#     ax.bar(campaign_names, campaign_progress, color='skyblue')
#     ax.set_xlabel('Campaigns')
#     ax.set_ylabel('Progress')
#     ax.set_title('Campaign Progress')

#     # Save the plot to a BytesIO object
#     img = io.BytesIO()
#     plt.avefig(img, format='png')
#     img.seek(0)
# s
#     # Serve the plot image to the template
#     return send_file(img, mimetype='image/png')

# if __name__ == '__main__':
#     app.run(debug=True)
