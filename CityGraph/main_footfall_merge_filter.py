import pandas as pd
import geopandas as gpd


def load_filter_footfall(day_num, mask_gdf, nrows):
    print(f"\n### Day {day_num} ###")
    input_csv_filepath = f'../data/raw_footfall/day{day_num}Bcntrakingotherdays.csv'

    # Load csv all spain footfall
    print(f"Load csv footfall day{day_num} : {input_csv_filepath}")
    df = pd.read_csv(input_csv_filepath,
                     delimiter='|',
                     usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'],
                     nrows=nrows)

    # Convert it to geopandas
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE), crs='epsg:4326')
    print(f"Footfall all spain: {len(gdf)} points")

    # Clip it to district
    gdf = gpd.clip(gdf, mask_gdf)
    print(f"Footfall Poblenou district: {len(gdf)} points")

    # Save district shp points
    district_ff_shp_folder = f'../data/raw_footfall/ff-day{day_num}-district'
    gdf.to_file(district_ff_shp_folder)
    print(f"Saved shp footfall district: {district_ff_shp_folder}")

    return district_ff_shp_folder


def fake_list_district():
    return ['../data/raw_footfall/ff-day1-district',
            '../data/raw_footfall/ff-day2-district',
            '../data/raw_footfall/ff-day3-district',
            '../data/raw_footfall/ff-day4-district',
            '../data/raw_footfall/ff-day5-district',
            '../data/raw_footfall/ff-day6-district']


def concat_district_ff(district_ff_folders):
    print("\n### Concat ###")
    # Load all district footfall points
    list_gdf_ff_district = [gpd.read_file(ff_folder) for ff_folder in district_ff_folders]

    # Concat them and clean null timestamp
    concat_gdf = gpd.GeoDataFrame(pd.concat(list_gdf_ff_district, ignore_index=True))
    concat_gdf = concat_gdf[concat_gdf['TIMESTAMP'].notnull()]
    concat_gdf = concat_gdf.to_crs(25831)
    print(f"Footfall concat district: {len(concat_gdf)} points")

    # Save concatenate to shapefile
    district_all_ff_shp_folder = f'../data/raw_footfall/ff-all-district_25831'
    concat_gdf.to_file(district_all_ff_shp_folder)
    print(f"Saved shp concat footfall district: {district_all_ff_shp_folder}")


def load_mask():
    mask_gdf = gpd.read_file('../data/District_Area/District_Area.shp')
    mask_gdf = mask_gdf[mask_gdf['geometry'].notnull()]
    return mask_gdf


# Load csv footfall: ../data/raw_footfall/day1Bcntrakingotherdays.csv
# Footfall all spain: 2333399 points
# Footfall Poblenou district: 96844 points
# Save shp footfall district: ../data/raw_footfall/ff-day1-district
#
# Load csv footfall: ../data/raw_footfall/day2Bcntrakingotherdays.csv
# Footfall all spain: 2161809 points
# Footfall Poblenou district: 88253 points
# Save shp footfall district: ../data/raw_footfall/ff-day2-district
#
# Load csv footfall: ../data/raw_footfall/day3Bcntrakingotherdays.csv
# Footfall all spain: 2140885 points
# Footfall Poblenou district: 87166 points
# Save shp footfall district: ../data/raw_footfall/ff-day3-district
#
# Load csv footfall: ../data/raw_footfall/day4Bcntrakingotherdays.csv
# Footfall all spain: 2177728 points
# Footfall Poblenou district: 84504 points
# Save shp footfall district: ../data/raw_footfall/ff-day4-district
#
# Load csv footfall: ../data/raw_footfall/day5Bcntrakingotherdays.csv
# Footfall all spain: 2326168 points
# Footfall Poblenou district: 91178 points
# Save shp footfall district: ../data/raw_footfall/ff-day5-district
#
# Load csv footfall: ../data/raw_footfall/day6Bcntrakingotherdays.csv
# Footfall all spain: 2548942 points
# Footfall Poblenou district: 92670 points
# Save shp footfall district: ../data/raw_footfall/ff-day6-district

# ### Concat ###
# Footfall concat district: 540615 points
# Saved shp concat footfall district: ../data/raw_footfall/ff-all-district

def main():
    # nrows = 1000
    nrows = None

    mask_gdf = load_mask()

    # Load and clip to district footfall points
    district_ff_folders = [load_filter_footfall(day_num, mask_gdf, nrows) for day_num in range(1, 7, 1)]
    #district_ff_folders = fake_list_district()
    print(district_ff_folders)

    concat_district_ff(district_ff_folders)

if __name__ == "__main__":
    main()
