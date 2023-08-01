 <pre>

                         ████████╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
                         ╚══██╔══╝██╔═══██╗██╔══██╗    ██╔══██╗██╔═████╗╚══██╔══╝
                            ██║   ██║   ██║██████╔╝    ██████╔╝██║██╔██║   ██║
                            ██║   ██║   ██║██╔══██╗    ██╔══██╗████╔╝██║   ██║
                            ██║   ╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝   ██║
                            ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝

                            Open Source Intelligence Tool for the Dark Web

</pre>

<p align="center">
   <img src="https://user-images.githubusercontent.com/4481429/191882921-527cb8e0-91ad-4f3f-bc26-9df533857133.png" width="250" title="Hacktoberfest 2022">
    <img src="https://user-images.githubusercontent.com/4481429/94646312-9dafcd80-030b-11eb-9824-73aa2414cf58.png" width="160" title="OpenSource">
  <img src="https://user-images.githubusercontent.com/4481429/94645022-65f35680-0308-11eb-8dce-a4ceba8db660.png" width="270" title="OWASP Foundation">
</p>


### Status/Social links
[![Flake8](https://github.com/DedSecInside/TorBot/actions/workflows/flake8.yml/badge.svg)](https://github.com/DedSecInside/TorBot/actions/workflows/flake8.yml)
[![Slack Invite](https://img.shields.io/badge/Join-Slack-informational?style=flat-square&logo=slack)](https://join.slack.com/t/dedsec-inside/shared_invite/zt-i4jcgj8w-1ecHiSdRubwuppAzz8~yfg)
[![Code Triage](https://www.codetriage.com/dedsecinside/torbot/badges/users.svg)](https://www.codetriage.com/dedsecinside/torbot)
[![](https://img.shields.io/badge/Built%20with-❤-orange.svg?style=flat-square)]()
[![](https://img.shields.io/badge/Made%20with-Python-red.svg?style=flat-square)]()

### Features
1. Onion Crawler (.onion)
2. Returns Page title and address with a short description about the site
3. Save links to database
4. Get data from site
5. Save crawl info to JSON file
6. Crawl custom domains
7. Check if the link is live
8. Built-in Updater
9. Build visual tree of link relationship that can be quickly viewed or saved to an image file

...(will be updated)

### Dependencies
- Tor
- Python ^3.8
- Golang 1.19
- Poetry

### Python Dependencies

(see requirements.txt for more details)

### Golang Dependencies
- https://github.com/KingAkeem/gotor (This service needs to be ran in tandem with TorBot)

## Installation

### From source
Before you run the torBot make sure the following things are done properly:

* Run the tor service:
```sh
sudo service tor start
```
* Make sure that your torrc is configured to SOCKS_PORT localhost:9050

* Open a new terminal and run:
```sh
cd gotor && go run cmd/main/main.go -server
```

* Install TorBot Python requirements using poetry

```sh
poetry install # to install dependencies
poetry run python run.py -u https://www.example.com --depth 2 -v # example of running command with poetry
poetry run python run.py -h # for help
```

<pre>
usage: Gather and analayze data from Tor sites.

optional arguments:
  -h, --help            show this help message and exit
  --version             Show current version of TorBot.
  --update              Update TorBot to the latest stable version
  -q, --quiet
  -u URL, --url URL     Specifiy a website link to crawl
  -s, --save            Save results in a file
  -m, --mail            Get e-mail addresses from the crawled sites
  -p, --phone           Get phone numbers from the crawled sites
  --depth DEPTH         Specifiy max depth of crawler (default 1)
  --gather              Gather data for analysis
  -v, --visualize       Visualizes tree of data gathered.
  -d, --download        Downloads tree of data gathered.
  -e EXTENSION, --extension EXTENSION
                        Specifiy additional website extensions to the list(.com , .org, .etc)
  -c, --classify        Classify the webpage using NLP module
  -cAll, --classifyAll  Classify all the obtained webpages using NLP module
  -i, --info            Info displays basic info of the scanned site` </pre>

* NOTE: -u is a mandatory for crawling

Read more about torrc here : [Torrc](https://github.com/DedSecInside/TorBoT/blob/master/Tor.md)

### Using Docker

- Ensure than you have a tor container running on port 9050.
- Build the image using following command (in the root directory):

    `docker build -f docker/Dockerfile -t dedsecinside/torbot .`
- Run the container (make sure to link the tor container as `tor`):

    `docker run --link tor:tor --rm -ti dedsecinside/torbot`

### Using executable (Linux Only)

On Linux platforms, you can make an executable for TorBot by using the install.sh script.
You will need to give the script the correct permissions using `chmod +x install.sh`
Now you can run `./install.sh` to create the torBot binary.
Run `./torBot` to execute the program.


## Curated Features
- [x] Visualization Module Revamp
- [x] Implement BFS Search for webcrawler
- [x] Use Golang service for concurrent webcrawling
- [x] Improve stability (Handle errors gracefully, expand test coverage and etc.)
- [ ] Randomize Tor Connection (Random Header and Identity)
- [ ] Keyword/Phrase search
- [ ] Social Media Integration
- [ ] Increase anonymity
- [x] Improve performance (Done with gotor)
- [ ] Screenshot capture


## Contribution Guidelines

### Found an issue?

If you face any issues in the project, please let us know by creating a new issue [here](https://github.com/DedSecInside/TorBot/issues/new/choose).

### Developer Guidelines

We welcome contributions to this project! Here are a few guidelines to follow:

1. Fork the repository and create a new branch for your contribution.
2. Make sure your code passes all tests by running `pytest` before submitting a pull request to `dev` branch.
3. Follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
4. Make sure to add appropriate documentation for any new features or changes.
5. When submitting a pull request, please provide a detailed description of the changes made.

## References

    1.  M. Glassman and M. J. Kang, “Intelligence in the internet age: The emergence and evolution of Open Source Intelligence (OSINT),” Comput. Human Behav., vol. 28, no. 2, pp. 673–682, 2012.
    2.  D. Bradbury, “In plain view: open source intelligence,” Comput. Fraud Secur., vol. 2011, no. 4, pp. 5–9, 2011.
    3.  B. Butler, B. Wardman, and N. Pratt, “REAPER: an automated, scalable solution for mass credential harvesting and OSINT,” 2016 APWG Symp. Electron. Crime Res., pp. 1–10, 2016.
    4.  B. Zantout and R. A. Haraty, “I2P Data Communication System I2P Data Communication System,” no. April 2002, 2014.
    5.  J. Qin, Y. Zhou, G. Lai, E. Reid, M. Sageman, and H. Chen, “The dark web portal project: collecting and analyzing the presence of terrorist groups on the web,” in Proceedings of the 2005 IEEE international conference on Intelligence and Security Informatics, 2005, pp. 623–624.
    6.  D. Moore, T. Rid, D. Moore, and T. Rid, “Cryptopolitik and the Darknet Cryptopolitik and the Darknet,” vol. 6338, 2016.
    7.  G. Weimann, “Going dark: Terrorism on the dark Web,” Stud. Confl. Terror., vol. 39, no. 3, pp. 195–206, 2016.
    8.  A. T. Zulkarnine, R. Frank, B. Monk, J. Mitchell, and G. Davies, “Surfacing collaborated networks in dark web to find illicit and criminal content,” in Intelligence and Security Informatics (ISI), 2016 IEEE Conference on, 2016, pp. 109–114.
    9.  T. Minárik and A.-M. Osula, “Tor does not stink: Use and abuse of the Tor anonymity network from the perspective of law,” Comput. Law Secur. Rev., vol. 32, no. 1, pp. 111–127, 2016.
    10. K. Loesing, S. J. Murdoch, and R. Dingledine, “A Case Study on Measuring Statistical Data in the {T}or Anonymity Network,” in Proceedings of the Workshop on Ethics in Computer Security Research (WECSR 2010), 2010.
    11. B. Nafziger, “Data Mining in the Dark : Darknet Intelligence Automation,” 2017.
    12. I. Sanchez-Rola, D. Balzarotti, and I. Santos, “The onions have eyes: A comprehensive structure and privacy analysis of tor hidden services,” in Proceedings of the 26th International Conference on World Wide Web, 2017, pp. 1251–1260.
    13. Mouli VR, Jevitha KP. “Web Services Attacks and Security-A Systematic Literature Review.”, Procedia Computer Science. 2016 Jan 1;93:870-7.
    14. Cova M, Felmetsger V, Vigna G. "Vulnerability analysis of web-based applications. InTest and Analysis of Web Services" 2007 (pp. 363-394). Springer, Berlin, Heidelberg.
    15. B. R. Holland, “Enabling Open Source Intelligence (OSINT) in private social networks,” 2012.
    16. S. Nakamoto, “Bitcoin: A Peer-to-Peer Electronic Cash System,” Cryptogr. Mail. List https//metzdowd.com, 2009.
    17. M. Wesam, A. Nabki, E. Fidalgo, E. Alegre, and I. De Paz, “Classifying Illegal Activities on Tor Network Based on Web Textual Contents”, vol. 1, pp. 35–43, 2017.
    18. Sathyadevan S, Gangadharan S.“Crime analysis and prediction using data mining”. In Networks & Soft Computing (ICNSC), 2014 First International Conference on 2014 Aug 19 (pp. 406-412). IEEE.
    19. Chau M, Chen H. "A machine learning approach to web page filtering using content and structure analysis. Decision Support Systems." 2008 Jan 1;44(2):482-94.
    20. Ani R, Jose J, Wilson M, Deepa OS. “Modified Rotation Forest Ensemble Classifier for Medical Diagnosis in Decision Support Systems”, In Progress in Advanced Computing and Intelligent Engineering 2018 (pp. 137-146). Springer, Singapore.
    21. Ani R, Augustine A, Akhil N.C. and Deepa O.S., 2016. “Random Forest Ensemble Classifier to Predict the Coronary Heart Disease Using Risk Factors”, In Proceedings of the International Conference on Soft Computing Systems (pp. 701-710). Springer, New Delhi.


## Maintainers

- [X] [PS Narayanan](https://github.com/PSNAppz) - Co-owner
- [X] [KingAkeem](https://github.com/KingAkeem) - Co-owner

... see all [contributors](https://github.com/DedSecInside/TorBot/graphs/contributors)

## License
[GNU Public License](https://github.com/DedSecInside/TorBot/blob/dev/LICENSE.md)
