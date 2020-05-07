import os
import json
from pathlib import Path
from uuid import uuid4

from jinja2 import Template
from dotenv import load_dotenv

ENV_NAME = os.environ.get('STAGE', 'default')

default_settings = Template(
    "STAGE=app\n"
    "USER_EMAIL={{ user_email }}\n"
    "DEVICE_ID={{ device_id }}\n"
    "CONTROLLER_TOKEN={{ controller_token }}\n"
    "WG_PUBLIC_KEY={{ wg_public_key }}\n"
    "WG_PRIVATE_KEY={{ wg_private_key }}\n"
    "MTU={{ mtu }}\n"
)

destinations = [
  28163, 21507, 1546, 26636, 11276, 18450, 16408, 5145, 27674, 6172, 28701, 6177, 12329, 18475, 2097, 6195, 16953,
  21051, 3132, 21569, 27716, 7755, 3660, 18509, 10315, 4173, 21585, 24154, 23643, 14429, 4706, 3174, 11881, 27249,
  19060, 28788, 25208, 2171, 10363, 26238, 14976, 19078, 15495, 24199, 27277, 15502, 1689, 20637, 4255, 17056, 3758,
  12463, 31410, 4275, 10420, 7353, 21184, 10432, 17602, 26309, 1734, 10438, 16069, 6872, 731, 23260, 29917, 26851,
  28910, 20212, 20728, 25336, 28921, 4347, 3846, 3337, 5899, 12046, 10008, 17691, 17692, 2336, 11557, 21286, 28457,
  11054, 16176, 15156, 3381, 24886, 10040, 15677, 9034, 23374, 19297, 12132, 4455, 6507, 30059, 5485, 22385, 22904,
  6527, 24447, 7553, 29062, 11150, 26511, 24974, 27550, 29599, 30626, 18868, 7617, 6085, 11722, 18894, 22991, 8147,
  6611, 27605, 18392, 9690, 7131, 13276, 23522, 28143, 22513, 21494, 25592
]

