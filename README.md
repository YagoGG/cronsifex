# cronsifex

Automatically update your Transifex resources, from a remote source.

Designed to work as a [Cron](https://en.wikipedia.org/wiki/Cron) job, although
it can be run manually.

## Setup

1. Clone the repo.

    ```bash
    $ git clone https://github.com/YagoGG/cronsifex
    $ cd cronsifex
    ```

2. Install the dependencies.

    ```bash
    $ pip install -r requirements.txt
    ```

3. Create a copy of the configuration file.

    ```bash
    $ cp conf.ini-template conf.ini
    ```

4. Fill in your custom settings (see [below](#config-file)).
5. Run it!

    ```bash
    $ python cronsifex.py
    ```

## Config file

You can find the template configuration file in `conf.ini-template`. It looks
like this:

```ini
[transifex]
username=<your_transifex_username>
password=<your_api_token>
project_slug=<your_project_name>

[resources]
<resource_name>=<remote_file_url>
```

Inside the `transifex` section you should put the information relative to your
Transifex account and project.
 - `username`: your Transifex username or email address. **If you're going to
    use an API key, type `api` instead.**
 - `password`: either your Transifex account password, or an API token (you can
    get one [here](https://www.transifex.com/user/settings/api/)). It is highly
    encouraged to use an API token instead of a password.
 - `project_slug`: the name of the Transifex project whose resources you want
    to update (e.g. `zulip`).

In the `resources` section you have to put all the resources in your project
that you want to update. You can put as many as you want, with the resource's
name as the key, and the URL where the up-to-date resource can be found as the
value.

Here's an example:

```ini
translationsjson=https://raw.githubusercontent.com/zulip/zulip/master/static/locale/en/translations.json
```

---

&copy; 2017 [Yago González](https://github.com/YagoGG). All rights reserved.
