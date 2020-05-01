# -*- coding: utf-8 -*-
from iscc import const


class GMT:
    """Generic Media Type"""

    IMAGE = "image"
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"


SUPPORTED_MIME_TYPES = {
    # Text Formats
    "application/rtf": {"gmt": GMT.TEXT, "ext": "rtf"},
    "application/msword": {"gmt": GMT.TEXT, "ext": "doc"},
    "application/pdf": {"gmt": GMT.TEXT, "ext": "pdf"},
    "application/epub+zip": {"gmt": GMT.TEXT, "ext": "epub"},
    "application/xml": {"gmt": GMT.TEXT, "ext": "xml"},
    "application/xhtml+xml": {"gmt": GMT.TEXT, "ext": "xhtml"},
    "application/vnd.oasis.opendocument.text": {"gmt": GMT.TEXT, "ext": "odt"},
    "text/html": {"gmt": GMT.TEXT, "ext": "html"},
    "text/plain": {"gmt": GMT.TEXT, "ext": "txt"},
    "application/x-ibooks+zip": {"gmt": GMT.TEXT, "ext": "ibooks"},
    "text/x-web-markdown": {"gmt": GMT.TEXT, "ext": "md"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "gmt": GMT.TEXT,
        "ext": "docx",
    },
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
        "gmt": GMT.TEXT,
        "ext": "xlsx",
    },
    "application/vnd.ms-excel": {"gmt": GMT.TEXT, "ext": "xls"},
    "application/x-mobipocket-ebook": {
        "gmt": GMT.TEXT,
        "ext": ["mobi", "prc", "azw", "azw3", "azw4"],
    },
    # Image Formats
    "image/bmp": {"gmt": GMT.IMAGE, "ext": "bmp"},
    "image/gif": {"gmt": GMT.IMAGE, "ext": "gif"},
    "image/jpeg": {"gmt": GMT.IMAGE, "ext": ["jpg", "jpeg"]},
    "image/png": {"gmt": GMT.IMAGE, "ext": "png"},
    "image/tiff": {"gmt": GMT.IMAGE, "ext": "tif"},
    "image/vnd.adobe.photoshop": {"gmt": GMT.IMAGE, "ext": "psd"},
    "application/postscript": {"gmt": GMT.IMAGE, "ext": "eps"},
    # Audio Formats
    "audio/mpeg": {"gmt": GMT.AUDIO, "ext": "mp3"},
    "audio/vnd.wave": {"gmt": GMT.AUDIO, "ext": "wav"},
    "audio/vorbis": {"gmt": GMT.AUDIO, "ext": "ogg"},
    "audio/x-aiff": {"gmt": GMT.AUDIO, "ext": "aif"},
    "audio/x-flac": {"gmt": GMT.AUDIO, "ext": "flac"},
    "audio/opus": {"gmt": GMT.AUDIO, "ext": "opus"},
    # Video Formats
    "application/vnd.rn-realmedia": {"gmt": GMT.VIDEO, "ext": "rm"},
    "video/x-dirac": {"gmt": GMT.VIDEO, "ext": "drc"},
    "video/3gpp": {"gmt": GMT.VIDEO, "ext": "3gp"},
    "video/3gpp2": {"gmt": GMT.VIDEO, "ext": "3g2"},
    "video/x-ms-asf": {"gmt": GMT.VIDEO, "ext": "asf"},
    "video/x-msvideo": {"gmt": GMT.VIDEO, "ext": "avi"},
    "video/webm": {"gmt": GMT.VIDEO, "ext": "webm"},
    "video/mpeg": {"gmt": GMT.VIDEO, "ext": ["mpeg", "mpg", "m1v", "vob"]},
    "video/mp4": {"gmt": GMT.VIDEO, "ext": "mp4"},
    "video/x-m4v": {"gmt": GMT.VIDEO, "ext": "m4v"},
    "video/x-matroska": {"gmt": GMT.VIDEO, "ext": "mkv"},
    "video/theora": {"gmt": GMT.VIDEO, "ext": ["ogg", "ogv"]},
    "video/quicktime": {"gmt": GMT.VIDEO, "ext": ["mov", "f4v"]},
    "video/x-flv": {"gmt": GMT.VIDEO, "ext": "flv"},
    "application/x-shockwave-flash": {"gmt": GMT.VIDEO, "ext": "swf"},
    "video/h264": {"gmt": GMT.VIDEO, "ext": "h264"},
    "video/x-ms-wmv": {"gmt": GMT.VIDEO, "ext": "wmv"},
}


SUPPORTED_EXTENSIONS = []
for v in SUPPORTED_MIME_TYPES.values():
    ext = v["ext"]
    if isinstance(ext, str):
        SUPPORTED_EXTENSIONS.append(ext)
    else:
        for e in ext:
            SUPPORTED_EXTENSIONS.append(e)


ISCC_COMPONENT_TYPES = {
    const.HEAD_MID: {"name": "Meta-ID", "code": "CC"},
    const.HEAD_CID_T: {"name": "Content-ID Text", "code": "CT"},
    const.HEAD_CID_T_PCF: {"name": "Content-ID Text", "code": "Ct"},
    const.HEAD_CID_I: {"name": "Content-ID Image", "code": "CY"},
    const.HEAD_CID_I_PCF: {"name": "Content-ID Image", "code": "Ci"},
    const.HEAD_CID_A: {"name": "Content-ID Audio", "code": "CA"},
    const.HEAD_CID_A_PCF: {"name": "Content-ID Audio", "code": "Ca"},
    const.HEAD_CID_V: {"name": "Content-ID Video", "code": "CV"},
    const.HEAD_CID_V_PCF: {"name": "Content-ID Video", "code": "Cv"},
    const.HEAD_CID_M: {"name": "Content-ID Mixed", "code": "CM"},
    const.HEAD_CID_M_PCF: {"name": "Content-ID Mixed", "code": "Cm"},
    const.HEAD_DID: {"name": "Data-ID", "code": "CD"},
    const.HEAD_IID: {"name": "Instance-ID", "code": "CR"},
}

