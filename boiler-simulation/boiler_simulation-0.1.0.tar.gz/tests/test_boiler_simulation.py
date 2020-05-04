from boiler_simulation import __version__
from boiler_simulation import Simulation

#ficout=open("ficout.txt","w") 

count=0
sim=Simulation({
  "service:dhw:production_fan_throttle": 0.70,
  "production:auxiliary:settings:startup_throttle": 0.25,
  "production:auxiliary:timers:ignition": 70000,
  "production:auxiliary:timers:stop": 3000
})
while count < 30:
    if count%10 == 2:
        sim["service:dhw:production_fan_throttle"] = 0.3
        sim.send("service:dhw:START")
    elif count%10 == 5:
        sim["service:dhw:production_fan_throttle"] = 0.8
    elif count%10 == 7:
        sim.send("service:dhw:STOP")
    elif count%10 == 9:
        sim["service:dhw:production_fan_throttle"] = 0.5
    sim.advance_time(500)
    #ficout.write("{} => {}".format(count,sim["service.heating_circuit._1.pump._throttle"]))
    #ficout.write('\n') 
    print("{} => {}".format(count,sim["service:heating_circuit:1:pump:THROTTLE"]))
    count = count + 1

del sim


# def test_version():
#     assert __version__ == '0.1.0'

# def test_simulation():
#     count=0
#     sim=Simulation()
#     while count < 30:
#         if count%10 == 2:
#             sim["service:dhw:production_fan_throttle"] = 0.3
#             sim.send("service:dhw:START")
#         elif count%10 == 5:
#             sim["service:dhw:production_fan_throttle"] = 0.8
#         elif count%10 == 7:
#             sim.send("service:dhw:STOP")
#         elif count%10 == 9:
#             sim["service:dhw:production_fan_throttle"] = 0.5
#         sim.advance_time(500)
#         ficout.write("{} => {}".format(count,sim["service.heating_circuit._1.pump._throttle"]))
#         ficout.write('\n') 
#         print("{} => {}".format(count,sim["service.heating_circuit._1.pump._throttle"]))
#         count = count + 1

#     sim.delSimulation("message")






