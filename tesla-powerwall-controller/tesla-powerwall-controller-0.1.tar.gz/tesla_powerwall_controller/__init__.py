import requests
import json
import argparse

protocol = "https://"
base_api_path = "/api"
power_level_path = base_api_path + "/system_status/soe"

class PowerwallController:
  def __init__(self, host):
    self.base_url = protocol + host

  def get_battery_level(self):
    req = requests.get(self.base_url + power_level_path, verify=False)
    content = req.content.decode("utf-8")
    result = json.loads(content)
    return "The battery is at {} percent".format(int(result['percentage']))
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('host')
  args = parser.parse_args()
  con = TygarwenPowerwallController(args.host)
  print(con.get_battery_level())
