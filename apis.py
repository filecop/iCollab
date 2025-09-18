from flask import make_response, jsonify, request
from flask_restful import Resource
from backend.models import db, UserInfo,Campaigns


class GetCampaign(Resource):
    def get(self, campaignid):
        campaign = Campaigns.query.filter_by(campaignid=campaignid).first()
        if not campaign:
            return make_response(jsonify({'message': 'Campaign not found'}), 404)
        campaign_data = {
            'campaignid': campaign.campaignid,
            'campaignname': campaign.campaignname,
            'campaigndescription': campaign.campaigndescription,
            'campaignstartdate': campaign.campaignstartdate,
            'campaignenddate': campaign.campaignenddate,
            'campaignbudget': campaign.campaignbudget,
            'ispublic': campaign.ispublic,
            'campaigngoals': campaign.campaigngoals,
            'iscampaignactive': campaign.iscampaignactive,
            'iscampaignflagged': campaign.iscampaignflagged,
            'iscampaignblacklisted': campaign.iscampaignblacklisted,
            'campaigntargetaudience': campaign.campaigntargetaudience,
            'campaigntargetreach': campaign.campaigntargetreach,
            'campaignprogress': campaign.campaignprogress,
            'campaigncreatedon': campaign.campaigncreatedon,
            'campaigncreatedby': campaign.campaigncreatedby,
            'reportreason': campaign.reportreason}
        return make_response(jsonify(campaign_data), 200)



class CreateCampaign(Resource):
    def post(self):
        data = request.get_json()
        existing_campaign = Campaigns.query.filter_by(campaignname=data['campaignname']).first()
        if existing_campaign:
            return make_response(jsonify({'message': 'Campaign exists'}), 400)
        new_campaign = Campaigns(campaignname=data['campaignname'],campaigndescription=data.get('campaigndescription'),
                campaignstartdate=data.get('campaignstartdate'),
                campaignenddate=data.get('campaignenddate'),
                campaignbudget=data.get('campaignbudget'),
                ispublic=data.get('ispublic', False),
                campaigngoals=data.get('campaigngoals'),
                iscampaignactive=data.get('iscampaignactive', True),
                iscampaignflagged=data.get('iscampaignflagged', False),
                iscampaignblacklisted=data.get('iscampaignblacklisted', False),
                campaigntargetaudience=data.get('campaigntargetaudience'),
                campaigntargetreach=data.get('campaigntargetreach'),
                campaignprogress=data.get('campaignprogress', 0.0),
                campaigncreatedon=data.get('campaigncreatedon'),
                campaigncreatedby=data.get('campaigncreatedby'),
                reportreason=data.get('reportreason'))
        db.session.add(new_campaign)
        db.session.commit()
        return make_response(jsonify({'message': 'Campaign created successfully'}), 201)
    

class GetUser(Resource):
    def get(self, userid):
        user = UserInfo.query.filter_by(userid=userid).first()
        if not user:
            return make_response(jsonify({'message': 'user does not exist'}), 404)
        userinfo = {
            'userid': user.userid,
            'username': user.username,
            'email': user.email,
            'fullname': user.fullname,
            'usertype': user.usertype,
            'userrole': user.role,      
            }
        return make_response(jsonify(userinfo), 200)

