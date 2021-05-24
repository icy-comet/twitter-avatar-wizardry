## Introduction
A Python recreation of the popular tool [blackmagic.so](https://blackmagic.so) created by [Tony Dinh](https://github.com/trungdq88).

The script automatically updates your Twitter profile image as your Followers change to reflect your progress towards the desired number of followers with a progress bar.

## Example Image
![example](example.png)

## Setup

### Installing Requirements
After creating a virtual environment and activating it, simply run:
```
pip install -r requirements.txt
```

### Loading API keys
The script looks for them in environment variables.

If using on a local machine, place the keys inside a `.env` file in the project's directory and you should be good to go. Example:
```
API_KEY=AAAAAA
API_SECRET_KEY=BBBB
ACCESS_TOKEN=CCCCC
ACCESS_TOKEN_SECRET=CCCCC
```

### Customization
You can also customize the colors of the progress bar created and your target number of followers. Just update the appropriate variables under `imports`.

```
screen_name='<your Twitter username>'
progress_mark = <show progress towards every leap (e.g. for every 100 followers)>
primary_arc_color = '<hex color>'
secondary_arc_color = '<hex color>'
```

### Run
Running would be as simple as `python script.py`