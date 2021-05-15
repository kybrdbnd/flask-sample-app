from flasgger import swag_from
from flask import request, jsonify
from . import asset
from employee_management.asset.models import Asset
from employee_management.asset.schema import assets_schema, asset_schema
from .. import db


@asset.route('/', methods=['GET', 'POST'])
@swag_from('docs/asset_list.yml', methods=['GET'])
@swag_from('docs/asset_post.yml', methods=['POST'])
def emp_assets():
    if request.method == 'GET':
        assets = Asset.query.all()
        return jsonify(assets_schema.dump(assets))
    if request.method == 'POST':
        data = request.json
        try:
            asset = Asset(name=data['name'])
            db.session.add(asset)
            db.session.commit()
            return {"message": "asset created successfully"}, 201
        except Exception as err:
            return {"message": str(err)}, 500


@asset.route('/assets/<assetId>', methods=['GET', 'PUT', 'DELETE'])
@swag_from('docs/asset_get.yml', methods=['GET'])
@swag_from('docs/asset_put.yml', methods=['PUT'])
@swag_from('docs/asset_delete.yml', methods=['DELETE'])
def assets_crud(assetId):
    if request.method == 'GET':
        asset = Asset.query.get(id=assetId)
        if asset is not None:
            return jsonify(asset_schema.dump(asset)), 200
        else:
            return {"message": "asset not found"}, 404
    if request.method == 'DELETE':
        asset = Asset.query.get(assetId)
        if asset is not None:
            db.session.delete(asset)
            db.session.commit()
            return {}, 204
        else:
            return {"message": "asset not found"}, 404
    if request.method == 'PUT':
        if Asset.query.get(assetId):
            asset = Asset.query.filter_by(id=assetId)
            data = request.json
            asset.update(data)
            db.session.commit()
            return {"message": "asset updated successfully"}, 200
        else:
            return {"message": "asset not found"}, 404
