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
steps=260
sumo_cmd="sumo"
config_path="examples/frankfurt-bahnhof.sumocfg"
step_length=1

traci.start([sumo_cmd, '--no-warnings', '-c', config_path])
vehID="rail1"

traci.vehicle.subscribe(vehID, (tc.VAR_SPEED, tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION, tc.VAR_POSITION))
logger.info("subscribe %s",traci.vehicle.getSubscriptionResults(vehID))
try:
    while step_counter < steps:
        logger.debug('Next step (%d of %d)', step_counter , steps)
        traci.simulationStep()

        logger.info("subscribe %d: %s",step_counter,traci.vehicle.getSubscriptionResults(vehID))


        
        step_counter +=  1
        #time.sleep(traci.simulation.getDeltaT())
except traci.exceptions.FatalTraCIError:
    logger.warning('Something went wrong with SUMO. Maybe the connection was closed.')

logger.info("Close SUMO");
traci.close()
