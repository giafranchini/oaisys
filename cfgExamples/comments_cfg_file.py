#COPY OF THE JSON CONFIG FILE IN ORDER TO COMMENT ITS CONTENT:
#how to run the simulation
#change the name of the config file each time obviously
#in src/assets/stages/defaultcfg/ there are other "noises" to generate the mesh
#python3 run_oaisys.py --blender-install-path /home/user/Thesis --config-file /home/user/Thesis/oaisys/cfgExamples/cfg_mars_t2.json

#in config mars t2 i tried modifying camera parameters and also some parameters of rock1 and dust in the air

{
    #component responsible of the setup of all main parameters for the simulation
	"SIMULATION_SETUP": {
		"outputPath":"",
		"defaultCfg": "",
		"numBatches":2,
		"numSamplesPerBatch":3,
		"renderImages": true,
		"saveBlenderFiles": true,
		"outputIDOffset":0
	},

    #informations on which render passes are activated
	"RENDER_SETUP": {

        #contains the general parameters of a component
		"GENERAL": {
					"renderEngine":"CYCLES", #keep it like this, don't change the render engine
					"renderFeatureSet":"EXPERIMENTAL",
					"renderDevice": "GPU",
					"performanceTilesX": 256,
					"performanceTilesY": 256
					},

        #the section of a specific component is contained in the relative list, contains all the modules used by a component
		"RENDER_PASSES": [{
							"type": "RGBDPass", #defines which module will be loaded-->RGBD so responsible of rgb and depth properties of the images
							"passParams": { #defines the dictionary of parameters passed to the module
											"numIter": 1, #how often the pass is executed
											"renderDepthActive": true, #boolean telling if depth is rendered or not
											"renderSamples":128, #how many render samples are used by blender for an image, should be ok at 128
											"lightPathesMaxBounces": 6 #how many times a light beam is allowed to bounce, 6 should be fine. More high it is more accurate is the render but will also take more time
										}
							},
							{
							"type": "SemanticPass", #
							"passParams": {
											"numIter": 2, #two render passes are dedicated to the semantic properties of the image
											"renderSamples":1 #do not change it, keep it at 1 since is good enough
										  }
							},
							{
							"type": "InstancePass",
							"passParams": {
											"numIter": 1,
											"renderSamples":1
										}
							}]
				
	},
    #NOTES:
    #we may delete the instancepass since we are only interested in the semantic segmentation and the rgbd values


    #modules interacting in the compositor editor of blender are defined here, for example here is activated blooming effect
	"RENDER_POST_PROCESSING_EFFECTS_SETUP": {
		"GENERAL": {
					"renderPasses": ["combined"]
					},
		"POST_EFFECTS": [{
							"type": "BloomEffect",
							"effectParams": {
											"quality": "HIGH",
											"threshold": 0.8
										}
							}
						]
				
	},


    #all sensors are defined here
	"SENSOR_SETUP": {
		"GENERAL": {

                    #movement behaviour of the base frame
					"baseMovement": {	"movementType": "randomEuclideanTarget",
										"hoverBaseModeEnabled": true,
									    "hoverBaseStage":"landscape01",
										"hoverBaseDistance":1.5,
										"hoverBaseDistanceNoise": 0.5
									},
					"sensorMovementType":"randomEuclideanTarget",
					"hoverBaseModeEnabled": true,
					"hoverBaseStage":"landscape01",
					"hoverBaseDistance":1.5,
					"hoverBaseDistanceNoise": 0.5,
					"hoverTargetModeEnabled": true,
					"hoverTargetStage":"landscape01",
					"hoverTargetDistance":0.0,
					"positionOffsetEnabled":true,
					"randomEuclideanPosMin": [-8.0,-8.0,0.0],
					"randomEuclideanPosMax": [8.0,8.0,5.0],
					"randomEuclideanEulerMin": [0,0,0],
					"randomEuclideanEulerMax": [0,0,0],
					"randomTargetPosMin": [-20.0,-20.0,-3.0],
					"randomTargetPosMax": [20.0,20.0,-0.2],
					"randomTargetEulerMin": [0,0,0],
					"randomTargetEulerMax": [0,0,0],
					"randomTargetRollDeg": [-10.0,10.0],
					"targetObjectActive":true,
					"tragetObjectMovementType":"random"},
        
        #all the sensors to be used are contained in this list            
		"SENSORS": [{"type": "SensorCameraRGBD",
					"sensorParams": {	
										"outputBaseName":"sensor_1",
										"imageResolution": [640,480],
										"KMatrix": [541.14,	0,			320,
													0,		541.14,		240,
													0,		0,			1],
										"transformation": [0.0,0,0,1.0,0.0,0,0],
										"triggerInterval": 1,
										"renderPasses": { #specifies for which render passes they are active
														"RGBDPass": {"activationSlot":[1], "DepthEnabled": true}, #1 means the sensor is active in this pass while 0 means deactivation
														"SemanticPass": {"activationSlot":[1,1]},
														"InstancePass": {"activationSlot":[1]}
														}
									}
					},
                    ]
	},


    #includes all modules changing the world setup of blender, also the light is set up here
	"ENVIRONMENT_EFFECTS_SETUP": {

		"GENERAL": {"backgroundStrength": [0.1],
					"stepInterval": 1
					},

		"ENVIRONMENT_EFFECTS": [	{"type": "EnvLightBlenderSky",
									"stepInterval": 1,
									"environmentEffectsParams": {
																"stepIntervalOption": "GLOBAL",
																"stepInterval": 1,
																"SunSize": [0.545],
																"SunIntensity": [1.0],
																"SunElevation": [15.0,90.0],
																"SunRotation": [0.0,360.0],
																"SunAltitude": [3000.0,3350.0],
																"AirDensity": [1.0,2.0],
																"DustDensity": [0.0,10.0],
																"OzoneDensity": [0.0,5.0],
																"SunStrength": [0.0001,0.1],
																"passParams": 	{ "RGBDPass": {"rgbIDVec": [1,-1,-1,-1]},
																				  "SemanticPass": {"semanticIDVec": [500,500,500,500]},
																				  "InstancePass": {"instanceIDVec": [-1]}
																				}
															}

									}
								]
	},


    #contains all the informations about the assets used for the simulation
	"ASSET_SETUP": { #contains three specific sections other than general



		"GENERAL": {},



		#defines the terrain materials used in the simulator, each material module is assigned to one stage module
		"MATERIALS": [	{"name": "terrain_01", #textures applied to the stages
						"type":"MaterialTerrain",
						"materialParams":{
											"general": {"minNumMixTerrains":1,
														"maxNumMixTerrains":2,
														"hardLabelBorders":true,
														"withReplacement":true,
														"dispMidLevel":0.0,
														"dispScale":1.0,
														"normalStrength":1.0,
														"mergingNoise": {
															"Scale": [3.0,7.0],
															"Detail": [1.0,3.0],
															"Roughness": [0.2,0.5],
															"Distortion": [0.0,0.6]
														}},
											"terrainTextureList": [ #this is a list of textures which will be merged togheter to create a material in the stage
														{
															"templatePath": "oaisys_data/examples/assets/materials/rock_ground/rock_ground.json",
                                                            #to define a template we need four 4k images
															"passParams": 	{ "rgb": {},
																			  "semantic_label": {"labelIDVec": [[30,500,5,]]},
																			  "instance_label": {}
																			},
															"colorAdjustment": 	{
																"cColorPoints": [[0.70758,0.30417]],
																"rColorPoints": [[0.50909,0.48750]],
																"gColorPoints": [[0.5,0.5]],
																"bColorPoints": [[0.5,0.48750]]
															},
															"size": 120.0,
															"dispStrength": 0.03
														},
														{
															"templatePath": "oaisys_data/examples/assets/materials/dry_ground_01/dry_ground_01.json",
															"passParams": 	{ "rgb": {},
																			  "semantic_label": {"labelIDVec": [[30,500,5,2]]},
																			  "instance_label": {}
																			},
															"colorAdjustment": 	{
																"cColorPoints": [[0.70758,0.30417]],
																"rColorPoints": [[0.50909,0.48750]],
																"gColorPoints": [[0.5,0.5]],
																"bColorPoints": [[0.5,0.48750]]
															},
															"size": 120.0,
															"dispStrength": 0.03
														}
														]
								}}
					  ],

		#responsible for all the stages in the simulation
		#stages are the meshes on which materials are applied and objects are placed, usually one stage is enough  hut they can be more than one
		"STAGES": [{"name": "landscape01", #name of the stage MUST be unique
					 "type": "StageBlenderLandscape",
					 "stageParams": {
							"stageName": "landscape",
							"stageSizeX": 200,
							"stageLandscapePreset": "another_noise",
							"assetMaterial": "terrain_01", #material applied to the stage
							"landscapeParams": {"random_seed":[0,1000]}
					 		}
					}
					],

		#here all the objects used in the simulator are defined
		"MESHES": [ {"name": "rock1",
					 "type": "MeshMultipleRandom",
					 "meshParams": {
							"meshFilePath":"oaisys_data/blender_files/rocks/rocks_01.blend",
							"meshInstanceName": "rock_02",
							"numberInstances": [300,500],
							"randomSwitchOnOff": false,
							"instanceLabelActive": false,
							"useDensityMap": true,
							"densityMapSettings": {
								"numberInstances": [13000,15000],
								"densityMap": {
									"noiseType": "VORONOI",
									"intensity": 1.2, #determines how strong is the effect of the density map in the distributions of instances
									"size": 0.2, #determines the scale or size of the density map pattern. It controls how much space each instance occupies in the density map.
									"colorStopPosition_0":0.6,
									"colorStopColor_0":[0,0,0,1],
									"colorStopPosition_1":1.0,
									"colorStopColor_1":[1,1,1,1]
								}
							},
							"defaultSize": 1.0, #Default size of the mesh instances.
							"strengthRandomScale": 1.0, #Strength of random scaling applied to instances.
							"randomRotationEnabled": true,
							"rotationOptionMode":"NOR",
							"rotationOptionFactor":0.4,
							"rotationOptionPhase":0.3,
							"rotationOptionPhaseRandom":0.7,
							"meshEmitter":"STAGE",
							"appliedOnStage":"landscape01",
							"passParams": 	{ 	"rgb": {},
												"semantic_label": {"labelIDVec": [[60,200,0,200]]},
												"instance_label": {}
											}
					 		}
					},
					{"name": "rock2",
					 "type": "MeshMultipleRandom",
					 "meshParams": {
							"meshFilePath":"oaisys_data/blender_files/rocks/rocks_01.blend",
							"meshInstanceName": "rock_02",
							"numberInstances": [300,500],
							"randomSwitchOnOff": false,
							"instanceLabelActive": true,
							"useDensityMap": true,
							"densityMapSettings": {
								"numberInstances": [5000,8000],
								"densityMap": {
									"noiseType": "VORONOI",
									"intensity": 1.2,
									"size": 0.2,
									"colorStopPosition_0":0.6,
									"colorStopColor_0":[0,0,0,1],
									"colorStopPosition_1":1.0,
									"colorStopColor_1":[1,1,1,1]
								}
							},
							"defaultSize": 3.0,
							"strengthRandomScale": 1.0,
							"randomRotationEnabled": true,
							"rotationOptionMode":"NOR",
							"rotationOptionFactor":0.4,
							"rotationOptionPhase":0.3,
							"rotationOptionPhaseRandom":0.7,
							"meshEmitter":"STAGE",
							"appliedOnStage":"landscape01",
							"passParams": 	{ 	"rgb": {},
												"semantic_label": {"labelIDVec": [[60,200,0,200]]},
												"instance_label": {}
											}
					 		}
					}
				]

	}

}
