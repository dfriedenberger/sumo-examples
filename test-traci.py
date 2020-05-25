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
traci.vehicle.subscribe(vehID, (tc.VAR_SPEED, tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION, tc.VAR_POSITION))

try:
    while step_counter < steps:
        logger.debug('Next step (%d of %d)', step_counter , steps)
        traci.simulationStep()
        subscription = traci.vehicle.getSubscriptionResults(vehID)
        if subscription is not None:
            speed = subscription[tc.VAR_SPEED];
            edge = subscription[tc.VAR_ROAD_ID];
            logger.info("step=%d edge=%s: speed=%s",step_counter,edge,speed);

        if step_counter == 200: # stop 
            traci.vehicle.setSpeed(vehID,0)
        if step_counter == 400: # stop 
            traci.vehicle.setSpeed(vehID,-1)  
        
        step_counter +=  1
except traci.exceptions.FatalTraCIError:
    logger.warning('Something went wrong with SUMO. Maybe the connection was closed.')

logger.info("Close SUMO");
traci.close()
