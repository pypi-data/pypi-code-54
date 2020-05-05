from pyrace.setting import Setting
from pyrace.model.modelregistery import ModelRegistery
from pyrace.model.car import Car

class Model:
    def __init__(self, model_name, vue):

        self.metadata = ModelRegistery.METADATA[model_name]

        self.vue = vue
        self.car = Car(self.vue.metadata, self.metadata)
        
        self.progress = 0
        
        self.state = self.car.get_state(self.vue)
        self.reward = 0
        self.done = False
        self.info = {}
        self.history = [(self.state, self.reward, self.done, self.info)]


    def step(self, action):
        
        if self.car.step(action) :

            self.state = self.car.get_state(self.vue)

            progress = self.vue.get_progress(self.car.position)
            self.reward = progress - self.progress
            if self.reward > 1000 :
                self.reward = -self.reward  # avoid going directly back during after start. 
                self.done = True

            self.progress = progress

            if not self.vue.is_road(self.car.position):
                self.done = True

            self.info = {}

            self.history.append((self.state, self.reward, self.done, self.info))
            return self.state, self.reward, self.done, self.info

        else :
            return None







    
