# Project Name

## Description
[Provide a brief description of your project here]

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Local Installation

```bash
git clone https://github.com/lsangeao/checkmailauthenticationtool.git

cd checkmailauthenticationtool
poetry install

```

## Usage

You should fill the domains.csv file as follow:

```csv
domain,selector
<domain1>,<selector>
<domain2>
```

If you don't know your selector, ask your DNS provider.
If you don't fill the selector, dkim will not be verified.

``` poetry run app-start ```

## Contributing

Contributions are not allowed

## License

GPL
