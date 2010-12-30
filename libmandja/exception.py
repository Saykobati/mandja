class mandjaGeneralError(StandardError):
    pass

class mandjaCrawlerError(mandjaGeneralError):
    pass

class mandjaCrawlerURLError(mandjaCrawlerError):
    pass

class mandjaCrawlerContentError(mandjaCrawlerError):
    pass