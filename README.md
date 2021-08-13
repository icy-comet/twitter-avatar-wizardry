# 🔮 Twitter Wizardry

> Track your Twitter progress right in your profile image!

![example](example_img.png)

The app (once deployed) automatically updates your Twitter profile image as your followers change to reflect your Twitter progress with a progress bar!

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy)

<a href="https://www.buymeacoffee.com/anikett" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="41" width="190"></a>

# Setup

## Deployment
You can deploy the app on a Deta Micro. It uses a Deta Base to cache a necessary data. And since it doesn't expose any HTTP endpoints, you can also keep `deta auth` enabled.

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

## Changing colors/gradients
The app uses plain gradient image files (jpeg/png). Either create your own or grab 'em from Internet.s
Here's a [site](https://cssgradient.io/gradient-backgrounds/) that lists all possible sites to get gradients from.

Alternately, you can also use solid colors for the ring. Edit your preference in `config.py`.

## Customization
Edit the `config.py` file according to your liking.

### What's a track mark?
The ring resets on the `track_mark`. Let's say you set it to 100. Then, after reaching 100 followers it will reset back to 0 and count progress towards next 100 i.e. 200 followers.

## Set Auto-Updates
After deploying to a Deta Micro, you can use `CRON` to run micro after every `x` minutes.
E.g. If you want it to check for change after every 60 seconds, set it up with:
```
deta cron set "1 minute"
```

## Reset Cache
Reset complete cache along with the cached avatar with:
```
deta run full-reset
```

Or reset just the followers cache to force a update:
```
deta run reset-count
```

## Installing Requirements (for development)
After creating a virtual environment and activating it, simply run:
```
pip install -r requirements.txt
```