ping_destinations = [
  {
    "game": "Fortnite",
    "ip": "3.234.219.249",
    "location": "Herndon, VA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "3.87.253.154",
    "location": "Herndon, VA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "54.153.7.100",
    "location": "Seattle, WA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "18.144.86.188",
    "location": "Seattle, WA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "54.199.233.28",
    "location": "Seattle, WA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "18.196.64.225",
    "location": "Munchen",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "35.178.132.109",
    "location": "London",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "3.8.145.238",
    "location": "London",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "13.239.38.65",
    "location": "Sydney",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "13.239.122.83",
    "location": "Sydney",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "18.228.14.133",
    "location": "Sao Paulo",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "18.228.14.133",
    "location": "Sao Paulo",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.67.12.164",
    "location": "Sao Paulo",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "18.179.15.100",
    "location": "Tokyo",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "3.112.95.5",
    "location": "Tokyo",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "143.131.161.10",
    "location": "Playa Vista, CA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "143.131.161.11",
    "location": "Playa Vista, CA",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "185.82.209.9",
    "location": "Europe",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.94.8.124",
    "location": "Japan (KR/JP and AS Servers)",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.94.6.156",
    "location": "Korea (KR/JP and AS Servers)",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.94.4.146",
    "location": "North America (Ohio)",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.94.13.192",
    "location": "Oceania (OC Server - Sydney)",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.94.7.12",
    "location": "South America (SA Server - São Paulo)",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "52.94.11.166",
    "location": "South-East Asia (SEA Servers - Singapore)",
    "provider": "AWS"
  },
  {
    "game": "Fortnite",
    "ip": "54.222.57.66",
    "location": "China (Beijing) Region",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "104.160.152.3",
    "location": "São Paulo, SP, Brazil",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "104.160.142.3",
    "location": "Frankfurt, Germany",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "104.160.136.3",
    "location": "Miami, FL, United States",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "104.160.131.3",
    "location": "Chicago, Illinois, US",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "104.160.156.1",
    "location": "Sydney, Australia",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "162.249.73.2",
    "location": "München,Germany",
    "provider": "AWS"
  },
  {
    "game": "League Of Legends",
    "ip": "122.11.128.127",
    "location": "Taguig City, Philippines",
    "provider": "AWS"
  },

  {
    "game": "Dota 2",
    "ip": "103.10.125.1",
    "location": "Australia (Sydney)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "200.73.67.1",
    "location": "Chile (Santiago)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "185.25.183.1",
    "location": "Dubai (UAE)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "146.66.155.1",
    "location": "Europe East 1 (Vienna, Austria)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "185.25.182.1",
    "location": "Europe East 2 (Vienna, Austria)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "146.66.152.2",
    "location": "Europe West 1 (Luxembourg)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "146.66.158.1",
    "location": "Europe West 2 (Luxembourg)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "116.202.224.146",
    "location": "India (Kolkata)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "191.98.144.1",
    "location": "Peru (Lima)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "146.66.156.2",
    "location": "Russia 1 (Stockholm, Sweden)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "185.25.180.1",
    "location": "Russia 2 (Stockholm, Sweden)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "103.28.54.16",
    "location": "SE Asia 1 (Singapore)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "103.10.124.1",
    "location": "SE Asia 2 (Singapore)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "197.80.200.1",
    "location": "South Africa 2 (Cape Town)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "197.84.209.1",
    "location": "South Africa 3 (Cape Town)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "196.38.180.1",
    "location": "South Africa 4 (Johannesburg)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "205.185.194.1",
    "location": "South America 1 (Sao Paulo)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "209.197.25.1",
    "location": "South America 2 (Sao Paulo)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "209.197.29.1",
    "location": "South America 3 (Sao Paulo)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "208.78.164.2",
    "location": "US East (Sterling, VA)",
    "provider": "Unknown"
  },
  {
    "game": "Dota 2",
    "ip": "192.69.96.1",
    "location": "US West (Seattle, WA)",
    "provider": "Unknown"
  },

  {
    "game": "PUBG",
    "ip": "13.210.41.168",
    "location": "Sydney",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "54.222.57.66",
    "location": "China (Beijing) Region",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.5.174",
    "location": "Ireland Region",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.15.28",
    "location": "London Region",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "185.82.209.9",
    "location": "Europe",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.8.124",
    "location": "Japan (KR/JP and AS Servers)",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.6.156",
    "location": "Korea (KR/JP and AS Servers)",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.4.146",
    "location": "North America (Ohio)",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.13.192",
    "location": "Oceania (OC Server - Sydney)",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.7.12",
    "location": "South America (SA Server - São Paulo)",
    "provider": "Unknown"
  },
  {
    "game": "PUBG",
    "ip": "52.94.11.166",
    "location": "South-East Asia (SEA Servers - Singapore)",
    "provider": "Unknown"
  }
]

inspector_path = "/etc/noia-inspector"

inspector_file = Path(f"{inspector_path}/{ENV_NAME}.env")
dest_file = Path(f"{inspector_path}/destinations.json")
ping_dest_file = Path(f"{inspector_path}/ping_destinations.json")

inspector_dir = Path(f"{inspector_path}")

if not inspector_dir.is_dir():
    inspector_dir.mkdir()
if not dest_file.is_file():
    dest_file.write_text(json.dumps(destinations))
if not ping_dest_file.is_file():
    ping_dest_file.write_text(json.dumps(ping_destinations))
if inspector_file.is_file():
    print("Default config found")
else:
    print("Default config not found, creating new")
    user_email = input("Enter your email : ")
    controller_token = input("Enter your jwt token : ")
    while True:
        wg_public_key = input("Enter your wireguard public key location default - /etc/wireguard/publickey : ")
        if not wg_public_key:
            wg_public_key = "/etc/wireguard/publickey"
        if Path(f"{wg_public_key}").is_file():
            break
        input(f"Could not find wireguard public key in {wg_public_key}, Try again : ")
    while True:
        wg_private_key = input("Enter your wireguard private key location default - /etc/wireguard/privatekey : ")
        if not wg_private_key:
            wg_private_key = "/etc/wireguard/privatekey"
        if Path(f"{wg_private_key}").is_file():
            break
        input(f"Could not find wireguard private key in {wg_private_key}, Try again : ")

    rendered = default_settings.render(
        user_email=user_email, device_id=f"AMBASSADOR-{uuid4()}",
        controller_token=controller_token, wg_public_key=wg_public_key, wg_private_key=wg_private_key, mtu=1420
    )
    inspector_file.write_text(rendered)


ENV_NAME = os.environ.get('STAGE', 'default')

env_path = Path('/etc/noia-inspector') / f'{ENV_NAME}.env'
load_dotenv(dotenv_path=env_path)
