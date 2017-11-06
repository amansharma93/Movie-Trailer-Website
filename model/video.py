class Video():
    def __init__(self, id, key, name, site, type):
        self.id = id
        self.key = key
        self.name = name
        self.site = site
        self.type = type
        self.link = '//www.youtube.com/embed/' + self.key + '?autoplay=1'
