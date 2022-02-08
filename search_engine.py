import master_duel_auto_scan_version as mda
from threading import Thread


def start():
    """method to start searching
    """
    scan_card = Thread(target=mda.main)
    scan_card.start()


def kill():
    """method to exit searching
    """
    mda.status_change(False, False, True)


def pause():
    """method to pause searching
    """
    mda.status_change(False, True, False)


def unpause():
    """method to unpause searching
    """
    mda.status_change(False, False, False)


def switch_mode():
    """method to switch between deck / duel searching
    """
    mda.status_change(True, False, False)

# more methodes can be added to fit database search result


def get_card_No():
    """method to get card code
    """
    if mda.g_card_show:
        return mda.g_card_show["card"]
    else:
        return None


def get_card_name():
    """method to get card name
    """
    if mda.g_card_show:
        return mda.g_card_show["name"]
    else:
        return None


def get_card_desc():
    """method to get card description
    """
    if mda.g_card_show:
        return mda.g_card_show["desc"]
    else:
        return None
