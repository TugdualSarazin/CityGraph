from CityGraph.simulation.simulation import Simulation


class GenJsonDef:
    base_root = {
        "group": "group name",
        "icon": "image_id_in_shared_folder",
        "proposal": {
            "description": "text",
            "image": "image_id_in_shared_folder",
            "video": "video_url"
        },
        "methodology": {
            "description": "text",
            "image": "image_id_in_shared_folder",
            "video": "video_url"
        },
        "challenge": {
            "description": "text",
            "image": "image_id_in_shared_folder",
            "video": "video_url"
        },
        "layers": []
    }

    base_sublayer_10 = {
        "name": "sublayer name",  # <layer name>
        "mapID": "username.5y2q4o9h",  # <map id provided by mapbox>
        "mapboxSrc": ["mapboxSourceID"],
        "type": "lineString",  # <polygon/point/lineString/raster>
        "representation": "2D",  # <3D/2D>
        # "source": "http:#www.webpage.com",  # <provide the source of the data if it is not generated>
        "scale": "large",  # <large/detailed> zoom level to zoom the map when layer is activated>
        "units": "meters (m)",  # <string to repesent the units. If not applicable type "N/A">
        "description": "LayerDescription",  # <layer's description - text>
        "interpolation": True,  # <true/false> true: if we want gradient, false: if we want discrete stops
        "paint": {
            "property": "my_property",  # <property to colour by>
            "stops": [
                [
                    5,  # <stop 1 value (upper limit)>
                    "#2c003e"  # hex colour code - e.g., https:#www.google.com/search?q=color+picker
                ],
                [
                    15,
                    "#512b58"
                ]
            ]
        },
        "legend": [
            {
                "color": "#2c003e",  # hex colour code - e.g., https:#www.google.com/search?q=color+picker
                "stop": "from-to"
            },
            {
                "color": "#512b58",
                "stop": "from-to"
            }
        ]
    }


    def __init__(self, simulations: [Simulation], ):
        self.json = self.base_root.copy()

    def gen_layers(self):
        pass


    def gen_sublayer(self):
        pass

