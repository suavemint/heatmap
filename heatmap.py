import sys, csv
from lxml import etree
#from pykml import parser
class DMA(object):

    # This DMA object class can be initialized with a DMA number, after which a list
    # + of ZIP codes will be generated from a source CSV file.
    def __init__(self):
        self.dma_number = 0
        self.zip_codes = []
        self.coordinates = []  # List of tuples (lat, long).
        self.n_devices = 0
        self.n_households = 0


    def double_check_zips_only_in_one_dma(self):
        pass


class ZIPCode(object):
    def __init__(self, zip_code, n_devices=0, n_households=0):
        self.zip_code = zip_code
        self.dma_number = 0
        self.coordinates = []
        self.n_devices = self.n_devices  # AKA 'weight'
        self.n_households = self.n_households  # AKA 'weight'


class HTMLDocument(object):
'''Put notes here'''
    def __init__(self, filename=''):
        self.filename = filename
        # self.header_line = ''
        self.weight_coords_dict = {}
        # self.style_vars = ''
        # self.tail_piece = ''

    @classmethod
    def header(cls):
        return '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>Heatmap</title>\n' + \
                  '<style> html, body, #map-canvas {height: 100%; margin: 0px; padding: 0px}\n' +\
                  '#panel {position: absolute; top: 5px; left:50%; margin-left: -180px; z-index: 5;' +\
                  'background-color: #fff; padding: 5px; border: 1px solid #999;}</style>' +\
                  '<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>'+\
                  '<script>\nvar map, pointArray, heatmap;\n'

    @classmethod
    def styles(cls):
        return '''var styles = [
                    {
                        featureType: "landscape",
                        stylers: [
                            {visibility: "off"}
                        ]
                        },{
                        featureType: "poi",
                        stylers: [
                            {visibility: "off"}
                        ]
                    }
                ];
             '''

    @classmethod
    def end_string(cls):
        return """
        ];
        heatmap.setMap(map);
        function initialize() {
            var mapOptions = {
                               styles: styles,
                               zoom: 6,
                               center: new google.maps.LatLng(40.374056,-82.195007),
                               mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
            heatmap = new google.maps.visualization.HeatmapLayer({data: heatMapData});
            heatmap.setMap(map);
            };
        google.maps.event.addDomListener(window, "load", initialize);
        </script></head>
        <body>
        <div id="map-canvas">
        </div>
        </body>
        </html>
         """

    def load_weights_and_coords(self, weight, coords):
        weight_coords_dict[weight] = tuple(coords)

    def write_out(self):
        f_out = open(filename, 'wb')
        f_out.write(HTMLDocument.header())
        f_out.write(HTMLDocument.styles())

        for w in self.weight_coords_dict:
            x,y = self.weight_coords_dict[w]
            f_out.write('{location: new google.maps.LatLng(%s, -%s), weight: %s},\n' % (x, y, w))

        f_out.write(HTMLDocument.end_string())
        f_out.close()


def centroid(x):
    # Input must be a list
    return sum(x) / len(x)

def get_nielsen_csv():
    return csv.reader(open('zip_code_devices_households.csv','rb'))

def convert_zip_to_dmas(csv_in='zip_dmas.csv'):

    import os, cPickle as pickle, csv
    p_name = 'dma_zip_map.pkl'
    dma_zip_map = {}

    is_file = isinstance(csv_in, str)

    # Case 1: The csv does not exist -- halt everything
    if not is_file:
        raise Exception('The required CSV file, {}, is missing from this directory.'.format(csv_in))

    # Case 2: The csv does exist, but the file hasn't yet been saved back to disk as a pkl file,
    # + in which case, pickle it, and return the newly-generated dict.
    if not os.path.isfile(p_name):
        zip_dma = csv.reader(open(csv_in))
        for line in zip_dma:
            zipc, dma, descr = line

            if dma not in dma_zip_map:
                dma_zip_map[dma] = [zipc]
            else:
                dma_zip_map[dma].append(zipc)
        pickle.dump(dma_zip_map, open(p_name,'wb'))
        return dma_zip_map
    else:
        dma_zip_map = pickle.load(open(p_name))
        return dma_zip_map


