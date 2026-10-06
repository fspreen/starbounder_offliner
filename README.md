# StarbounderOffliner
This is a tool for making an offline OpenZIM file from the [Starbounder
wiki](https://starbounder.org) which is the wiki for the 2016 computer
game _Starbound_.

This tool is written in Python and is modeled after the
[mwoffliner](https://github.com/openzim/mwoffliner) tool for general
MediaWiki capture.

## Installation
Copy the Git repository:
```
git clone https://github.com/fspreen/starbounder_offliner
cd starbounder_offliner
```

Create a Python virtual environment:
```
virtualenv -p python3 venv
```

Activate the virtual environment and install dependencies:
```
source venv/bin/activate
pip install -r requirements.txt
```

Run the software:
```
python cli.py --adminEmail YOUR_EMAIL
```

## Why a separate tool?
The [mwoffliner](https://github.com/openzim/mwoffliner) tool is good for
creating offline copies of wikis built on MediaWiki software.  But it
only supports MediaWiki version 1.27 or newer.  The Starbounder wiki
uses version 1.26.2 so it is not supported by `mwoffliner`.  This tool
fills that gap.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0) or later, see
[LICENSE](LICENSE) for more details.
