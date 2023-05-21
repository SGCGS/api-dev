def rdoc(path):
    with open(path, "r", encoding="utf-8") as f:
        doc = f.read()
    return doc
