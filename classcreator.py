###############################################################################
#nitrogencylcing
#inputcreator.property
#Author(s): Chris VanKerkhove
###############################################################################

import inputs
import soil_1
import classes_1
import nitrogencycling

config = inputs.file["config"]
farm = inputs.file["farm"]
soil = farm["soil"]
weather = inputs.file["weather"]

config1 = classes_1.Config(config)
w1 = classes_1.Weather(weather, config1.duration)
s1 = soil_1.Soil(soil, config1)
time = classes_1.Time(config1.duration)
nitrogencycling.daily_nitrogen_cycling_routine(s1, time, w1)
nitrogencycling.daily_nitrogen_update(s1, time, w1)
