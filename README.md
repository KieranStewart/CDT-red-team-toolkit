# CDT-red-team-toolkit

A red team toolkit for CSEC 473 Cyber Defense Techniques.
These tools were developed solely for use in **authorized Red Team competitions, penetration testing engagements, and security research** conducted under explicit permission from all relevant parties. Any use outside of this scope should be conducted with user disgression and following ethical and legal practices. The creator of this tool accepts no responsibility for how any of these tools are used outside of its intended context. Any harm, legal liability, or ethical violations arising from unauthorized or irresponsible use are the sole responsibility of the individual using the tools.

## Bosh

Bosh is a modified variant of gnu bash which reports all of the commands run in it to a central server. To install bosh on a target run *install.sh* from the gnu_bosh folder. Additionally you can pass a username (defaults to admin) and a password (defaults to prompting the user) in the following format.
```bash
REMOTE_USER=<username> REMOTE_PASS=<password> ./install.sh
```
The remote user you are authenticating to must have sudo permissions and be a valid ssh user.

<sub>bingo bango bongo bish bash bosh</sub>
