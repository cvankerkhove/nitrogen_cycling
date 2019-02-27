###############################################################################
#nitrogencylcing
#inputcreator.property
#Author(s): Chris VanKerkhove
###############################################################################

import inputs
import soil_1
import classes_1
import nitrogencycling
from Outputs import soilnitrogen
from Outputs import reporthandler

config = inputs.file["config"]
farm = inputs.file["farm"]
soil = farm["soil"]
weather = inputs.file["weather"]
output = inputs.file["output"]
SN = soilnitrogen.SoilNitrogen(output["soil_summary"])

config1 = classes_1.Config(config)
w1 = classes_1.Weather(weather, config1.duration)
s1 = soil_1.Soil(soil, config1)
time = classes_1.Time(config1.duration)
print('CToN')
print(s1.CToN)
for _ in range(365):
    nitrogencycling.daily_nitrogen_cycling_routine(s1, time, w1)
    print('CToN')
    print(s1.CToN)
    nitrogencycling.daily_nitrogen_update(s1, time, w1)
    SN.initialize(s1)
    SN.daily_update(s1, w1, time)
    time.advance()
