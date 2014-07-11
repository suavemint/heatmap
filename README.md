##Heat Map
=======
- Generates two HTML documents -- one for Nielsen-reported number of devices in a ZIP, another for Nielsen-report number of devices in a ZIP -- which display the georgraphic concentration of Nielsen stats in ZIP codes.
- Currently, most HTML/JS behavior is hard-coded into the script proper.
- The "hotspots" are the centroids of the ZIP codes.

#Things to keep in mind:
1. The pages generated are fairly limited in power and scope: zooming out shows the densities better in high-density areas (Maps normalizes intensity to what's currently in view), and there is no further data available to the user for a given hotspot.

#To do:
1. Remove the forests (PoI: forests, I think) in the Maps view
2. Allow for display of the data by DMA as well as by ZIP code
    a. (this will require an initial reworking of the data, combining zip codes into DMAs, but should at worst double the data density in each HTML, which is OTO 10^2 KB.)
1. Combine the two datasets into one Maps view, by adding in a panel which allows for the reloading of the map with the data named in the button clicked.


