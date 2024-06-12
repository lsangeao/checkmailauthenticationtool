# Check Mail Authentication tool

## Description

This project will provide organizations an effective tool to improve the security of their email infrastructure and reduce the risk of cyber attacks.

## Table of Contents

- [ServerLess Installation](#ServerLess)
- [Local Installation](#Local)
- [Contributing](#contributing)
- [License](#license)

## ServerLess Installation

If you don't have a server to run the code, you can [create a fork](https://docs.github.com/es/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository)

Once you have a copy of the repository, you can proceed to adapt it to your needs:

- [Create Secrets for the repository](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)

|Secret Name|Secret Value|
|---|---|
|MAIL_USERNAME|gmail account|
|MAIL_PASSWORD|[gmail app password](https://support.google.com/mail/answer/185833?hl=en)|
|MAIL_TO|Email Recipients|
|MAIL_FROM|Email Sender|

- Change the schedule by editing the line 5 on [this](.github/workflows/main.yml) file. If you are not familiar with crontab expressions this [link](https://crontab.guru/) can be helpful for you.

- Edit the [files/domains.csv](files/domains.csv) file as follow:

    ```csv
    domain,selector
    <domain1>,<selector>
    <domain2>
    ```

> If you don't know your selector, ask your DNS provider.
> If you don't fill the selector, dkim will not be verified.

- Change [workflow permissions](https://github.com/ad-m/github-push-action/issues/96#issuecomment-1740080754)

## Local Installation

Local Installation is only for testing purposes.


This project requires:
- python 3.10.5 or higher (Default in Ubuntu 22.04)
- poetry : ```curl -sSL https://install.python-poetry.org | python3 -```

```bash
git clone https://github.com/lsangeao/checkmailauthenticationtool.git

cd checkmailauthenticationtool
poetry install

```

### Usage

Edit the [files/domains.csv](files/domains.csv) file as follow:

```csv
domain,selector
<domain1>,<selector>
<domain2>
```

If you don't know your selector, ask your DNS provider.
If you don't fill the selector, dkim will not be verified.

```bash 
    poetry run app-start 
    cat files/output.txt
```


#### Test

There is a file [test/mocks/domains.csv](tests/mocks/domains.csv) to perform tests
If you want to force differences , you should edit the file [test/mocks/domains1.json](tests/mocks/domains1.json)

You can run a test running the following command:

``` poetry run app-test ```

You can check the result in the file: [files/output.txt](files/output.txt)




## Contributing

Contributions are not allowed

## License

GPL
