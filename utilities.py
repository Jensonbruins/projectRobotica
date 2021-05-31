from PathFolower import wiel


def setup_wielen():
    wiel1 = wiel.Wiel()
    wiel1.set_wiel("lv")
    wiel2 = wiel.Wiel()
    wiel2.set_wiel("la")
    wiel3 = wiel.Wiel()
    wiel3.set_wiel("rv")
    wiel4 = wiel.Wiel()
    wiel4.set_wiel("ra")
    wielen = [wiel1, wiel2, wiel3, wiel4]

    return wielen