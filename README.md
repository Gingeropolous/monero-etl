# monero-etl
Tool to get your personal transaction data out of the Monero blockchain into other data formats.

* release 0.0.1
* Currently supports csv destination
* Additional  destinations planned: SQL and BeanCounter
* open source: https://github.com/tiedtoastar/monero-etl/
* works with Monero 0.12.x and later
* Provides easy step by step configuration to your running Monero RPC
* python 3.x compatible

Want to help?

If you find this project useful, please consider a donation to the following address: 

* 88ie1Zyr2v1bsJFUQBscA4Aq1cv5M1nmsCSj7dPxfiewGbKuJkqwG15MTGQLTo5K3oGaEdDbhDp7QiTSPoxC2SyQUp1deri

Please support developers that made this project possible:

* https://github.com/emesik/monero-python


Usage
-----------

1. Clone the repo
2. Create virtualenv & activate it

.

    python3 -m venv .venv
    source .venv/bin/activate

3. Install dependencies

.

    pip install -r requirements.txt -r test_requirements.txt
    pip install git+https://github.com/emesik/monero-python.git

4. Do your thing

5. Run tests

