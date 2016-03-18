import subprocess
import salt.client

def _parse_time(time):
    """
    Parse a time string according to the following format
    'N sec/min'
    """
    try:
        n_time, t_time = time.split()
        n_time = int(n_time)
        assert t_time in ['sec', 'min']
        return n_time, t_time
    except Exception as e:
        raise ValueError("Invalid time given: {}".format(time))

def participants(time):
    """
    Get minions that participated in mine
    between now and given time.

    CLI Example:

    .. code-block:: bash

        salt-run mine.participants '90 sec'
    """
    n_time, t_time = _parse_time(time)

    get_participants_command = [
        "find", "/var/cache/salt/master/minions/",
        "-type", "f", "-name", "mine.p", "!",
        "-newermt", "-{} {}".format(n_time, t_time)
    ]
    output = subprocess.check_output(get_participants_command)
    return [m.split("/")[-2] for m in output.split("\n")[:-1]]

def remove_stale(time, update=False, alert=True):
    """
    Remove stale mine data.

    CLI Example:

    .. code-block:: bash

        salt-run mine.remove_stale '90 sec'
        salt-run mine.remove_stale '3 min'
        salt-run mine.remove_stale '10 sec' update=True
    """
    n_time, t_time = _parse_time(time)

    if alert is True:
        pre_removal_minions = participants(time)

    # Remove stale mine data
    remove_stale_command = [
        "find", "/var/cache/salt/master/minions/",
        "-type", "f", "-name", "data.p", "!",
        "-newermt", "-{} {}".format(n_time, t_time),
        "-printf", "%h",
        "-exec", "bash", "-c", "rm {}", ";"
    ]

    subprocess.call(remove_stale_command)

    if alert is True:
        caller = salt.client.Caller()
        post_removal_minions = participants(time)
        for minion_id in pre_removal_minions:
            if minion_id not in post_removal_minions:
                caller.sminion.functions['event.send'](
                    'mine.minion.removed',
                    {
                        'id': minion_id
                    }
                )

    if update is True:
        # Update mine data
        client = salt.client.LocalClient(__opts__['conf_file'])
        client.cmd('*', 'mine.update')
