
def parse(file_path):
    f = open(file_path, "r")
    rows = f.read().split('\n')
    sites = []
    label = []
    for row in rows:
        value = row.split('\t')
        sites.append(value[0])
        label.append(value[1])
    return sites,label
