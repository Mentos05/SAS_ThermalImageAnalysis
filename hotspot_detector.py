import numpy as np
import cv2
import matplotlib
from matplotlib.cm import get_cmap

for i in range(1,16):
    for var in ['size','avgtemp', 'maxtemp', 'mintemp', 'x1', 'y1', 'w', 'h', 'centerx', 'centery']:
        globals()['hs{}_{}'.format(i,var)] = -1

def detect_hotspots(thermal_image, filename, save_path, min_degree_celsius):
    "Output: thermal_image_annotated, filename, save_path, hs1_size, hs1_avgtemp, hs1_maxtemp, hs1_mintemp, hs1_x1, hs1_y1, hs1_w, hs1_h, hs1_centerx, hs1_centery, hs2_size, hs2_avgtemp, hs2_maxtemp, hs2_mintemp, hs2_x1, hs2_y1, hs2_w, hs2_h, hs2_centerx, hs2_centery, hs3_size, hs3_avgtemp, hs3_maxtemp, hs3_mintemp, hs3_x1, hs3_y1, hs3_w, hs3_h, hs3_centerx, hs3_centery, hs4_size, hs4_avgtemp, hs4_maxtemp, hs4_mintemp, hs4_x1, hs4_y1, hs4_w, hs4_h, hs4_centerx, hs4_centery, hs5_size, hs5_avgtemp, hs5_maxtemp, hs5_mintemp, hs5_x1, hs5_y1, hs5_w, hs5_h, hs5_centerx, hs5_centery, hs6_size, hs6_avgtemp, hs6_maxtemp, hs6_mintemp, hs6_x1, hs6_y1, hs6_w, hs6_h, hs6_centerx, hs6_centery, hs7_size, hs7_avgtemp, hs7_maxtemp, hs7_mintemp, hs7_x1, hs7_y1, hs7_w, hs7_h, hs7_centerx, hs7_centery, hs8_size, hs8_avgtemp, hs8_maxtemp, hs8_mintemp, hs8_x1, hs8_y1, hs8_w, hs8_h, hs8_centerx, hs8_centery, hs9_size, hs9_avgtemp, hs9_maxtemp, hs9_mintemp, hs9_x1, hs9_y1, hs9_w, hs9_h, hs9_centerx, hs9_centery, hs10_size, hs10_avgtemp, hs10_maxtemp, hs10_mintemp, hs10_x1, hs10_y1, hs10_w, hs10_h, hs10_centerx, hs10_centery, hs11_size, hs11_avgtemp, hs11_maxtemp, hs11_mintemp, hs11_x1, hs11_y1, hs11_w, hs11_h, hs11_centerx, hs11_centery, hs12_size, hs12_avgtemp, hs12_maxtemp, hs12_mintemp, hs12_x1, hs12_y1, hs12_w, hs12_h, hs12_centerx, hs12_centery, hs13_size, hs13_avgtemp, hs13_maxtemp, hs13_mintemp, hs13_x1, hs13_y1, hs13_w, hs13_h, hs13_centerx, hs13_centery, hs14_size, hs14_avgtemp, hs14_maxtemp, hs14_mintemp, hs14_x1, hs14_y1, hs14_w, hs14_h, hs14_centerx, hs14_centery, hs15_size, hs15_avgtemp, hs15_maxtemp, hs15_mintemp, hs15_x1, hs15_y1, hs15_w, hs15_h, hs15_centerx, hs15_centery"
    min_degree_celsius=20
    max_size=50000
    min_size=50
    thermal_image = np.frombuffer(thermal_image, dtype='uint8')
    thermal_image = cv2.imdecode(thermal_image, cv2.IMREAD_GRAYSCALE)
    thermal_image = thermal_image.astype(np.uint8)
    thermal_image_hotspot = thermal_image.copy()
    #cv2.imwrite('/data/notebooks/ESP_DEMO/save_path/debug0.png', thermal_image_hotspot)
    thermal_image_hotspot = cv2.GaussianBlur(thermal_image_hotspot, (11, 11), 0)
    #cv2.imwrite('/data/notebooks/ESP_DEMO/save_path/debug1.png', thermal_image_hotspot)
    thermal_image_hotspot = cv2.threshold(thermal_image_hotspot, min_degree_celsius, 255, cv2.THRESH_BINARY)[1]  # ensure binary
    #cv2.imwrite('/data/notebooks/ESP_DEMO/save_path/debug2.png', thermal_image_hotspot)
    thermal_image_hotspot = cv2.erode(thermal_image_hotspot, None, iterations=2)
    #cv2.imwrite('/data/notebooks/ESP_DEMO/save_path/debug3.png', thermal_image_hotspot)
    thermal_image_hotspot = cv2.dilate(thermal_image_hotspot, None, iterations=4)
    #cv2.imwrite('/data/notebooks/ESP_DEMO/save_path/debug4.png', thermal_image_hotspot)
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(thermal_image_hotspot)
    hotspots = {}
    for i in range(num_labels):
        hotspot = {}
        labelMask = np.zeros(thermal_image.shape, dtype="uint8")
        labelMask[labels_im == i] = 255
        locs = np.where(labelMask == 255)
        hotspot_pixels = thermal_image[locs]
        hotspot_size = stats[i][4]
        if hotspot_size >= min_size and hotspot_size <= max_size:
            hotspot['size'] = hotspot_size
            hotspot['avgtemp'] = np.mean(hotspot_pixels)
            hotspot['maxtemp'] = np.max(hotspot_pixels)
            hotspot['mintemp'] = np.min(hotspot_pixels)
            hotspot['x1'] = int(stats[i][0])
            hotspot['y1'] = int(stats[i][1])
            hotspot['w'] = int(stats[i][2])
            hotspot['h'] = int(stats[i][3])
            hotspot['centerx'] = int(centroids[i][0])
            hotspot['centery'] = int(centroids[i][1])
            hotspots[str(i)] = hotspot
    thermal_image_annotated = visualize_hotspots(thermal_image, hotspots, 25, 100)
    #cv2.imwrite('/data/notebooks/ESP_DEMO/save_path/debug5.png', thermal_image_annotated)
    _, thermal_image_annotated = cv2.imencode('.PNG', thermal_image_annotated)
    thermal_image_annotated = thermal_image_annotated.tobytes()
    hotspots_to_variables(hotspots)
    return thermal_image_annotated, filename, save_path, hs1_size, hs1_avgtemp, hs1_maxtemp, hs1_mintemp, hs1_x1, hs1_y1, hs1_w, hs1_h, hs1_centerx, hs1_centery, hs2_size, hs2_avgtemp, hs2_maxtemp, hs2_mintemp, hs2_x1, hs2_y1, hs2_w, hs2_h, hs2_centerx, hs2_centery, hs3_size, hs3_avgtemp, hs3_maxtemp, hs3_mintemp, hs3_x1, hs3_y1, hs3_w, hs3_h, hs3_centerx, hs3_centery, hs4_size, hs4_avgtemp, hs4_maxtemp, hs4_mintemp, hs4_x1, hs4_y1, hs4_w, hs4_h, hs4_centerx, hs4_centery, hs5_size, hs5_avgtemp, hs5_maxtemp, hs5_mintemp, hs5_x1, hs5_y1, hs5_w, hs5_h, hs5_centerx, hs5_centery, hs6_size, hs6_avgtemp, hs6_maxtemp, hs6_mintemp, hs6_x1, hs6_y1, hs6_w, hs6_h, hs6_centerx, hs6_centery, hs7_size, hs7_avgtemp, hs7_maxtemp, hs7_mintemp, hs7_x1, hs7_y1, hs7_w, hs7_h, hs7_centerx, hs7_centery, hs8_size, hs8_avgtemp, hs8_maxtemp, hs8_mintemp, hs8_x1, hs8_y1, hs8_w, hs8_h, hs8_centerx, hs8_centery, hs9_size, hs9_avgtemp, hs9_maxtemp, hs9_mintemp, hs9_x1, hs9_y1, hs9_w, hs9_h, hs9_centerx, hs9_centery, hs10_size, hs10_avgtemp, hs10_maxtemp, hs10_mintemp, hs10_x1, hs10_y1, hs10_w, hs10_h, hs10_centerx, hs10_centery, hs11_size, hs11_avgtemp, hs11_maxtemp, hs11_mintemp, hs11_x1, hs11_y1, hs11_w, hs11_h, hs11_centerx, hs11_centery, hs12_size, hs12_avgtemp, hs12_maxtemp, hs12_mintemp, hs12_x1, hs12_y1, hs12_w, hs12_h, hs12_centerx, hs12_centery, hs13_size, hs13_avgtemp, hs13_maxtemp, hs13_mintemp, hs13_x1, hs13_y1, hs13_w, hs13_h, hs13_centerx, hs13_centery, hs14_size, hs14_avgtemp, hs14_maxtemp, hs14_mintemp, hs14_x1, hs14_y1, hs14_w, hs14_h, hs14_centerx, hs14_centery, hs15_size, hs15_avgtemp, hs15_maxtemp, hs15_mintemp, hs15_x1, hs15_y1, hs15_w, hs15_h, hs15_centerx, hs15_centery
    

