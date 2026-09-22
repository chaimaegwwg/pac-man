import json

MANDATORY_KEYS = (
    "highscore_filename", "lives", "points_per_pacgum", 
    "points_per_super_pacgum", "points_per_ghost"
)
OPTIONAL_KEYS = ("level_max_time")

def read_file_without_cmts(file_name):
    lines = []

    with open(file_name) as f:
        for line in f:
            if line.strip().startswith('#') or line.strip().startswith('//'):
                continue
            lines.append(line)

        return "".join(lines)

def check_key_exesting(js_content):
    entred_keys = set()
    for key in js_content:
        
        if key in OPTIONAL_KEYS:
            continue
        elif key not in MANDATORY_KEYS:
            raise ValueError(
                f"{key} not allowed please make sure to enter just allowed keys"
                )
        entred_keys.add(key)
    if len(entred_keys) != len(MANDATORY_KEYS) and len(entred_keys) != 6:
        raise ValueError(
            'make sure to enter all mandatory keys: "highscore_filename", "lives", "points_per_pacgum",'
            '"points_per_super_pacgum", "points_per_ghost"')


def check_highscore_filename(highscore_filename):
    if not isinstance(highscore_filename, str):
        raise ValueError("the highscore_filename should be a string with .txt extension")
    if not highscore_filename.endswith('.txt'):
        raise ValueError("the highscore_filename should be text file (.txt)")


def check_lives(lives):
    if not isinstance(lives, int):
        raise ValueError("lives must be integer")
    # lives = int(lives)
    if lives > 5 or lives < 1:
        raise ValueError("lives must be between 1 and 5")



content = read_file_without_cmts("config/config.json")
# convert the json data to a dict
js_content = json.loads(content)

check_key_exesting(js_content)
check_highscore_filename(js_content["highscore_filename"])
check_lives(js_content["lives"])
print(js_content)