if __name__ == '__main__':

    import os, cPickle as pickle, itertools
    # print 'Number of DMAs: %r' % len(convert_zip_to_dmas())

    string_list = ['nielsen_devices.html','nielsen_households.html','nielsen_dma_devices.html', 'nielsen_dma_households.html']

    # html_out_devices = 'nielsen_devices.html'
    # html_out_households = 'nielsen_households.html'

    # dmas_out_devices = 'nielsen_dma_devices.html'
    # dmas_out_households = 'nielsen_dma_households.html'

    html_out_list = [HTMLDocument(x) for x in string_list]  # Important structure for HTML out products.

    # html_header += styles
    zip_kml = 'zipcodes.kml'
    googl = './/{http://earth.google.com/kml/2.0}'

    zips = []

    gnc_dict = get_nielsen_csv()
    for zipcode in gnc_dict:
        nd, nh = gnc_dict[zipcode]
        zips.append(ZIPCode(zipcode, nd, nh))

    # zips_dict = { x[0]:(x[1], x[2]) for x in get_nielsen_csv() }
    # zips = zips_dict.keys()

    for z in zips:
        zc = z.zip_code
        if not zc.isdigit():
            zips.pop(zips.index(x))

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

    dmas_dict = convert_zip_to_dmas()
    dmas_nums = {}

    ####
    asdf
    #### TO DO: Make a list of DMA objects; this will simplify the crazy looping piles we've been doing ####

    # print(zips_dict)
    # print(len(zips_dict))
    print(len(dmas_dict))

    for n in dmas_dict:
        zip_list = dmas_dict[n]
        d, h = 0, 0
        # print zip_list
        for m in zip_list:
            try:
                d += int(zips_dict[m][0])
                h += int(zips_dict[m][1])
            except KeyError as e:
                continue
            dmas_nums[n] = (d, h)

    print 'Testing length of dmas nums: %r' % len(dmas_nums)
    print('Testing dmas nums: %s' % dmas_nums)


    for x in zips:
        if x in names:
            # Keep its zip and corresponding coords
            index = names.index(x)
            coord = coords[index]
            coords_dict[x] = coord

    ns = html_header + 'var heatMapData = [\n'
    js_var_string_devices = ns
    js_var_string_households = ns
    js_var_string_dma_devices = ns
    js_var_string_dma_households = ns

    for k,v in coords_dict.iteritems():
        if k in zips_dict:
            boundaries = v.split('-')[1:]  # Leave off the initial empty string.
            x = centroid([float(a.split(',')[1]) for a in boundaries])
            y = centroid([float(a.split(',')[0]) for a in boundaries])

            devs = zips_dict[k][0]
            hs = zips_dict[k][1]
            #print x,y
            #coords_dict[k] = (x,y)  # This is the centroid for the given ZIP code.
            #print boundaries

            # Probably should have split by spaces, but not going back, so add back the minus (-) signs:
            js_var_string_devices += '{location: new google.maps.LatLng(%s, -%s), weight: %s},\n' % (x, y, devs)
            js_var_string_households += '{location: new google.maps.LatLng(%s, -%s), weight: %s},\n' % (x, y, hs)

        else:
            continue

    def finish_string(l):
        l += '];\n'
        # 99.2569978653, 34.1977940798
#        l += 'function initialize() { var mapOptions = {styles: styles, zoom:10, center: new google.maps.LatLng(40.374056,-82.195007), mapTypeId: google.maps.MapTypeId.ROADMAP};\n\nmap = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);\nheatmap = new google.maps.visualization.HeatmapLayer({data: heatMapData});\nheatmap.setMap(map);\n\n'
        l += '''function initialize() {
                    var mapOptions = {
                                        styles: styles,
                                        zoom: 6,
                                        center: new google.maps.LatLng(40.374056,-82.195007),
                                        mapTypeId: google.maps.MapTypeId.ROADMAP
                    };
                    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
                    heatmap = new google.maps.visualization.HeatmapLayer({data: heatMapData});
                    heatmap.setMap(map);
            };
            '''
        l += 'google.maps.event.addDomListener(window, "load", initialize);\n</script></head>\n'
        # map.setOptions({styles:styles})
        l += '<body>\n<div id="map-canvas"></div></body></html>'
        return l

    js_var_string_devices = finish_string(js_var_string_devices[:-2]+'\n')
    js_var_string_households = finish_string(js_var_string_devices[:-2]+'\n')

    with open(html_out_devices,'wb') as f:
        f.write(js_var_string_devices)
    with open(html_out_households,'wb') as f:
        f.write(js_var_string_households)
