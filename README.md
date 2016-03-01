# py-twitter-automaton
Bot which automatically retweets and likes tweets based on user whitelist.

### Setup Instructions
1. Clone a copy of the project to your computer.

  ```bash
  git clone https://github.com/MikaSoftware/py-twitter-automaton.git
  ```

2. Setup your virtual environment.

  **OS X Environment:**
  ```bash
  python3 -m venv env
  ```

  **Linux or FreeBSD Environment:**
  ```bash
  virtualenv env
  ```

3. Activate the vritual environment.

  ```bash
  source env/bin/activate
  ```

4. Install the required libraries to operate this script.

  ```bash
  pip install -r requirements.txt
  ```

5. Go to http://apps.twitter.com and create an app. Once finished, be sure to make a copy of the following data:
  * Consumer Key
  * Consumer Secret
  * Access Token
  * Access Secret

6. Go into the source folder and change the **secret_settings.py** file by entering the values you saved from step (5).

  ```bash
  cp src/secret_settings_example.py src/secret_settings.py
  vi src/secret_settings.py
  ```

6. Replace the values with your *Twitter API Keys/Tokens*.

7. Now you are ready to run the application! Enter the following code and you will be able to have it running.

  ```bash
  python3 automaton.py
  ```