def visualize_hotspots(thermal_image, hotspots, min_degree_celsius=25, max_degree_celsius=100):
    cmap = get_cmap('hot')
    norm = matplotlib.colors.Normalize(vmin=min_degree_celsius, vmax=max_degree_celsius, clip=True)
    thermal_image_annotated = thermal_image.astype(np.uint8).copy()
    thermal_image_annotated = cv2.cvtColor(thermal_image_annotated,cv2.COLOR_GRAY2BGR)
    for hotspot in hotspots:
        hotspot_id = int(hotspot)
        hotspot = hotspots[hotspot]
        hotspot_color = np.array(cmap(norm(int(hotspot['avgtemp'])))[0:3])*255
        hotspot_color = (hotspot_color[2],hotspot_color[1],hotspot_color[0])
        cv2.rectangle(thermal_image_annotated,(hotspot['x1'],hotspot['y1']),(hotspot['x1']+hotspot['w'],hotspot['y1']+hotspot['h']),hotspot_color,2)
        cv2.circle(thermal_image_annotated, (hotspot['centerx'], hotspot['centery']), int(2), hotspot_color, -1)
        cv2.putText(thermal_image_annotated, "ID:{}".format(hotspot_id), (hotspot['x1'], hotspot['y1'] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, lineType=cv2.LINE_AA)
        # average temperatures
        cv2.putText(thermal_image_annotated, "ID:{} | {} | {} | {}".format(hotspot_id, int(hotspot['avgtemp']), hotspot['mintemp'], hotspot['maxtemp']), (10,15+hotspot_id*18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    cv2.putText(thermal_image_annotated, "Temperaturwerte (AVG | MIN | MAX) in C".format(hotspot_id, int(hotspot['avgtemp']), hotspot['mintemp'], hotspot['maxtemp']), (10,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    return thermal_image_annotated

def hotspots_to_variables(hotspots):
    for ix, hotspot in enumerate(hotspots):
        for var in hotspots[hotspot]:
            var_name = 'hs{}_{}'.format(ix,var)
            var_value = hotspots[hotspot][var]
            if type(var_value) == np.float64:
                var_value = float(var_value)
            else:
                var_value = int(var_value)
            globals()[var_name] = var_value