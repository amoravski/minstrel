from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import PerformanceModel
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
        if PerformanceModel.find_by_title(title):
            return {'message': "An Performance with name '{}' already exists.".format(title)}, 400

        data = performance_parser.parse_args()

        user_id = get_jwt_identity()
        performance = PerformanceModel(title, data['text'], user_id)

        try:
            performance.save_to_db()
        except:
            return {"message": "An error occurred while creating the performance."}, 500

        return performance.json(), 201

class PerformanceList(Resource):
    """
        Returns a list of all performances
    """

    def get(self):
        performances = [performance.json() for performance in PerformanceModel.find_all()]
        return {'performances': performances}
