[![CircleCI status](https://img.shields.io/circleci/project/oinume/dmm-eikaiwa-tsc.svg)](https://circleci.com/gh/oinume/dmm-eikaiwa-tsc)

# dmm-eikaiwa-tsc

Teacher Schedule Checker for DMM Eikaiwa. This application sends emails to you when  reservable lessons of your favorite teachers are available.

## Deploying to Heroku

You can deploy dmm-eikaiwa-tsc to Heroku easily. At first, click this button.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

And then, input following.

* App Name - Heroku's application name. dmm-eikaiwa-tsc-demo or something.
* TEACHER_IDS - Teacher's IDs what you want to follow
* NOTIFICATION_EMAILS - Email addresses for notification

Finally, click `Heroku Scheduler` link and click `Add new job` button. Next, type `bin/fetcher -l debug` and then click `Save` as follows.

![Heroku Scheduler setting](/../master/doc/heroku_scheduler.png?raw=true "Heroku Scheduler setting")

That's all for now, you'll receive emails of reservable lesson schedules of your favorite teachers.

NOTE, Emails are sent from noreply@lampetty.net, please check a spam folder if you cannot get emails.

## Updating this application

Do you want to deploy any updates to your Heroku environment?
You can deploy this application as follows:

```shell
$ git clone https://github.com/oinume/dmm-eikaiwa-tsc.git
(Or git pull when second time)
$ cd dmm-eikaiwa-tsc
$ heroku git:remote -a <YOUR_APPLICATION_NAME>
$ git push heroku master
---> Starting to deploy to Heroku
```

NOTE: You have to install [Heroku Toolbelt](https://toolbelt.heroku.com/) to use `heroku` command.

## Developing

### Setup

```bash
$ ./setup.sh
$ source venv/bin/activate
```

### Migrating database

```bash
$ alembic upgrade head
```
