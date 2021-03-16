import subprocess
import json
import re
def extract_convert_GPS(lat, lon):
    def dms2dd(degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
        if direction == 'W' or direction == 'S':
            dd *= -1
        return dd;
    parts_lat = re.split('[^\d\w]+', lat)
    parts_lon = re.split('[^\d\w]+', lon)
    lat = dms2dd(parts_lat[0], parts_lat[2], float('.'.join(parts_lat[3:5])), parts_lat[5])
    lon = dms2dd(parts_lon[0], parts_lon[2], float('.'.join(parts_lon[3:5])), parts_lon[5])
    return lat, lon

def extract_metadata(filename, save_path):
    "Output: filename, save_path, latitude, longitude, relative_altitude, gimbal_roll_degree, gimbal_yaw_degree, gimbal_pitch_degree, flight_roll_degree, flight_yaw_degree, flight_pitch_degree, central_temperature, modify_date, emmisivity, object_distance_m, reflected_apparent_temperature_c, athmospheric_temperature_c, ir_window_temperature_c, ir_window_transmission, relative_humidity_percent, planck_r1, planck_b, planck_f, athmospheric_trans_alpha_1, athmospheric_trans_alpha_2, athmospheric_trans_beta_1, athmospheric_trans_beta_2, athmospheric_trans_x, camera_temperature_range_max_c, camera_temperature_range_min_c, camera_temperature_max_clip_c, camera_temperature_min_clip_c, camera_temperature_max_warn_c, camera_temperature_min_warn_c, camera_temperature_max_saturated_c, camera_temperature_min_saturated_c"
    meta_json = subprocess.check_output(['exiftool', save_path+filename, '-ModifyDate', '-RelativeAltitude', '-GPSLatitude', '-GPSLongitude', '-GimbalRollDegree', '-GimbalYawDegree', 
                                         '-GimbalPitchDegree', '-FlightRollDegree', '-FlightYawDegree', '-FlightPitchDegree', '-CentralTemperature', '-ModifyDate', '-Emissivity', 
                                         '-ObjectDistance', '-ReflectedApparentTemperature', '-AtmosphericTemperature', '-IRWindowTemperature', '-IRWindowTransmission', '-RelativeHumidity', 
                                         '-PlanckR1', '-PlanckB', '-PlanckF', '-AtmosphericTransAlpha1', '-AtmosphericTransAlpha2', '-AtmosphericTransBeta1', '-AtmosphericTransBeta2', 
                                         '-AtmosphericTransX', '-CameraTemperatureRangeMax', '-CameraTemperatureRangeMin', '-CameraTemperatureMaxClip', '-CameraTemperatureMinClip', 
                                         '-CameraTemperatureMaxWarn', '-CameraTemperatureMinWarn', '-CameraTemperatureMaxSaturated', '-CameraTemperatureMinSaturated', '-j'])
    meta = json.loads(meta_json.decode())[0]
    latitude, longitude = extract_convert_GPS(meta['GPSLatitude'], meta['GPSLongitude'])
    relative_altitude = meta['RelativeAltitude']
    gimbal_roll_degree = meta['GimbalRollDegree']
    gimbal_yaw_degree = meta['GimbalYawDegree']
    gimbal_pitch_degree = meta['GimbalPitchDegree']
    flight_roll_degree = meta['FlightRollDegree']
    flight_yaw_degree = meta['FlightYawDegree']
    flight_pitch_degree = meta['FlightPitchDegree']
    central_temperature = meta['CentralTemperature']
    modify_date = meta['ModifyDate']
    emmisivity = meta['Emissivity']
    #object_distance_m = meta['ObjectDistance']
    object_distance_m = float(re.match('\d*.?\d*', meta['ObjectDistance']).group(0))
    reflected_apparent_temperature_c = float(re.match('\d*.?\d*', meta['ReflectedApparentTemperature']).group(0))
    athmospheric_temperature_c = float(re.match('\d*.?\d*', meta['AtmosphericTemperature']).group(0))
    ir_window_temperature_c = float(re.match('\d*.?\d*', meta['IRWindowTemperature']).group(0))
    ir_window_transmission = meta['IRWindowTransmission']
    relative_humidity_percent = float(re.match('\d*.?\d*', meta['RelativeHumidity']).group(0))
    planck_r1 = meta['PlanckR1']
    planck_b = meta['PlanckB']
    planck_f = meta['PlanckF']
    athmospheric_trans_alpha_1 = meta['AtmosphericTransAlpha1']
    athmospheric_trans_alpha_2 = meta['AtmosphericTransAlpha2']
    athmospheric_trans_beta_1 = meta['AtmosphericTransBeta1']
    athmospheric_trans_beta_2 = meta['AtmosphericTransBeta2']
    athmospheric_trans_x = meta['AtmosphericTransX']
    camera_temperature_range_max_c = float(re.match('\d*.?\d*', meta['CameraTemperatureRangeMax']).group(0))
    camera_temperature_range_min_c = float(re.match('\d*.?\d*', meta['CameraTemperatureRangeMin']).group(0))
    camera_temperature_max_clip_c = float(re.match('\d*.?\d*', meta['CameraTemperatureMaxClip']).group(0))
    camera_temperature_min_clip_c = float(re.match('\d*.?\d*', meta['CameraTemperatureMinClip']).group(0))
    camera_temperature_max_warn_c = float(re.match('\d*.?\d*', meta['CameraTemperatureMaxWarn']).group(0))
    camera_temperature_min_warn_c = float(re.match('\d*.?\d*', meta['CameraTemperatureMinWarn']).group(0))
    camera_temperature_max_saturated_c = float(re.match('\d*.?\d*', meta['CameraTemperatureMaxSaturated']).group(0))
    camera_temperature_min_saturated_c = float(re.match('\d*.?\d*', meta['CameraTemperatureMinSaturated']).group(0))
    return filename, save_path, latitude, longitude, relative_altitude, gimbal_roll_degree, gimbal_yaw_degree, gimbal_pitch_degree, flight_roll_degree, flight_yaw_degree, flight_pitch_degree, central_temperature, modify_date, emmisivity, object_distance_m, reflected_apparent_temperature_c, athmospheric_temperature_c, ir_window_temperature_c, ir_window_transmission, relative_humidity_percent, planck_r1, planck_b, planck_f, athmospheric_trans_alpha_1, athmospheric_trans_alpha_2, athmospheric_trans_beta_1, athmospheric_trans_beta_2, athmospheric_trans_x, camera_temperature_range_max_c, camera_temperature_range_min_c, camera_temperature_max_clip_c, camera_temperature_min_clip_c, camera_temperature_max_warn_c, camera_temperature_min_warn_c, camera_temperature_max_saturated_c, camera_temperature_min_saturated_c