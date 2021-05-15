from employee_management import ma
from employee_management.asset.models import Asset


class AssetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset


asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)
