import os
import salt.client

def remove_stale(time, update=False):
    """
    Remove stale mine data.

    CLI Example:

    .. code-block:: bash

        salt-run mine.remove_stale '90 sec'
        salt-run mine.remove_stale '3 min'
        salt-run mine.remove_stale '10 sec' update=True
    """
    try:
        n_time, t_time = time.split()
        n_time = int(n_time)
        assert t_time in ['sec', 'min']
    except Exception as e:
        raise ValueError("Invalid time given: {}".format(time))

    # Remove stale mine data
    refresh_command = \
        ("find /var/cache/salt/master/minions/ "
         "-type f -name mine.p ! -newermt '-" + str(n_time) + " " + t_time +"' "
         "-exec bash '-c' 'rm {}' ';'")

    os.system(refresh_command)

    if update is True:
        # Update mine data
        client = salt.client.LocalClient(__opts__['conf_file'])
        client.cmd('*', 'mine.update')