ISCC_COMPONENT_CODES = {
    value["code"]: {"name": value["name"], "marker": key}
    for key, value in ISCC_COMPONENT_TYPES.items()
}

TEST_DATA_URL = "https://raw.githubusercontent.com/iscc/iscc-specs/master/tests/"

WTA_PERMUTATIONS = (
    (292, 16),
    (219, 247),
    (295, 7),
    (105, 236),
    (251, 142),
    (334, 82),
    (17, 266),
    (250, 167),
    (38, 127),
    (184, 22),
    (215, 71),
    (308, 181),
    (195, 215),
    (145, 345),
    (134, 233),
    (89, 351),
    (155, 338),
    (185, 68),
    (233, 122),
    (225, 314),
    (192, 22),
    (298, 2),
    (120, 68),
    (99, 155),
    (274, 187),
    (122, 160),
    (341, 281),
    (230, 223),
    (240, 33),
    (334, 299),
    (166, 256),
    (80, 114),
    (211, 122),
    (18, 16),
    (254, 154),
    (310, 336),
    (36, 273),
    (41, 76),
    (196, 290),
    (191, 307),
    (76, 57),
    (49, 226),
    (85, 97),
    (178, 221),
    (212, 228),
    (125, 348),
    (140, 73),
    (316, 267),
    (91, 61),
    (136, 233),
    (154, 84),
    (338, 332),
    (89, 90),
    (245, 177),
    (167, 222),
    (114, 2),
    (278, 364),
    (22, 169),
    (163, 124),
    (40, 134),
    (229, 207),
    (298, 81),
    (199, 253),
    (344, 123),
    (376, 268),
    (139, 266),
    (247, 308),
    (255, 32),
    (85, 250),
    (345, 236),
    (205, 69),
    (215, 277),
    (299, 178),
    (275, 198),
    (250, 359),
    (84, 286),
    (225, 50),
    (212, 18),
    (1, 224),
    (274, 33),
    (25, 179),
    (47, 77),
    (55, 311),
    (232, 248),
    (71, 234),
    (223, 256),
    (228, 175),
    (371, 132),
    (357, 234),
    (216, 168),
    (332, 266),
    (267, 78),
    (378, 121),
    (165, 316),
    (16, 351),
    (100, 329),
    (301, 294),
    (321, 245),
    (12, 59),
    (151, 222),
    (126, 367),
    (148, 45),
    (23, 305),
    (281, 54),
    (146, 83),
    (343, 244),
    (72, 184),
    (304, 205),
    (98, 179),
    (93, 40),
    (302, 99),
    (218, 106),
    (49, 350),
    (157, 237),
    (355, 267),
    (369, 216),
    (229, 340),
    (284, 106),
    (136, 305),
    (186, 59),
    (3, 107),
    (217, 312),
    (209, 195),
    (333, 102),
    (35, 216),
    (45, 28),
    (178, 130),
    (184, 233),
    (217, 99),
    (321, 144),
    (238, 355),
    (150, 259),
    (255, 259),
    (134, 207),
    (226, 327),
    (174, 178),
    (371, 141),
    (247, 228),
    (244, 300),
    (245, 42),
    (353, 276),
    (368, 187),
    (369, 207),
    (86, 308),
    (212, 368),
    (288, 33),
    (304, 375),
    (156, 8),
    (302, 167),
    (333, 164),
    (37, 379),
    (203, 312),
    (191, 144),
    (310, 95),
    (123, 86),
    (157, 48),
    (284, 27),
    (112, 291),
    (37, 215),
    (98, 291),
    (292, 224),
    (303, 8),
    (200, 103),
    (173, 294),
    (97, 267),
    (288, 167),
    (24, 336),
    (354, 296),
    (25, 18),
    (289, 187),
    (203, 166),
    (307, 326),
    (87, 80),
    (60, 310),
    (176, 84),
    (15, 370),
    (274, 261),
    (178, 45),
    (203, 224),
    (295, 178),
    (30, 74),
    (227, 361),
    (241, 312),
    (231, 369),
    (226, 309),
    (89, 181),
    (216, 175),
    (286, 262),
    (234, 198),
    (99, 49),
    (221, 328),
    (78, 21),
    (95, 327),
    (324, 97),
    (291, 219),
    (184, 286),
    (192, 25),
    (309, 26),
    (84, 159),
    (114, 25),
    (296, 90),
    (51, 325),
    (289, 184),
    (95, 154),
    (21, 202),
    (306, 219),
    (39, 176),
    (99, 251),
    (83, 86),
    (207, 239),
    (168, 19),
    (88, 90),
    (297, 361),
    (215, 78),
    (262, 328),
    (356, 200),
    (48, 203),
    (60, 120),
    (54, 216),
    (369, 327),
    (159, 370),
    (148, 273),
    (332, 50),
    (176, 267),
    (317, 243),
    (311, 125),
    (272, 148),
    (6, 340),
    (80, 346),
    (197, 355),
    (117, 49),
    (261, 326),
    (242, 51),
    (295, 204),
    (298, 111),
    (147, 181),
    (35, 96),
    (318, 285),
    (271, 13),
    (38, 204),
    (16, 8),
    (334, 220),
    (173, 91),
    (372, 24),
    (183, 166),
    (320, 243),
    (87, 9),
    (105, 65),
    (148, 103),
    (197, 314),
    (279, 299),
    (304, 214),
    (282, 15),
    (64, 2),
    (63, 14),
    (28, 351),
)
