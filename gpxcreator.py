import gpxpy 
import gpxpy.gpx
import datetime
import sys

gpx = gpxpy.gpx.GPX() 

#meters_to_feet=3.28084

# Create first track in our GPX: 
gpx_track = gpxpy.gpx.GPXTrack() 
gpx.tracks.append(gpx_track) 

# Create first segment in our GPX track: 
gpx_segment = gpxpy.gpx.GPXTrackSegment() 
gpx_track.segments.append(gpx_segment) 

FileToConvert = open("/mnt/usb/kittlogs/"+sys.argv[1]+".txt", 'r')

for line in FileToConvert:
    data = line.split()
    dateandtime = datetime.datetime.strptime(data[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    lat = float(data[1])
    lon = float(data[2])
    #alt = '{0:0.2f}'.format(float(data[7])*meters_to_feet)
    alt = float(data[7])
    
# Create points: 
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=alt, time=dateandtime, speed=170)) 
#gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1235, 5.1235, elevation=1235, time=datetime.datetime(2016,01,19,01,44,05),hr=77)) 
#gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1236, 5.1236, elevation=1236, time=datetime.datetime(2016,01,19,01,44,06),hr=77)) 

# You can add routes and waypoints, too... 

FileToConvert.close()

print 'Created GPX for ride '+sys.argv[1]

Output = open('/mnt/usb/kittlogs/'+sys.argv[1]+'.gpx', 'w')
Output.write(gpx.to_xml())
Output.close()

replacements = {'speed':'hr', 'gpx.py -- https://github.com/tkrajina/gpxpy': "KITT with Barometer"}
lines = []
with open('/mnt/usb/kittlogs/'+sys.argv[1]+'.gpx') as infile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        lines.append(line)
with open('/mnt/usb/kittlogs/'+sys.argv[1]+'.gpx', 'w') as outfile:
    for line in lines:
        outfile.write(line)
outfile.close()
