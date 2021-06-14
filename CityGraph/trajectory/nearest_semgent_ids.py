import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.ops import nearest_points


class NearestSegmentIds:
    def __init__(self, segments_filepath):
        gpd_segments = gpd.read_file(segments_filepath)

        points = []

        def linestring_to_points(row):
            for coord in row.geometry.coords:
                points.append(pd.Series({'ID_unique': row['ID_unique'], 'geometry': Point(coord[0], coord[1])}))

        gpd_segments.apply(linestring_to_points, axis=1)
        self.segments_pts = GeoDataFrame(points)
        self.segments_pts_union = self.segments_pts.geometry.unary_union

    def nearest_ID_unique(self, point):
        # find the nearest point and return the corresponding geometry
        nearest = nearest_points(point, self.segments_pts_union)[1]
        # Find the ID_unique of the nearest geometry
        return self.segments_pts[self.segments_pts.geometry == nearest]['ID_unique'].head(1).item()

    def find_nearest_segments(self, points):
        return points.apply(lambda pt: self.nearest_ID_unique(pt))
