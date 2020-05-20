# sumo-examples

Simulation of Frankfurt central station using the real departure schedule. 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/RFYjQs4Jr7Q/0.jpg)](https://www.youtube.com/watch?v=YRFYjQs4Jr7Q)

## Installation

### Use Docker-Container

Using the VSCode *Remote - Containers* extension and run it in "debian with sumo"-Container. 

### Configure DISPLAY

On Windows Install "VcXsrv Windows X Server" https://sourceforge.net/projects/vcxsrv/
For configuration see also (https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde)

Set DISPALY Variable
export DISPLAY=<YourIp>:0.0

```
root@docker-desktop:~/sumo-examples# export DISPLAY=192.168.2.108:0.0
root@docker-desktop:~/sumo-examples# sumo-gui 
```

## Steps 

### Create Network

Download osm Files from openstreemap
```
wget -O frankfurt-bahnhof.osm "http://api.openstreetmap.org/api/0.6/map?bbox=8.6171,50.0882,8.6681,50.1102"
```

Create Typefile only for trains (railway.rail) 
```
cp /usr/share/sumo/data/typemap/osmNetconvertBidiRail.typ.xml rail.typ.xml 
vi rail.typ.xml
```

Convert osm to SUMO Net
```
netconvert --osm-files frankfurt-bahnhof.osm --type-files rail.typ.xml -o frankfurt-bahnhof.net.xml
```

### Create Trips 

#### Random trips
```
python /usr/share/sumo/tools/randomTrips.py -n frankfurt-bahnhof.net.xml --seed 42 --fringe-factor 40 -p 21.879005 -o rail.trips.random.xml -e 3600 --vehicle-class rail --vclass rail --prefix rail --fringe-start-attributes "departSpeed=\"max\"" --min-distance 2400 --trip-attributes "departLane=\"best\"" --validate
```
#### Trips from real departure schedule
https://github.com/dfriedenberger/sumo-Utils

```
cat rail.trips.departure.xml
```
#### Test Routing for created trips
```
duarouter -n frankfurt-bahnhof.net.xml -r rail.trips.manuell.xml --ignore-errors --begin 0 --end 3600.0 --no-step-log --no-warnings -o routes.rou.xml
```
### ConfigFile für Simulation
```
cat frankfurt-bahnhof.sumocfg
...
    <input>
        <net-file value="frankfurt-bahnhof.net.xml"/>
        <route-files value="rail.trips.departure.xml"/>
    </input>
...
```

### Start Simulation with sumo-gui
```
sumo -c frankfurt-bahnhof.sumocfg
```


### Start Simulation with sumo-gui
```
sumo-gui -c frankfurt-bahnhof.sumocfg
```

### Run Sumo with access to TraCi
```
python test-traci.py 
```