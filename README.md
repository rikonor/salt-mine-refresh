### Salt runner / **mine.remove_stale**

mine.remove_salt is a Salt runner for cleaning out stale mine data.

#### Installation

To use this runner put the mine.py in the designated runners directory.
Alternatively, copy mine.py to salt://_runners/mine.py and set salt://_runners as an additional runners directory in the salt master config file.

```bash
runner_dirs: ["/srv/salt/_runners"]
```

#### Usage

```bash
salt-run mine.remove_stale '90 sec'
salt-run mine.remove_stale '5 min'

# set Update=True to trigger a mine.update 
salt-run mine.remove_stale '10 sec' update=True
```

#### Example in Reactor

You can call the runner in response to an event.

```yaml
refresh_mine_data:
  runner.mine.remove_stale:
    - time: '90 sec'
    - update: True # optional 

```

Now schedule an event to be emitted every minute or so, and stale mine data will be automatically removed.

#### Motivation

```bash
# Preliminary: Minions report their IP to the salt mine every minute. 
# I'd like to retrieve the private_ip of all minions
$ sudo salt 'minion_1' mine.get '*' private_ip expr_form=grain
minion_1:
    ----------
    minion_1:
        4.8.15.16
    minion_2:
        23.42.0.0

# Notice: minion_2 is actually dead.
# Let's clean the stale data.
$ sudo salt-run mine.remove_stale '90 sec'
$ sudo salt 'minion_1' mine.get '*' private_ip expr_form=grain
minion_1:
    ----------
    minion_1:
        4.8.15.16
``` 