id_to_name =    [
                "",
                "jumper",       "explorer",     "prospector",   "pioneer",      "space digger",
                "drone",        "pathfinder",   "vanguard",     "handshaker",   "senator",
                "sunriser",
                "auditor",      "comptroller",  "enforcer",     "chancelor",
                "petrack",
                "nomad",        "netrunner",    "highrider",    "apogee",
                "journey",      "demons",       "spirits",      "kingdoms",
                "fren",         "monocle",      "curve",        "ghost",
                "pickle",       "slice",        "sandwich",     "mason jar",
                "anakuma",      "mellivora",    "leucurus",     "capensis",
                "croissant",    "friendmaker",  "space crab",   "liberator",
                "arbitrator",   "pinakion",     "justitia",     "truthstar",
                "konpeito",    "ramune",       "anpan",        "higashi",
                "gorgo",        "gemini",       "consul",
                "detos",        "foresight",    "annuare",      "mot",
                "apex",         "doggo",        "graff",        "mastodon",
                "le france",
                "alata",        "trifida",        "rotunda",
                "shit5",        "shit6",        "shit7",        "shit8",
                "shit9",        "shit10",       "shit11",       "shit12"
                ]


def id_to_str(id):
    if id >= 1000000000:
        return "mule"
    id = int(id / 1000000)
    return id_to_name[id]

def getId(name, number):
    name = name.lower()
    if name == "mule":
         return 1000000000 + number - 1
    else:
        name_n = {x:i for i, x in enumerate(id_to_name)}
    return name_n[name] * 1000000 + number - 1
