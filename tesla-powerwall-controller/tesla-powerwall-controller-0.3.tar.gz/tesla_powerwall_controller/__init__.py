import requests
import json
import argparse

protocol = "https://"
base_api_path = "/api"
battery_level_path = base_api_path + "/system_status/soe"
power_levels_path = base_api_path + "/meters/aggregates"


class PowerwallController:
  def __init__(self, host):
    self.base_url = protocol + host

  def get_battery_charge(self):
    req = requests.get(self.base_url + battery_level_path, verify=False)
    content = req.content.decode("utf-8")
    result = json.loads(content)
    val = int(result['percentage'])
    return f"The battery is at {val} percent"

  def get_battery_power(self):
    req = requests.get(self.base_url + power_levels_path, verify=False)
    content = req.content.decode("utf-8")
    result = json.loads(content)
    val = int(result['battery']['instant_power'])
    if val == 0:
      return "The battery is not being used"
    if val < 0:
      return f"The battery is charging at {-val} watts"
    else:
      return f"The battery is supplying {val} watts"

  def get_solar_power(self):
    req = requests.get(self.base_url + power_levels_path, verify=False)
    content = req.content.decode("utf-8")
    result = json.loads(content)
    val = int(result['solar']['instant_power'])
    return f"The solar panels are supplying {val} watts"

  def get_grid_power(self):
    req = requests.get(self.base_url + power_levels_path, verify=False)
    content = req.content.decode("utf-8")
    result = json.loads(content)
    val = int(result['site']['instant_power'])
    if val == 0:
      return "The grid is not being used"
    if val < 0:
      return f"You are exporting {-val} watts"
    else:
      return f"You are importing {val} watts"

  def get_house_power(self):
    req = requests.get(self.base_url + power_levels_path, verify=False)
    content = req.content.decode("utf-8")
    result = json.loads(content)
    val = int(result['load']['instant_power'])
    return f"The house is using {val} watts"

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('host')
  parser.add_argument('measurement', choices=['charge', 'battery', 'solar', 'grid', 'house'])
  args = parser.parse_args()
  con = PowerwallController(args.host)
  if args.measurement == 'charge':
    method = con.get_battery_charge
  elif args.measurement == 'battery':
    method = con.get_battery_power
  elif args.measurement == 'solar':
    method = con.get_solar_power
  elif args.measurement == 'grid':
    method = con.get_grid_power
  elif args.measurement == 'house':
    method = con.get_house_power
  else:
    raise Exception("invalid option")

  print(method())
    
