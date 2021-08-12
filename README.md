## Twitter Wizardry
A Python recreation of a popular tool [blackmagic.so](https://blackmagic.so) created by [Tony Dinh](https://github.com/trungdq88).

The app (once deployed) automatically updates your Twitter profile image as your Followers change to reflect your Twitter progress with a progress bar.

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy)

## Example Image
![example](example.png)

## Setup

### Installing Requirements
After creating a virtual environment and activating it, simply run:
```
pip install -r requirements.txt
```

### Loading secret keys
The script looks for them in environment variables.

If using on a local machine, place the keys inside a `.env` file in the project's directory and you should be good to go. Example:
```
DETA_PROJECT_KEY=DDDDD
TWITTER_KEY=AAAAAA
TWITTER_SECRET=BBBB
ACCESS_TOKEN=CCCCC
ACCESS_TOKEN_SECRET=CCCCC
```

### Customization
Edit the `config.py` file according to your liking.
