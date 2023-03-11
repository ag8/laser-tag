def s(vertices, scale):
    scaled = []

    for p in vertices:
        scaled.append((p[0] * scale, p[1] * scale))

    return scaled
