import logging
import os
import sys
import threading
import time

if 'SUMO_HOME' in os.environ:
    SUMO_HOME = os.environ['SUMO_HOME']
    sys.path.append(os.path.join(SUMO_HOME, 'tools'))
    os.environ['PATH'] += os.pathsep + os.path.join(SUMO_HOME, 'bin')

import traci
import traci.constants as tc


fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.INFO, format=fmt_str)

logger = logging.getLogger(__name__)



step_counter=0
steps=5000
sumo_cmd="sumo-gui"
#sumo_cmd="sumo"

config_path="summerschool/sumo.sumocfg"
step_length=1

traci.start([sumo_cmd, '--no-warnings', '-c', config_path])
vehID="trip_0"

blockabschnitt_belegt = {};
signals = { "gneJ17" : ["gneE16", "gneE1" ] ,
            "gneJ2"  : ["gneE1",  "gneE7" ] , 
            "gneJ8"  : ["gneE7",  "gneE10" ] , 
            "gneJ11" : ["gneE10", "gneE13" ],
            "gneJ14" : ["gneE13", "gneE16"] };


for signalId in signals:
    traci.trafficlight.setRedYellowGreenState(signalId, "r");
    for edgeId in signals[signalId]: 
        traci.edge.subscribeContext(edgeId, tc.CMD_GET_VEHICLE_VARIABLE, 0, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

traci.vehicle.subscribe(vehID, (tc.VAR_SPEED, tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION, tc.VAR_POSITION))

try:
    while step_counter < steps:
        logger.debug('Next step (%d of %d)', step_counter , steps)
        traci.simulationStep()
        subscription = traci.vehicle.getSubscriptionResults(vehID)
        #logger.info("subscribe %d: speed=%s",step_counter,subscription);
        if subscription is not None:
            speed = subscription[tc.VAR_SPEED];
            edge = subscription[tc.VAR_ROAD_ID];
            logger.info("edge=%s: speed=%s",edge,speed);


        for signalId in signals:
            belegt = traci.edge.getContextSubscriptionResults(signals[signalId][0]);
            if belegt is not None:
                train = list(belegt.keys())[0];
                logger.info("blockabschnitt belegt: %s durch %s",signalId,train);
                blockabschnitt_belegt[signalId] = train;
            frei = traci.edge.getContextSubscriptionResults(signals[signalId][1]);
            if frei is not None:
                train = list(frei.keys())[0];
                if signalId in blockabschnitt_belegt and blockabschnitt_belegt[signalId] == train:
                    del blockabschnitt_belegt[signalId];
                    logger.info("blockabschnitt frei: %s durch %s",signalId,train);

            if not signalId in blockabschnitt_belegt: #Blockabschnitt belegt
                logger.info("blockabschnitt frei: %s ",signalId);
                traci.trafficlight.setRedYellowGreenState(signalId, "G");
            else:
                logger.info("blockabschnitt belegt: %s durch %s",signalId,blockabschnitt_belegt[signalId]);
                traci.trafficlight.setRedYellowGreenState(signalId, "r");

        step_counter +=  1
        #time.sleep(traci.simulation.getDeltaT())
except traci.exceptions.FatalTraCIError:
    logger.warning('Something went wrong with SUMO. Maybe the connection was closed.')

logger.info("Close SUMO");
traci.close()
