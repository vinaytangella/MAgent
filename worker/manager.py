import cotyledon
from app.Worker import MetricsWorker

class Manager(cotyledon.ServiceManager):
    def __init__(self):
        super().__init__()
        self.add(MetricsWorker,workers=1)

if __name__ == '__main__':
    Manager().run()