import enum
from smear.uiterm import markup_print


class SmearingEngines:
    EIC_SMEAR = 'eic_smear'
    JLEIC_SMEAR = 'jleic_smear'


class DetectorDescription:
    def __init__(self, version='', description='', flag='', engine='eic_smear', link=''):
        self.version = version
        self.description = description
        self.engine = engine
        self.link = link


detectors = {
    "yfhandbook": DetectorDescription(
        version='v1.0.0',
        description="Strict to the handbook table, handbook detector by Yulia Furletova",
        link='eic_smear/ESDetectorHandBook_v1_0_4.cc',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "jleic": DetectorDescription (
        version='1.0.2',
        description="Yulia Furletova smear using JLEIC parameters",
        link='',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "jleic-v1.0.1": DetectorDescription(
        version='1.0.1',
        description="Yulia Furletova smear using JLEIC parameters",
        link='',
        engine=str(SmearingEngines.JLEIC_SMEAR)
    ),
    "handbook": DetectorDescription(
        version='v1.0.4',
        description="Interpretation of handbook table by Kolja Kauder",
        link='eic_smear/ESDetectorHandBook_v1_0_4.cc',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "beast": DetectorDescription(
        version='v1.0.4',
        description="BeAST",
        link='ESDetectorBeAST_v1_0_4.cc',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "ephenix": DetectorDescription(
        version='v1.0.4',
        description="ePHENIX",
        link='ESDetectorEPHENIX_v1_0_4.cc',
        engine=str(SmearingEngines.EIC_SMEAR)
    ),
    "zeus": DetectorDescription(
        version='v1.0.4',
        description="Zeus",
        link='ESDetectorZeus_v1_0_0.cc',
        engine=str(SmearingEngines.EIC_SMEAR)
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
