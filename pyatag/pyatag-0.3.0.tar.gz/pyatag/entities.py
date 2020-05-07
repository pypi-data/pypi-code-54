from .const import CLASSES, SENSORS, STATES
import datetime


def convert_time(seconds, sensorclass="time"):
    if sensorclass == "duration":
        return str(datetime.timedelta(seconds=seconds))
    return str(datetime.datetime(2000, 1, 1) + datetime.timedelta(seconds=seconds))


class Report:
    def __init__(self, data, update, setter):
        self._update = update
        self._setter = setter
        self._items = {}
        self._data = data
        self._classes = CLASSES
        self._classes["temp"][1] = STATES["temp_unit"][
            self._data["configuration"]["temp_unit"]
        ]
        self._process_raw(self._data)

    def update(self, data):
        self._data = data
        self._process_raw(self._data)

    def _process_raw(self, raw):

        for grp in ["configuration", "status", "report", "control"]:
            for id, raw_item in raw[grp].items():
                name = SENSORS.get(id)
                obj = self._items.get(name) or self._items.get(id)

                if obj is not None:
                    obj.raw = raw_item
                elif grp == "control":
                    self._items[name or id] = Control(
                        id, raw_item, self._classes, self._setter
                    )
                else:
                    self._items[name or id] = Sensor(id, raw_item, self._classes)

    def values(self):
        return self._items.values()

    def items(self):
        return self._items.values()

    @property
    def report_time(self):
        return self._items["report_time"].state

    def __getitem__(self, obj_id):
        if obj_id in SENSORS:
            return self._items[SENSORS[obj_id]]
        return self._items[obj_id]

    def __iter__(self):
        return iter(self._items.values())


class Sensor:
    """Represents an Atag sensor."""

    def __init__(self, id, raw, classes):
        self.id = id
        self.raw = raw
        self._info = classes.get(self.id.split("_")[-1])
        if id == "tout_avg":
            self._info = classes["temp"]
        self._states = STATES.get(self.id)

    @property
    def name(self):
        return SENSORS.get(self.id) or self.id

    @property
    def sensorclass(self):
        if self._info:
            return self._info[0]

    @property
    def state(self):
        if self.sensorclass in ["time", "duration"]:
            return convert_time(self.raw, self.sensorclass)
        if self.id == "boiler_status":
            return {
                "burner": self.raw % 8 == 8,
                "dhw": self.raw % 4 == 4,
                "ch": self.raw % 2 == 2,
            }
        if self.id == "download_url":
            return self.raw.split("/")[-1]
        if self._states is not None:
            if isinstance(self._states[self.raw], dict):
                return self._states[self.raw]["state"]
            return self._states[self.raw]
        return self.raw

    @property
    def icon(self):
        if self._info:
            return self._info[2]
        if self._states is not None and isinstance(self._states[self.raw], dict):
            return self._states[self.raw]["icon"]
        return None

    @property
    def measure(self):
        if self._info:
            return self._info[1]
        return None

    def __repr__(self):
        return self.name


class Control(Sensor):
    """Represents an Atag control."""

    def __init__(self, id, raw, classes, setter):
        super().__init__(id, raw, classes)
        self._setter = setter
        self._target = None
        self._last_call = None

    @property
    def state(self):
        if self._target:
            if (datetime.datetime.utcnow() - self._last_call).total_seconds() < 15:
                return self._target
            self._target = None
        if self.sensorclass in ["time", "duration"]:
            return convert_time(self.raw, self.sensorclass)
        if self._states:
            if isinstance(self._states[self.raw], dict):
                return self._states[self.raw]["state"]
            return self._states[self.raw]
        if self.id == "dhw_mode_temp":
            return self.raw % 150
        return self.raw

    async def set_state(self, target):
        if self.state == target:
            return True
        self._target = target
        if self._states is not None:
            target = list(self._states.keys())[
                list(self._states.values()).index(target)
            ]
        self._last_call = datetime.datetime.utcnow()
        return await self._setter(**{self.id: target})


class Climate:
    """Main climate entity."""

    def __init__(self, report):
        self._report = report

    @property
    def temp_unit(self):
        """Return temperature unit"""
        return self._report["temp_unit"].state

    @property
    def burnerstatus(self):
        """Returns boolean for burner active"""
        return self._report["boiler_status"].state["burner"]

    @property
    def status(self):
        """Return HVAC action"""
        return self._report["boiler_status"].state["ch"]

    @property
    def flame(self):
        """Return flame level"""
        if self.status:
            return self._report["flame"].state
        return 0

    @property
    def hvac_mode(self):
        """Return the operating mode (Weather or Regular/Heat)"""
        return self._report["ch_control_mode"].state

    async def set_hvac_mode(self, target: str) -> bool:
        """Set the operating mode (Weather or Regular/Heat) """
        await self._report["ch_control_mode"].set_state(target)

    @property
    def preset_mode(self):
        """Return the preset mode (Manual/Auto/Extend/Vacation/Fireplace)"""
        return self._report["ch_mode"].state

    @property
    def preset_mode_duration(self):
        """Return remaining time on preset mode"""
        return self._report["ch_mode_duration"].state

    async def set_preset_mode(self, target: str, **kwargs) -> bool:
        """Set the hold mode (Manual/Auto/Extend/Vacation/Fireplace) """
        await self._report["ch_mode"].set_state(target)

    @property
    def temperature(self):
        """Return current CV temperature"""
        return self._report["room_temp"].state

    @property
    def target_temperature(self):
        return self._report["ch_mode_temp"].state

    async def set_temp(self, target: float):
        """Set target CV temperature"""
        await self._report["ch_mode_temp"].set_state(target)


class DHW:
    """Main dhw entity."""

    def __init__(self, report):
        self._report = report

    @property
    def temp_unit(self):
        """Return temperature unit"""
        return self._report["temp_unit"].state

    @property
    def burnerstatus(self):
        """Returns boolean for burner status"""
        return self._report["boiler_status"].state["burner"]

    @property
    def status(self):
        """Return boolean indicator for heating for DHW"""
        return self._report["boiler_status"].state["dhw"]

    @property
    def flame(self):
        """Return flame level if active for DHW"""
        if self.status:
            return self._report["flame"].state
        return 0

    @property
    def temperature(self):
        """Return water temperature"""
        return self._report["dhw_water_temp"].state

    @property
    def min_temp(self):
        """Return dhw min temperature"""
        return self._report["dhw_min_set"].state

    @property
    def max_temp(self):
        """Return dhw max temperature"""
        return self._report["dhw_max_set"].state

    @property
    def target_temperature(self):
        """Return dhw target temperature"""
        if self.status:
            return self._report["dhw_temp_setp"].state
        return self._report["dhw_mode_temp"].state

    async def set_temp(self, target: float):
        """Set dhw target temperature"""
        await self._report["dhw_target_temp"].set_state(target)
