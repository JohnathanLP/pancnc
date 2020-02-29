class PanJob:
    filename = None

    raw_image = None
    raw_pixels = None

    parsed_image = None
    parsed_pixels = None

    def rawWide(self):
        if self.raw_image != None:
            return self.raw_image.size[0]
        else:
            return None

    def rawHigh(self):
        if self.raw_image != None:
            return self.raw_image.size[1]
        else:
            return None
    
    def rawMode(self):
        if self.raw_image != None:
            return self.raw_image.mode
        else:
            return None

    def cleanup(self):
        if self.raw_image != None:
            self.raw_image.close()
        if self.parsed_image != None:
            self.parsed_image.close()