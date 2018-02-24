# ssh workflow for Alfred

A workflow for [Alfred](http://www.alfredapp.com/) Powerpack users to rapidly open Secure SHell (ssh) sessions with smart hostname autocompletion based on the contents of `~/.ssh/known_hosts`, `~/.ssh/config`, `/etc/hosts` and (optionally) Bonjour.

![Example 1](https://raw.github.com/isometry/alfredworkflows/master/screenshots/ssh_local.png)

![Example 2](https://raw.github.com/isometry/alfredworkflows/master/screenshots/ssh_user@local.png)

## Releases

- [v1.3 for Alfred 2.4+](https://github.com/isometry/alfred-ssh/releases/tag/v1.3)
- [v2.x for Alfred 3.1+](https://github.com/isometry/alfred-ssh/releases/latest)

## Prerequisites

- [Alfred](http://www.alfredapp.com/) (version 2.4+/3.1+)
- The [Alfred Powerpack](http://www.alfredapp.com/powerpack/).
- (optional) [pybonjour](https://pypi.python.org/pypi/pybonjour)

## Usage

Type `ssh` in Alfred followed by either a literal hostname or by some letters from the hostname of a host referenced in any of `~/.ssh/known_hosts`, `~/.ssh/config`, `/etc/hosts`, or (with `pybonjour` installed) Bonjour.

Alfred 3 only: workflow configuration is available by setting/changing Workflow Environment Variables (accessed via the [𝓍] button within the workflow):

- disable unwanted sources by setting the associated Workflow Environment Variable to 0; e.g. `alfredssh_known_hosts`, `alfredssh_ssh_config`, `alfredssh_hosts`, `alfredssh_bonjour`.
- change the maximum number of returned results by changing `alfredssh_max_results` (default=36).
- add additional files listing valid host completions (e.g. for pre-seeding) by adding space-separated short-name=~/file/path entries to the `alfredssh_extra_files` Workflow Environment Variable. Lines beginning with `#` are ignored, all other whitespace separated words are assumed to be valid hostnames.

If you wish to have [iTerm2](https://www.iterm2.com/) act as ssh protocol handler rather than Terminal.app, create a new iTerm2 profile with “Name” `$$USER$$@$$HOST$$`, “Command” `$$` and “Schemes handled” `ssh` (e.g. [here](http://apple.stackexchange.com/questions/28938/set-iterm2-as-the-ssh-url-handler) and [here](http://www.alfredforum.com/topic/826-ssh-with-smart-hostname-autocompletion/#entry4147)).

## Contributions & Thanks

- [nikipore](https://github.com/nikipore)
