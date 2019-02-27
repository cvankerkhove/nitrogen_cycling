file = {

    "config":
    {
        "StartYear" : 2008,
        "EndYear" : 2009,
        "output_dir": "Outputs/"
    },

    "weather": "nitrogen_cycling/weatherfile.csv",

    "output":
    {
        "soil_summary":
        {
            "active": True,
            "report_name": "Soil Summary",
            "file_name": "soil_summary.csv"
        },
        "ration_report":
        {
            "active": True,
            "report_name": "Ration Report",
            "file_name": "ration_report.txt"
        },
        "soil_nitrogen":
        {
            "active": True,
            "report_name": "Soil Nitrogen",
            "file_name": "soil_nitrogen.csv"
        },
        "crop_report":
        {
            "active": True,
            "report_name": "Crop Report",
            "file_name": "crop_summary.csv"
        }
    },

    "farm":
    {
        "crop":
        {
            "corn":
            {
                "crop_name": "corn",
                "crop_type": "annual",
                "fix_nitrogen": False,

                "planting_date": 121,
                "harvest_date": 319,

                "harvest_index": 0.65,
                "harvest_eff": 0.9,
                "HI_opt": 0.6,
                "HI_min": 0.3,
                "init_residue": 8000,

                "min_temp_for_growth": 10,
                "max_temp_for_growth": 30,
                "opt_temp_for_growth": 25,
                "HU_for_maturity": 1200,

                "fr_PHU_50" : 0.5,
                "fr_PHU_100" : 1.0,
                "fr_PHU_sen": 0.90,
                "fr_PHU_1": 0.15,
                "fr_PHU_2": 0.50,
                "fr_LAI_1": 0.05,
                "fr_LAI_2": 0.95,

                "LAI_max": 3,
                "radiation_use_efficiency": 39,
                "light extinction coefficient": 0.65,

                "z_root_max": 2000,

                "fr,n1": 0.047,
                "fr,n2": 0.0177,
                "fr,n3": 0.0138,
                "fr,n~3": 0.01381,
                "beta_n": 10,

                "beta_w": 10,
                "epco": 0.5,

                "fr,p1": 0.0048,
                "fr,p2": 0.0018,
                "fr,p3": 0.0014,
                "fr,p~3": 0.00141,
                "beta_p": 10,


                "TESTING_Ea_sum" : [251.2544561385, 313.6495119524],
                "TESTING_Eo_sum" : [329.6603213136, 372.2587849571],
                "TEST_DATA" : "Inputs/TEST_INPUTS.csv"
            }
        },
        "soil":
        {
            "ProfileDepth": 450,
            "ProfileBulkDensity": 1.16525,
            "CN2": 86.00,
            "FieldSlope": 0.02,
            "SlopeLength": 7,
            "Manning": 0.4,
            "FieldSize": 1.0,
            "PracticeFactor": 0.25,
            "Orgc": 1,
            "Sand": 15,
            "Silt": 65,
            "SoilAlbedo": 0.16,
            "Residue": 8000,
            "FreshNMineralRate": 0.05,
            "SoilCoverType": "BARE",

            "SoilLayers":
            {
                "Layer1":
                {
                    "BottomDepth": 150,
                    "WiltingPoint": 0.1,
                    "FieldCapacity": 0.33,
                    "Saturation": 0.5,
                    "Ksat": 29.2,
                    "CationExclusionFraction": 0.0,
                    "Clay": 21,
                    "InitialTemperature": -4.098,
                    "BulkDensity": 1.23,
                    "OrgC%": 2.0,
                    "NH4": 1,
                    "FracActiveN": 0.02,
                    "LabileP": 15,
                    "ActiveMineralRate": 0.0001,
                    "VolatileExchangeFac": 0.15,
                    "DenitrificationRate": 0.01,
                    "StartingSoilWater": 0.3,
                    "OM%": 1.9
                },
                "Layer2":
                {
                    "BottomDepth": 1000,
                    "WiltingPoint": 0.1,
                    "FieldCapacity": 0.3,
                    "Saturation": 0.5,
                    "Ksat": 13.2,
                    "CationExclusionFraction": 0.0,
                    "Clay": 33,
                    "InitialTemperature": -1.978,
                    "BulkDensity": 1.16,
                    "OrgC%": 1,
                    "NH4": 1,
                    "FracActiveN": 0.02,
                    "LabileP": 15,
                    "ActiveMineralRate": 0.0001,
                    "VolatileExchangeFac": 0.15,
                    "DenitrificationRate": 0.01,
                    "StartingSoilWater": 0.3,
                    "OM%": 1.9
                },
                "Layer3":
                {
                    "BottomDepth": 2000,
                    "WiltingPoint": 0.1,
                    "FieldCapacity": 0.30,
                    "Saturation": 0.5,
                    "Ksat": 20,
                    "CationExclusionFraction": 0.0,
                    "Clay": 20,
                    "InitialTemperature": 8,
                    "BulkDensity": 1.8,
                    "OrgC%": 1.2,
                    "NH4": 1,
                    "FracActiveN": 0.02,
                    "LabileP": 174,
                    "ActiveMineralRate": 0.00005,
                    "VolatileExchangeFac": 0.15,
                    "DenitrificationRate": 0.01,
                    "StartingSoilWater": 0.3,
                    "OM%": 1.9
                }
            },

            "Fertilizers":
            {
                "Application1":
                {
                    "Year": 2008,
                    "JDay": 179,
                    "PMass": 25.0,
                    "Depth": 3.0,
                    "%onSurface": 0.25
                }
            },

            "ManureApplication":
            {
                "Application1":
                {
                    "Type": "DAIRY",
                    "Year": 2009,
                    "Jday": 200,
                    "Mass": 1000.0,
                    "TotalP": 0.025,
                    "WEIP": 0.50,
                    "WEOP": 0.05,
                    "DryMatter": 0.05,
                    "%Cover": 0.5,
                    "Depth": 0.0,
                    "%onSurface": 100.0
                }
            },

            "TillageOperations":
            {
                "Operation1":
                {
                    "Year": 2008,
                    "Jday": 365,
                    "%Incorporate": 0.5,
                    "%Mixed": 0.30,
                    "Depth": 15.0
                },
                "Operation2":
                {
                    "Year": 2009,
                    "Jday": 365,
                    "%Incorporate": 0.5,
                    "%Mixed": 0.30,
                    "Depth": 15.0
                },
                "Operation3":
                {
                    "Year": 2010,
                    "Jday": 365,
                    "%Incorporate": 0.5,
                    "%Mixed": 0.30,
                    "Depth": 15.0
                }
            },

            "CropPUptake":
            {
                "Uptake1":
                {
                    "Year": 2008,
                    "PUptake": 15.0
                },
                "Uptake2":
                {
                    "Year": 2009,
                    "PUptake": 15.0
                }

            }
        },

        "animal":
        {
            "Herd":
            {
                "cow_num": 100
            },
            "housing": "barn",
            "ration":
            {
                "user_input": False,
                "formulation_interval": 7
            }
        },

        "feed":
        {
            "feed_library": "Inputs/first_feed_library.csv",

            "available_feeds":
            [
              "CG",
              "PROT",
              "UPROT",
              "FAT",
              5,
              "HMC"
            ]
        }
    }
}
