import os

from config import transmission_auth


def get_torrent_status():
    out = os.popen("transmission-remote -n " + transmission_auth + " -l").read()

    torrent_list = out.split("\n")[1:-2]
    data = []
    for t in torrent_list:
        t = t.split()
        error = False
        if t[0].endswith("*"):
            t[0] = t[0][:-1]
            error = True
        t_id = int(t[0])
        out2 = os.popen("transmission-remote -n " + transmission_auth + " -t " + str(t_id) + " -i").read()
        torrent_data = out2.split("\n")
        torrent_data = [d.split(":", 1) for d in torrent_data]
        data.append({"name": torrent_data[2][1].strip(), "status": torrent_data[7][1].strip(),
                     "perc": torrent_data[9][1].strip(), "eta": torrent_data[10][1].strip(),
                     "dws": torrent_data[11][1].strip(), "ups": torrent_data[12][1].strip(), "error": error})
    return data


def add_torrent(magnet):
    out = os.popen("transmission-remote -n " + transmission_auth + " -a " + magnet).read()
    if out.startswith("Error"):
        return -1
    return 1
