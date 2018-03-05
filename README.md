# Injection Scoring Engine
### Sumamry
A python3 program used to test various service's uptime for a given network infrastructure. The ISE is made to be modular with only the JSON files needing to be configured.

### Setup
1. Git clone this repository:
- `git clone https://github.com/SilexOne/ise.git`
2. Run the install script:
- `./ise_setup.sh`
3. Configure the JSON files to your network:
- The `main.json` chooses if your testing or actually scoring your services and enables which ones you want to use. 
- The `services/score_dns.json` is the settings you are scoring for Domain Name Server.
- The `services/score_ad.json` is the settings you are scoring for Active Directory.
- The `services/score_http.json` is the settings you are scoring for the website.
- The `services/score_https.json` is the settings you are scoring for the website.
- The `services/score_ftp.json` is the settings you are scoring for the File Transfer server.
- The `services/score_email.json` is the settings you are scoring for the email server.
4. Run the program:
- `python main.py`
5. View the website:
- Browse to the machine that is hosting the ISE `http://#.#.#.#`.