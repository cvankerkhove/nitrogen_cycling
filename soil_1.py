import math
import nitrogencycling

#------------------------------------------------------------------------------
# Function: daily_soil_routine
# Executes all the daily soil routines
#------------------------------------------------------------------------------
def daily_soil_routine(soil, weather, time):
    '''
    Description:
        Executes all the daily soil routines.

    Args:
        soil: instance of the Soil class
        crop: instance of the Crop class
        weather: instance of the Weather class
        time: instance of the Time class
    '''
    # calculate and update the temperature of the soil layers

    # calculate daily runoff
    soil.dailyInfiltration(weather.rainfall[time.year-1][time.day-1])

    # calculate daily percolation
    soil.dailyPercolation()

    nitrogencycling.daily_nitrogen_cycling_routine(soil, time, weather)

#------------------------------------------------------------------------------
# Function: daily_soil_update
# Update attributes of soil in preparation of following day
#------------------------------------------------------------------------------
def daily_soil_update(soil, weather, time):
    '''
    Description:
        Update attributes of soil in preparation of the following day.

    Args:
        soil: instance of the Soil class
        crop: instance of the Crop class
        weather: instance of the Weather class
        time: instance of the Time class
    '''
    # update current soil water
    soil.updateCurrentSoilWater(weather.rainfall[time.year-1][time.day-1])
    nitrogencycling.daily_nitrogen_update(soil, time, weather)


