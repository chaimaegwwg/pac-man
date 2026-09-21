import json

def read_file_without_cmts(file_name):
    lines = []

    with open(file_name) as f:
        for line in f:
            if line.strip().startswith('#'):
                continue
            lines.append(line)

        return "".join(lines)


content = read_file_without_cmts("config/config.json")
js_content = json.loads(content)

print(js_content)

