from .weekly_template import read_config, WeeklyTemplate
import os

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

Weekly8x5 = WeeklyTemplate(
    read_config(os.path.join(LOCAL_DIR, "uk_weekly_8x5.yaml")))