#-------------------------------------------------------------------------------
# Class: Soil
#        Contains the state of the farm's soil
#-------------------------------------------------------------------------------
class Soil():
    '''
    Contains the state of the farm's soil.
    '''
    listOfSoilLayers = []
    fertilizerApplications = []
    manureApplications = []
    tillageOperations = []


    def __init__(self, data, config):
        '''
        Description:
            Constructs an instance of the Soil class by populating its arrays
            and the necessary values.

        Args:
            data: the information from the json input file
            config: instance of the Config class
        '''
        # Values Initialized by Input
        self.profileDepth = data['ProfileDepth']
        self.profileBulkDensity = data['ProfileBulkDensity']
        self.CN2 = data['CN2'] # unitless, user-defined curve number (empirical)
        # soil erosion attributes
        self.fieldSlope = data['FieldSlope']
        self.slopeLength = data['SlopeLength']
        self.manning = data['Manning']
        self.fieldSize = data['FieldSize']
        self.practiceFactor = data['PracticeFactor']
        self.orgc = data['Orgc']
        self.sand = data['Sand']
        self.silt = data['Silt']

        # soil temperature attributes
        self.soilAlbedo = data['SoilAlbedo']
        self.Tsurf = data['SoilLayers']['Layer1']['InitialTemperature']

        # create soil layers
        for layerName, layerData in data['SoilLayers'].items():
            self.listOfSoilLayers.append(self.SoilLayer(layerName, layerData))

        # sort layers by bottomDepth
        self.listOfSoilLayers.sort(key=lambda x: x.bottomDepth)
        # calculate initial depth of each soil layer
        for x in range(0, len(self.listOfSoilLayers)):
            if x == 0:
                self.listOfSoilLayers[x].depth = self.listOfSoilLayers[x].bottomDepth
            else:
                self.listOfSoilLayers[x].depth = (self.listOfSoilLayers[x].bottomDepth
                    - self.listOfSoilLayers[x-1].bottomDepth)

        # get fertilizer application information
        for fertApp, fertData in data['Fertilizers'].items():
            self.fertilizerApplications.append(self.Fertilizer(fertApp, fertData))

        # get manure application information
        for manureApp, manureData in data['ManureApplication'].items():
            self.manureApplications.append(self.Manure(manureApp, manureData))

        # get tillage application information
        for tillageApp, tillageData in data['TillageOperations'].items():
            self.tillageOperations.append(self.Tillage(tillageApp, tillageData))

        self.convertCurrentSoilWaterToMM() # calculate initial soil water in layer
        self.calculateWiltingWater() # calculate wilting water in layer
        self.calculateFcWater() # calculate field capacity water in layer
        self.calculateSatWater() # calculate saturation water in layer

        # daily output values
        self.runoff = 0.0
        self.Etrans = 0.0
        self.E0 = 0.0
        self.E0_sum = 0.0
        self.Esoil = 0.0

        self.dayInfiltraiton = 0.0
        self.sedimentYield = 0.0
        self.snowCorrectedSed = 0.0

        # daily soil nitrogen values
        self.residue = data['Residue']
        self.freshNMineralRate = data['FreshNMineralRate']
        self.CToN = 0.0
        self.CToP = 0.0
        self.decayRate = 0.0
        self.freshMin = 0.0
        self.freshDecomp = 0.0

        self.freshNConc = 0.0
        self.activeNConc = 0.0
        self.stableNConc = 0.0
        self.NH4Conc = 0.0
        self.enrichmentRatio = 0.0
        self.freshNLoss = 0.0
        self.activeNLoss = 0.0
        self.stableNLoss = 0.0
        self.NH4Loss = 0.0
        self.runoffNO3Conc = 0.0
        self.NO3Runoff = 0.0
        self.runoffNH4Conc = 0.0
        self.NH4Runoff = 0.0

        # soil phosphorus attributes
        self.soilCoverType = data['SoilCoverType']
        #self.pUptake = [[0 for x in range(366)] for y in range(config.endYear+1)]
        self.lightFactor = []
        self.yieldFactor = []
        self.summan = 0.0
        self.summanP = 0.0


    #------ INITIALIZE SOIL NITROGEN POOLS ------------------------------------
        # Calculate initial amount of NO3 in each soil layer;
        # Initial NO3 levels (kg/ha) in the soil are varied by depth as:
        for x in range(0, len(self.listOfSoilLayers)):
            # Initial NO3 levels (kg/ha) in the soil are varied by depth as:
            self.listOfSoilLayers[x].NO3 = ((7 * math.exp
                                (-self.listOfSoilLayers[x].bottomDepth /
                                1000)) * self.listOfSoilLayers[x].bulkDensity
                                 * self.listOfSoilLayers[x].depth) /100

            # Calculate initial amount of organic N in each soil layer;
            # Organic N (Active + Stable, mg/kg): is initialized as:
            self.listOfSoilLayers[x].orgN = (10 ** 4) * (
                self.listOfSoilLayers[x].orgC / 14)

            # Calculate initial amount (kg/ha) of active N in each soil layer;
            self.listOfSoilLayers[x].activeN = ((
                self.listOfSoilLayers[x].fracActiveN *
                self.listOfSoilLayers[x].orgN)*
                self.listOfSoilLayers[x].bulkDensity *
                self.listOfSoilLayers[x].depth) /100

            # Calculate initial amount (kg/ha) of stable N in each soil layer;
            self.listOfSoilLayers[x].stableN = (((1 -
                self.listOfSoilLayers[x].fracActiveN) *
                self.listOfSoilLayers[x].orgN) *
                self.listOfSoilLayers[x].bulkDensity *
                self.listOfSoilLayers[x].depth) /100

            # Calculate initial amount (kg/ha) of NH4 in each soil layer;
            self.listOfSoilLayers[x].NH4 = (self.listOfSoilLayers[x].NH4 *
                            self.listOfSoilLayers[x].bulkDensity *
                            self.listOfSoilLayers[x].depth) /100

        # Fresh N Pool --- only in top soil layer
        self.topLayerFreshN = ((0.0015*self.residue)*
                            self.listOfSoilLayers[0].bulkDensity *
                            self.listOfSoilLayers[0].depth) /100


    #---------------------------------------------------------------------------
    # Class: SoilLayer
    # An instance of this class represents a layer in the soil
    #---------------------------------------------------------------------------
    class SoilLayer():
        '''
        An instance of this class represents a layer in the soil.
        '''
        def __init__(self, layerName, layerData):
            '''
            Description:
                Populates the characteristic values of a soil layer.

            Args:
                layerName: a string which is the name of this layer
                layerData: a dictionary which stores the information for this layer
            '''
            self.name = layerName

            self.bottomDepth = layerData['BottomDepth']
            self.wiltingPoint = layerData['WiltingPoint']
            self.fieldCapacity = layerData['FieldCapacity']
            self.saturation = layerData['Saturation']
            #self.currentSoilWater = layerData['StartingSoilWater']

            self.depth = 0.0 # depth of soil layer
            self.fcWater = 0.0 # constant
            self.satWater = 0.0 # constant
            self.wiltingWater = 0.0 # constant

            self.currentSoilWaterMM = 0.0 # soil water in layer in mm
            self.bulkDensity = layerData['BulkDensity']


            # Variables to calculate dailyEvapotranspiration
            self.topEsoil = 0.0 # evaporation demand at top of layer
            self.bottomEsoil = 0.0 # evaporation demand at bottom of layer
            self.layerEsoil = 0.0 # evaporation demand at layer

            # Variables used for soil temperature
            self.temperature = layerData['InitialTemperature']

            # Variables to calculate dailyPercolation
            self.ksat = layerData['Ksat'] # saturated hydraulic conductivity (mm/h)
            self.TT = 0.0
            self.perc = 0.0 # amount of water that percolates to next layer

            self.labileP = layerData['LabileP'] # labile P in soil layer
            self.clay = layerData['Clay'] # soil clay % in soil layer


            # Variable to simulate nitrogenCycling
            self.orgC = layerData['OrgC%']
            self.activeMineralRate = layerData['ActiveMineralRate']
            self.cationExclusionFraction = layerData['CationExclusionFraction']
            self.denitrificationRate = layerData['DenitrificationRate']
            self.NH4 = layerData['NH4']

            # Initial NO3 levels (kg/ha) in the soil layer:
            self.NO3 = 0.0

            # Organic N (Active + Stable, mg/kg):
            self.orgN = 0.0

            # Initial Active N in layer:
            self.activeN = 0.0

            # Initial Stable N in layer:
            self.stableN = 0.0


            self.nMinAct = 0.0
            self.nitrification = 0.0
            self.volatilization = 0.0
            self.denitrification = 0.0
            self.NO3Conc = 0.0
            self.NO3Perc = 0.0
            self.NH4Conc = 0.0
            self.NH4Perc = 0.0
            self.activeNConc = 0.0
            self.activeNPerc = 0.0
            self.nTrans = 0.0
            self.totNitriVolatil = 0.0

            self.fracActiveN = layerData['FracActiveN']
            self.volatileExchangeFactor = layerData['VolatileExchangeFac']

            # Variables to simulate phosphorus cycling
            self.OMpercent = layerData['OM%']
            self.soilOC = 0.0
            self.psp = 0.0

            self.activeP = 0.0
            self.stableP = 0.0
            self.orgP = 0.0


    #---------------------------------------------------------------------------
    # Class: Fertilizer
    # An instance of this class represents a particular fertilizer and the date
    # of its application
    #---------------------------------------------------------------------------
    class Fertilizer():
        '''
        Description:
            An instance of this class represents a particular fertilizer and the date
        of its application.
        '''
        def __init__(self, FertName, FertData):
            '''
            Constructs an instance of this class by setting the values of its necessary
            fields.

            Args:
                FertName: a string which is the name of this fertilizer
                FertData: a dictionary which holds the rest of the information about
                    this fertilizer
            '''
            self.name = FertName
            self.appYear = FertData['Year']
            self.appDay = FertData['JDay']
            self.fertPMass = FertData['PMass']
            self.depth = FertData['Depth']
            self.percentOnSurface = FertData['%onSurface']

    #---------------------------------------------------------------------------
    # Class: Manure
    # An instance of this class represents a particular manure and the date
    # of its application
    #---------------------------------------------------------------------------
    class Manure():
        '''
        An instance of this class represents a particular manure and the date
        of its application
        '''
        def __init__(self, manureName, manureData):
            '''
            Description:
                Constructs an instance of this class

            Args:
                manureName: a string which represents the name is this manure
                manureData: a dictionary which stores the information for this manure
            '''
            self.name = manureName
            self.type = manureData['Type']
            self.appYear = manureData['Year']
            self.appDay = manureData['Jday']
            self.mass = manureData['Mass']
            self.totalP = manureData['TotalP']
            self.weip = manureData['WEIP']
            self.weop = manureData['WEOP']
            self.dryMatter = manureData['DryMatter']
            self.percentCover = manureData['%Cover']
            self.depth = manureData['Depth']
            self.percentOnSurface = manureData['%onSurface']


    #---------------------------------------------------------------------------
    # Class: Tillage
    # An instance of this class represents a particular tillage and the date
    # of its application
    #---------------------------------------------------------------------------
    class Tillage():
        '''
        An instance of this class represents a particular tillage and the date
        of its application
        '''
        def __init__(self, tillageName, tillageData):
            '''
            Description:
                Constructs an instance of this class.

            Args:
                tillageName: a string which is the name of this tillage
                tillageData: a dictionary which stores the information for this tillage
            '''
            self.name = tillageName
            self.appYear = tillageData['Year']
            self.appDay = tillageData['Jday']
            self.percentIncorporate = tillageData['%Incorporate']
            self.percentMixed = tillageData['%Mixed']
            self.depth = tillageData['Depth']

    #---------------------------------------------------------------------------
    # Class: CropPUptake
    # An instance of this class represents a particular uptake and the date
    # of uptake
    #---------------------------------------------------------------------------

    def calculateFcWater(self):
        '''
        Description:
            Calculates the amount of water in soil profile for a given layer at
            field capacity (mm H2O). Called when soil portion of input is read.
        '''
        for x in range(0, len(self.listOfSoilLayers)):
            self.listOfSoilLayers[x].fcWater = (self.listOfSoilLayers[x].depth
                    * self.listOfSoilLayers[x].fieldCapacity)


    #---------------------------------------------------------------------------
    # Function: calculateSatWater
    # Calculates the amount of water in soil profile for a given layer at
    # saturation (mm H2O). Called when soil portion of input is read.
    #---------------------------------------------------------------------------
    def calculateSatWater(self):
        '''
        Description:
            Calculates the amount of water in soil profile for a given layer at
            saturation (mm H2O). Called when soil portion of input is read.
        '''
        for x in range(0, len(self.listOfSoilLayers)):
            self.listOfSoilLayers[x].satWater = (self.listOfSoilLayers[x].depth
                    * self.listOfSoilLayers[x].saturation)

    #---------------------------------------------------------------------------
    # Function: calculateWiltingWater
    # Calculates the amount of water in soil profile for a given layer at
    # wilting point (mm H2O). Called when soil portion of input is read.
    #---------------------------------------------------------------------------
    def calculateWiltingWater(self):
        '''
        Description:
            Calculates the amount of water in soil profile for a given layer at
            wilting point (mm H2O). Called when soil portion of input is read.
        '''
        for x in range(0, len(self.listOfSoilLayers)):
            self.listOfSoilLayers[x].wiltingWater = (self.listOfSoilLayers[x].
                    depth * self.listOfSoilLayers[x].wiltingPoint)

    #---------------------------------------------------------------------------
    # Function: convertCurrentSoilWaterToMM
    # Calculates the amount of soil water in a given layer in millimeters.
    # Called once when soil portion of input is read.
    #---------------------------------------------------------------------------
    def convertCurrentSoilWaterToMM(self):
        '''
        Description:
            Calculates the amount of soil water in a given layer in millimeters.
            Called once when soil portion of input is read.
        '''
        for x in range(0, len(self.listOfSoilLayers)):
            self.listOfSoilLayers[x].currentSoilWaterMM = (
                self.listOfSoilLayers[x].depth * self.listOfSoilLayers[x]
                .fieldCapacity)

    #---------------------------------------------------------------------------
    # Function: getSumSoilWater
    # Calculates the total amount of soil water in all the soil layers (mm)
    #---------------------------------------------------------------------------
    def getSumSoilWater(self):
        '''
        Description:
            Calculates the total amount of soil water in all the soil layers (mm)
        '''
        totalSoilWater = 0.0
        for soilLayer in self.listOfSoilLayers:
            totalSoilWater += soilLayer.currentSoilWaterMM
        return totalSoilWater

    #---------------------------------------------------------------------------
    # Function: getSumWiltingWater
    # Calculates the total amount of wilting water in all soil layers (mm H2O)
    #---------------------------------------------------------------------------
    def getSumWiltingWater(self):
        '''
        Description:
            Calculates the total amount of wilting water in all soil layers (mm H2O)
        '''
        totalWiltingWater = 0.0
        for soilLayer in self.listOfSoilLayers:
            totalWiltingWater += soilLayer.wiltingWater
        return totalWiltingWater

    #---------------------------------------------------------------------------
    # Function: dailyInfiltration
    # Uses curve number approach (equations taken from SWAT 2009 documentation)
    #---------------------------------------------------------------------------
    def dailyInfiltration(self, dailyRainfall):
        '''
        Description:
            Uses the curve number approach to calculate the daily infiltration of this
            particular uptake.

        Args:
            dailyRainfall: a number which represents the daily rainfall from the Weather class
        '''
        dailyRainfall = float(dailyRainfall)
        # curve number 1
        cn1 = self.CN2 - (20 * (100 - self.CN2)) / (100
                                                    - self.CN2 + math.exp(2.533
                                                    - 0.0636 * (100- self.CN2)))
        # curve number 3
        cn3 = self.CN2 * math.exp(0.00673 * (100 - self.CN2))

        # maximum value of S on any given day (mm H2O)
        sMax = 25.4 * ((1000 / cn1) - 10)

        s3 = 25.4*((1000/cn3) - 10)

        # amount of water in soil profile at field capacity (mm H2O)
        FC = self.profileDepth * self.listOfSoilLayers[0].fieldCapacity

        # amount of water in soil profile at saturation (mm H2O)
        SAT = self.profileDepth * self.listOfSoilLayers[0].saturation

        # soil water content of entire profile, excluding water held at wilting
        # point (mm H2O)
        SW = self.getSumSoilWater() - self.getSumWiltingWater()

        #shape coefficients
        w2 = (math.log(FC /
                      (1 -s3 * (1/sMax)) - FC) -math.log(
                          SAT/(1-2.54*(1/sMax))- SAT
                          )) /(SAT - FC)
        w1 = math.log((FC /
                       (1 - (s3) * (1/sMax)))-
                      FC)+ w2*FC

        # retention paramenter (mm H2O)
        s = sMax * (1 - (SW/(SW + math.exp(w1 - (w2)*(SW)))))

        # when the top soil is frozen, s is modified
        if(self.listOfSoilLayers[0].temperature <= 2):
            s = sMax * (1-math.exp(-0.000862 * s))

        # daily runoff (mm H2O)
        Q = 0.0
        if dailyRainfall > 0.2*s:
            Q = ((dailyRainfall - 0.2*s)**2) / (dailyRainfall + 0.8*s)

        self.runoff = Q

        # daily infiltration (mm H20)
        self.dayInfiltraiton = dailyRainfall - self.runoff

    #---------------------------------------------------------------------------
    # Function: dailyEvapotranspiration
    # Uses Hargreaves method for simplicity (equations taken from SWAT 2009
    # documentation)
    # Step 1: Calculate Potential Evapotranspiration
    # Step 2: Calculate Crop Transpiration
    # Step 3: Calculate Sublimation and Soil Evaporation
    # Step 4: Partition Esoil among different soil layers
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # Function: dailyPercolation
    # (equations taken from SWAT 2009 documentation)
    #---------------------------------------------------------------------------
    def dailyPercolation(self):
        '''
        Description:
            Calculates the daily percolation for this particular uptake.
        '''
        # Calculate value of water available for percolation FOR each layer
        for x in range(0, len(self.listOfSoilLayers)):
            # Volume of water available for percolation (SWperc) in a soil layer
            # is the difference between SW and WP.
            SWperc = 0.0
            if (self.listOfSoilLayers[x].currentSoilWaterMM >=
                                            self.listOfSoilLayers[x].fcWater):
                SWperc = (self.listOfSoilLayers[x].currentSoilWaterMM -
                          (self.listOfSoilLayers[x].fcWater))

            # travel time for percolation (h)
            self.listOfSoilLayers[x].TT = (((self.listOfSoilLayers[x].saturation
                    * self.listOfSoilLayers[x].depth)-
                    self.listOfSoilLayers[x].fcWater)/
                                               self.listOfSoilLayers[x].ksat)
            t = 24 # time step (hours)

            #amount of water that percolates
            self.listOfSoilLayers[x].perc = (SWperc *
                            (1 - math.exp(-t/self.listOfSoilLayers[x].TT)))

    #---------------------------------------------------------------------------
    # Function: updateCurrentSoilWater
    # Updates the soil water within each layer at the end of each day. The
    # model assumes 80% of plant transpiration comes out of the top soil layer
    # and 20% from layer 2.
    #---------------------------------------------------------------------------
    def updateCurrentSoilWater(self, rainfall):
        '''
        Description:
            Updates the soil water within each layer at the end of each day. The
            model assumes 80% of plant transpiration comes out of the top soil layer
            and 20% from layer 2.

        Args:
            rainfall: a number which represents the rainfall from the Weather instance
        '''

        for x in range(0, len(self.listOfSoilLayers)):
            if x == 0:
                self.listOfSoilLayers[x].currentSoilWaterMM = (max
                    (self.listOfSoilLayers[x].wiltingWater,
                    self.listOfSoilLayers[x].currentSoilWaterMM+float(rainfall)
                    -self.runoff-self.listOfSoilLayers[x].layerEsoil
                    -self.listOfSoilLayers[x].perc))#-self.Etrans*0.8))
            elif x== 1:
                    self.listOfSoilLayers[x].currentSoilWaterMM = (max
                        (self.listOfSoilLayers[x].wiltingWater,
                         self.listOfSoilLayers[x].currentSoilWaterMM
                        -self.listOfSoilLayers[x].layerEsoil
                        -self.listOfSoilLayers[x].perc
                        +self.listOfSoilLayers[x-1].perc))#-(self.Etrans*0.2)))
            else:
                    self.listOfSoilLayers[x].currentSoilWaterMM = (max
                        (self.listOfSoilLayers[x].wiltingWater,
                         self.listOfSoilLayers[x].currentSoilWaterMM
                        -self.listOfSoilLayers[x].layerEsoil
                        -self.listOfSoilLayers[x].perc
                        +self.listOfSoilLayers[x-1].perc))

    def annual_reset(self):
        '''
        Description:
            Resets the E0 sum for the next year.
        '''
        self.E0_sum = 0.0
