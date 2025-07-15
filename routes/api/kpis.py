from flask_restful import Resource, reqparse
from flask import jsonify
from models.kpi import KPI
from app import db

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title is required')
parser.add_argument('description', type=str)
parser.add_argument('target_value', type=float)
parser.add_argument('current_value', type=float)
parser.add_argument('unit', type=str)
parser.add_argument('category', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)

class KpisAPI(Resource):
    def get(self, id=None):
        """Get a specific KPI or all KPIs"""
        if id:
            kpi = KPI.query.get_or_404(id)
            return jsonify(kpi.serialize())
        all_kpis = KPI.query.all()
        return jsonify([k.serialize() for k in all_kpis])

    def post(self):
        """Create a new KPI"""
        args = parser.parse_args()
        kpi = KPI(
            title=args['title'],
            description=args.get('description'),
            target_value=args.get('target_value'),
            current_value=args.get('current_value', 0),
            unit=args.get('unit'),
            category=args.get('category'),
            start_date=args.get('start_date'),
            end_date=args.get('end_date')
        )
        db.session.add(kpi)
        db.session.commit()
        return jsonify(kpi.serialize()), 201

    def put(self, id):
        """Update an existing KPI"""
        kpi = KPI.query.get_or_404(id)
        args = parser.parse_args()
        
        kpi.title = args['title']
        kpi.description = args.get('description', kpi.description)
        kpi.target_value = args.get('target_value', kpi.target_value)
        kpi.current_value = args.get('current_value', kpi.current_value)
        kpi.unit = args.get('unit', kpi.unit)
        kpi.category = args.get('category', kpi.category)
        kpi.start_date = args.get('start_date', kpi.start_date)
        kpi.end_date = args.get('end_date', kpi.end_date)
        
        db.session.commit()
        return jsonify(kpi.serialize())

    def delete(self, id):
        """Delete a KPI"""
        kpi = KPI.query.get_or_404(id)
        db.session.delete(kpi)
        db.session.commit()
        return '', 204
