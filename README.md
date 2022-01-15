# Volunteer Core
The Volunteer Core project is a web app that assists in better management of Volunteer Core operations. It will track opportunities for volunteers, and volunteers. Later features could include communications to build out functionality similar to a CRM.

## Development Setup
This setup is for use with local development only; production instructions will be included later. Do not use these instructions in production without turning off debug and resetting the SECRET_KEY in the .env variables.

You will need [git](https://git-scm.com/downloads) to clone this repo.

For the backend you need [python 3](https://www.python.org/downloads/), venv, pip, and SQLite installed. Depending where you get Python from, venv may already be included with Python.

### Prepare Development Enviornment
Clone the repo and cd into the created directory

##### Prepare and start the Flask API
1. `python3 -m venv venv`
1. `source venv/bin/active`
1. `pip install -r requirements.txt`
1. `cp config.env.template .env`
1. `flask db upgrade`
1. Create the admin user: `flask auto-setup`
1. `flask run`
1. You can later end the app with ctrl + c.

## Contributing
We welcome new contributors.  Be sure to check out the guide on [contributing][contributing], which includes instructions on how to fork, clone, branch, commit, pull request and sync your fork.

Not sure where to start? Look for [open issues][githubissue] on GitHub, or message the team on [our Slack site][slack]. If you aren't on our Slack, [click here for an invite][slackinvite].

TL;DR Contribution Workflow:

1. [Fork][fork] this repository and Clone your fork locally.
1. Checkout a new branch on which to make your changes.
1. Make edits. Try to match existing coding style.
1. Test your changes.
1. Commit your changes. Push your changes to your fork on GitHub.
1. Submit a new [pull request][pullrequest] and your changes will be reviewed and merged.

## Bugs / Feedback / Suggestions / Questions

We encourage you to [open up an issue][newissue] if you have any feedback, suggestions, bugs or just have a question on where to start.

## License

MIT, see [LICENSE](/LICENSE) for full license.

[slack]: https://codeforfoco.slack.com/
[slackinvite]: https://codeforfocoslack.herokuapp.com
[fork]: https://help.github.com/articles/fork-a-repo/
[forkthisrepo]: https://github.com/CodeForFoco/volunteercore#fork-destination-box
[contributing]: https://github.com/CodeForFoco/org/blob/master/CONTRIBUTING.md
[githubissue]: https://github.com/CodeForFoco/volunteercore/issues
[newissue]: https://github.com/CodeForFoco/volunteercore/issues/new
[pullrequest]: https://github.com/CodeForFoco/volunteercore/pulls
