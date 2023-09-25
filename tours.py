import config


def parse_trevel(file: str) -> []:
    with open(file, mode="r", encoding="utf-8") as f:
        text = f.read()
    tours = text.split("#")
    ret = []
    for t in tours:
        try:
            if not t:
                continue
            t = t.replace("\n", "")
            x = t.split("[X]")
            ret.append(Tour(tour_id=x[0], head=x[1],body=x[2],url=x[3]))
        except Exception as e: 
            print(e)
    return ret
        

class Tour:
    def __init__(self, tour_id: str, head: str, body: str, url: str) -> None:
        self.id = tour_id
        self.head = head
        self.body = body
        self.url = url

def get_tour_by_id(tour_id: str) -> Tour:
    tours = parse_trevel(config.BUS)
    ret = next((x for x in tours if x.id == tour_id), None)
    if not ret: 
        tours = parse_trevel(config.HIKING)
        ret = next((x for x in tours if x.id == tour_id), None)
    if not ret: 
        tours = parse_trevel(config.TOURS)
        ret = next((x for x in tours if x.id == tour_id), None)

    return ret
        
def get_bus():
    return parse_trevel(config.BUS)

def get_hike():
    return parse_trevel(config.HIKING)

def get_tours():
    return parse_trevel(config.TOURS)

        