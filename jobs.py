from adapters.amsterdam import parking, stops
from adapters.ipo import environmental_zones


def run_jobs():
    """
    Run the adapters to get data from remote sources.
    """
    parking.run()
    stops.run()
    environmental_zones.run()


if __name__ == "__main__":
    """
    Placeholder so the jobs script can also be ran from a command line, for cronjobs
    """
    run_jobs()    
