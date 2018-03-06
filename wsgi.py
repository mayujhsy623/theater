
from theater import create_app
from theater.configs.production import ProductionConfig


application = create_app(config=ProductionConfig)