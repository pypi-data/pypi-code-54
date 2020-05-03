
class ModelRegistery:

	METADATA = {

		'car_v1' : {
			'model_name' : 'car_v1',
			'description' : 'In this model the car have 5 sensors and a discret action space',
			'observation_space' : {'name' : 'basic_sensor',
										'observer_type' : 'Camera',
										'dimension' : (5,),
										'values_type' : 'float',
										'values_range' : [0, 20]
			},
			'action_space' : {'descritpion' : 'Discret orientation and discret acceleration',
								'type': 'discret',
								'dimension' : (3,),	
								'actioner_names' : ['accelerator', 'breaks', 'wheel_orientation'],
								'actioner_types' : {'accelerator': 'int', 'breaks': 'int', 'wheel_orientation': 'int'},
								'actioner_ranges' :  {'accelerator': {0, 1, 2}, 'breaks': {0, 1, 2}, 'wheel_orientation':{-50, -20, 0, 20, 50}}

			}
		},

		'car_v2' : {
			'model_name' : 'car_v2',
			'description' : 'In this model the car have 5 sensors and a continuous action space',
			'observation_space' : {'name' : 'basic_sensor',
										'observer_type' : 'Camera',
										'dimension' : (5,),
										'values_type' : 'float',
										'values_range' : [0, 20]
			},
			'action_space' : {'descritpion' : 'Discret orientation and discret acceleration',
								'type': 'discret',
								'dimension' : (3,),	
								'actioner_names' : ['accelerator', 'breaks', 'wheel_orientation'],
								'actioner_types' : {'accelerator': 'float', 'breaks': 'float', 'wheel_orientation': 'float'},
								'actioner_ranges' :  {'accelerator': [0, 1], 'breaks': [0, 1], 'wheel_orientation':[-90, 90]}


			}
		}

	}