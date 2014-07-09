import sys, csv
from lxml import etree
from pykml import parser

def average(x):
    # Input must be a list
    return sum(x) / len(x)

def get_nielsen_csv():
    return csv.reader(open('zip_code_devices_households.csv','rb'))

def get_kml_for_zipcode(z):
    pass


if __name__ == '__main__':

    import os, cPickle as pickle, itertools

    html_out_devices = 'nielsen_devices.html'
    html_out_households = 'nielsen_households.html'

    html_header = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>Heatmap</title>\n' + \
                  '<style> html, body, #map-canvas {height: 100%; margin: 0px; padding: 0px}\n' +\
                  '#panel {position: absolute; top: 5px; left:50%; margin-left: -180px; z-index: 5;' +\
                  'background-color: #fff; padding: 5px; border: 1px solid #999;}</style>' +\
                  '<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>'+\
                  '<script>\nvar map, pointArray, heatmap;\n'

    #zip_kml = 'C:\\Users\\james\\zipcodes.kml'
    zip_kml = 'zipcodes.kml'
    googl = './/{http://earth.google.com/kml/2.0}'
    
    zips_dict = { x[0]:(x[1], x[2]) for x in get_nielsen_csv() }
    zips = zips_dict.keys()

    # print 'Testing zips before cull:', len(zips)
    for x in zips:
        if not x.isdigit():
            zips.pop(zips.index(x))
            # sys.exit(1)
    # print 'Testing zips after cull:', len(zips)

    names, coords = [], []

    with open(zip_kml) as f:
        root = etree.parse(f)#.getroot()
        placemarks = root.findall(googl+'Placemark')

        for placemark in placemarks:
            name = placemark.find(googl+'name').text
            coord = placemark.find(googl+'coordinates').text

            names.append(name); coords.append(coord)

    kml_start_num = len(names)
    coords_dict = {}

    #print 'Length of coords list: %i' % len(coords)
    #print 'Length of names list: %i' % len(names)
    #print 15*'='
    #print '%s ZIPs in CSV file.' % len(zips)
    #print '%s ZIPs in KML file.' % kml_start_num

    for x in zips:
        if x in names:
            # Keep its zip and corresponding coords
            index = names.index(x)
            coord = coords[index]
            coords_dict[x] = coord
    
#   print 'Now testing the third way: %i' % len(coords_dict)

    # for name in names:
    
#   print 'Number of zips in names after culling: %i' % len(names)

    #names = [x for x in names if x.isdigit()]
    #names = [x for x in names if x in zips]

    # print 'Surviving number in names:',len(names)
#   print 'Original number of ZIPS:', len(zips)

    js_var_string_devices = html_header + 'var heatMapData = [\n'
    js_var_string_households = html_header + 'var heatMapData = [\n'

    for k,v in coords_dict.iteritems():
        if k in zips_dict:
            boundaries = v.split('-')[1:]  # Leave off the initial empty string.
            x = average([float(a.split(',')[1]) for a in boundaries])
            y = average([float(a.split(',')[0]) for a in boundaries])

            devs = zips_dict[k][0]
            hs = zips_dict[k][1]
            #print x,y
            #coords_dict[k] = (x,y)  # This is the centroid for the given ZIP code.
            #print boundaries

            js_var_string_devices += '{location: new google.maps.LatLng(%s, -%s), weight: %s},\n' % (x, y, devs)
            js_var_string_households += '{location: new google.maps.LatLng(%s, -%s), weight: %s},\n' % (x, y, hs)

        else:
            continue

        #break
#   js_var_string_devices += '];\n'
#   js_var_string_households += '];\n'
        # sys.exit(1)
#    print js_var_string_devices[:-2]; sys.exit(1)
        

#    for l in (js_var_string_devices[:-2]+'\n', js_var_string_households[:-2]+'\n'):
    def finish_string(l):
        l += '];\n'
        # 99.2569978653, 34.1977940798
        l += 'function initialize() { var mapOptions = {zoom:10, center: new google.maps.LatLng(40.374056,-82.195007), mapTypeId: google.maps.MapTypeId.ROADMAP};\n\nmap = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);\nheatmap = new google.maps.visualization.HeatmapLayer({data: heatMapData});\nheatmap.setMap(map);\n};\n'
        l += 'google.maps.event.addDomListener(window, "load", initialize);\n</script></head>\n'
        l += '<body>\n<div id="map-canvas"></div></body></html>'
        return l

    js_var_string_devices = finish_string(js_var_string_devices[:-2]+'\n')
    js_var_string_households = finish_string(js_var_string_devices[:-2]+'\n')
      
    with open(html_out_devices,'wb') as f:
        f.write(js_var_string_devices)
    with open(html_out_households,'wb') as f:
        f.write(js_var_string_households)
    

#   print '%s ZIPs removed: %i difference between KML and # removed.' % (len(names), len(names)-kml_start_num)




    # zips_coords = {int(float(x)):c for x,c in zip(names, coords) if int(float(x)) in zips}

    # print zips_coords



    # zip_coords_dict = 

    # for line in get_nielsen_csv():
    #   print line
