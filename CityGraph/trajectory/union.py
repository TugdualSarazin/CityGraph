import geopandas
import pandas as pd

monday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_monday_bcn.csv'
tuesday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_tuesday_bcn.csv'
wednesday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_wednesday_bcn.csv'
thursday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_thursday_bcn.csv'
friday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_friday_bcn.csv'
saturday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_saturday_bcn.csv'
sunday_path = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_sunday_bcn.csv'

nrows = None

monday = pd.read_csv(monday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)
tuesday = pd.read_csv(tuesday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)
wednesday = pd.read_csv(wednesday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)
thursday = pd.read_csv(thursday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)
friday = pd.read_csv(friday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)
saturday = pd.read_csv(saturday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)
sunday = pd.read_csv(sunday_path, usecols=['TIMESTAMP', 'DEVICE_AID', 'LATITUDE', 'LONGITUDE'], nrows=nrows)

concat_df = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday])
concat_df = concat_df[concat_df['TIMESTAMP'].notnull()]
concat_df.to_csv('G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\05_Data\\Footfall\\Filtered+clipped\\footfall_concat_bcn.csv')

print(concat_df)
