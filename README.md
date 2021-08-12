# 🔮 Twitter Wizardry

> Track your Twitter progress right in your profile image!

![example](example_img.png)

The app (once deployed) automatically updates your Twitter profile image as your followers change to reflect your Twitter progress with a progress bar!

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy)

# Setup

## Installing Requirements
After creating a virtual environment and activating it, simply run:
```
pip install -r requirements.txt
```

## Loading secret keys
All secret keys are to be loaded as environment variables.

If using on a local machine, you can place the keys inside a `.env` file in the project's directory. Example:
```
DETA_PROJECT_KEY=DDDDD
TWITTER_KEY=AAAAAA
TWITTER_SECRET=BBBB
ACCESS_TOKEN=CCCCC
ACCESS_TOKEN_SECRET=CCCCC
```

### Customization
Edit the `config.py` file according to your liking.
