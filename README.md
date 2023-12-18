# curie_holdings_task
With script crate_draft_gmail.py you can create a draft of an email inside your Gmail account.
To do this You should create Google project following https://developers.google.com/workspace/guides/create-project
When all steps of project creating will be done, you will receive "credentials.json" file.
While the project is in Test mode, don't forget to add test users accounts, so You can pass with OAuth.

## Installing / Getting started

A quick introduction of the minimal setup you need to get create_draft_gmail
running.

### Python3 must be already installed!
To run the script(when You already have "credentials.json"), follow this commands in terminal:
```shell
git clone https://github.com/arturiermolenko/curie_holdings_task
cd curie_holdings_task
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

The next step, You should rename file .env_sample to .env and fill this file with necessary data.

Then you can run:
```shell
python3 create_draft_gmail.py
```
and follow the inputs.

The inputs of subject, email address and email content are added only to let running the script from terminal and to add data manually.
You can remove "if `name` == `__main__`" section and call CreateDraft class for creation it's instance with your parameters.

With the first run You should pass authentication with Your Google account credentials. Then "token.json" file will be created, and next time script will take/refresh token from that file.
