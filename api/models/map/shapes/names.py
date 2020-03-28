# Define this here rather than in __init__.py to avoid circular import:
# Shape -> Feature -> FeatureType -> Shape
SHAPE_MODEL_NAMES = ["Circle", "Line", "MultiPolygon", "Point", "Polygon"]
