# Notes

Based off of [this repo](https://github.com/pmahend1/BingRewards).

---

- Run EdgeBrowser Selenium container like this:

    ```sh
    docker run --rm -p 4444:4444 -p 7901:7900 --shm-size="2g" selenium/standalone-edge:4.1.1-20211217
    ```

The password for Selenium container is `secret`, taken from [here](https://github.com/SeleniumHQ/docker-selenium).

---

- Save python requirements like this:

    ```sh
    python3.9 -m pip freeze > requirements.txt
    ```

- Create python venv like this:

    ```sh
    python3.9 -m venv .venv
    ```

- Install py `requirements.txt` like this:

    ```sh
    python3.9 -m pip install -r requirements.txt
    ```
