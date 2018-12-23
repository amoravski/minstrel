from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import PerformanceModel
from models.user import PerformerModel
from resources.parsers import performance_parser

class Performance(Resource):
    """
        Methods by which events are made possible
    """

    def get(self, title):
        performance = PerformanceModel.find_by_title(title)
        if performance:
            return performance.json()
        return {'message': 'Performance not found'}, 404

    @fresh_jwt_required
    def post(self, title):
        user_id = get_jwt_identity()
        if not PerformerModel.find_by_email(user_id):
            return {'status': 'error', 'message': 'Only performers can make performances'}, 400
        if PerformanceModel.find_by_title(title):
            return {"status":"ok",'message': "An Performance with name '{}' already exists.".format(title)}, 400

        data = performance_parser.parse_args()

        performer_categories = PerformerModel.find_by_email(user_id).categories

        performance = PerformanceModel(title, data['text'], user_id, data['location'], data['date'], performer_categories)

        try:
            performance.save_to_db()
        except:
            return {"status": "ok","message": "An error occurred while creating the performance."}, 500

        return {"status": "ok", "performer": performance.json()}, 201

class PerformanceList(Resource):
    """
        Returns a list of all performances
    """

    def get(self):
        performances = [performance.json() for performance in PerformanceModel.find_all()]
        return {'performances': performances}
