# TorScape

<p align="center">
    <img src="https://cdn.discordapp.com/attachments/884182157415817247/899809795773698118/Tor__anonymity_network_-Logo.wine-removebg-preview.png" width="320">
</p>


TorScrape is a small but useful script made in python that wills scrape a website for active tor nodes, parse the html and then save the nodes in the correct format so that they can be used as proxies in other programs.

## Installation
Make sure [python](https://www.python.org/) is installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requests and BeautifulSoup.

```bash
pip3 install requests bs4
```

## Usage

```python
python3 main.py
```
It is important to note that the website it uses can only be scraped every 30 minutes so do not run this script unless the 30 minutes has passed.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)