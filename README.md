Buildbot Configuration
======================

BuildBot Configuration Files for the QLC+ build master. If you expected to find
passwords here you'll be disappointed (as they're stored on the build master in
<build slave name>.pass files and excluded from the repo via .gitignore).

See https://wiki.openlighting.org/index.php/OLA_Buildbot for instructions on
setting up a buildslave, then adapt the packages to suit QLC+.

There is a cronscript that runs on the server (update.sh) which pulls from the
git repo and reloads the build master. Any changes submitted should go live in
5 minutes.
