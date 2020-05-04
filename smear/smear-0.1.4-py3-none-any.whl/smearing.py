import enum
from smear.uiterm import markup_print


class SmearingEngines:
    EIC_SMEAR = 'eic_smear'
    JLEIC_SMEAR = 'jleic_smear'


class DetectorDescription:
    def __init__(self, version = '', description = '', flag = '', engine = 'eic_smear', link=''):
        self.version = version
        self.description = description
        self.flag = flag
        self.engine = engine
        self.link = link


detectors = {
    "handbook": DetectorDescription(
        version='0.1.0',
        description="Strict to the handbook table, handbook detector by Yulia Furletova",
        link='',
        flag='eic_smear:detector=handbook',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),

    "jleic": DetectorDescription (
        version='0.1.0',
        description="ulia Furletova smear using JLEIC parameters",
        link='',
        flag='eic_smear:detector=handbook',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
}


def print_detectors():
    for name, detector in detectors.items():
        markup_print("\n<blue>detector</blue>: {}".format(name))
        markup_print(" <b>version</b> : {}".format(detector.version))
        markup_print(" <b>descr.</b>  : {}".format(detector.description))
        markup_print(" <b>link</b>    : {}".format(detector.link))
        markup_print(" <b>engine</b>  : {}".format(detector.engine))


if __name__ == '__main__':
    print_detectors()
