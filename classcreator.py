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
from Outputs import outputhandler

def daily_simulation():
    '''Executes the daily simmulation routines'''
    soil_1.daily_soil_routine(s1, w1, time)
    soil_1.daily_soil_update(s1, w1, time)
    print('CToN')
    print(s1.CToN)
    SN.daily_update(s1, w1, time)
    time.advance()

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

outputhandler.initialize_output_dir("outputs/Sample_Farm_Outputs/")
SN.initialize(s1)

while not time.end_year():
    daily_simulation()
#SN.annual_update(s1, w1, time)
#SN.write_annual_report(time.year)
#SN.annual_flush()
