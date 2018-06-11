# Service Scoring Engine
#### Table
[Summary](#summary)

[Setup](#setup)

[Usage](#usage)

[Contributing](#contributing)

<a id="summary"></a>
### Summary
A python 3 program used to test various service uptimes for a given network infrastructure. 

<a id="setup"></a>
### Setup
1. Git clone this repository:
    - `git clone https://github.com/SilexOne/ise.git`
2. Run the install script:
    - `./ise_setup.sh`
3. Configure the JSON file to your network:
    - The `main.json` chooses if your testing or actually scoring your services and enables which ones you want to use.
4. Run the program:
    - `python main.py`
5. View the website:
    - Browse to the machine that is hosting the SSE `http://#.#.#.#`.
    
<a id="usage"></a>
### Usage
1. Once installed you will need to view and configure the `main.json`.

2. Choose the SSE mode, have a `1` on what mode you want to use:
    - Production: This mode is used to score a team on their network infrastructure 
    - Testing: This mode is primarily used for troubleshooting

    ```
    {
      "0": {
        "name": "production",
        ...
      },
      "1": {
        "name": "testing",
        ...
      }
    }
    ``` 
    For example, Testing mode is selected in this code snippet.
    
3. View the mode's overall settings and configure if needed:
    - `logging`: This sets the logging level for SSE 
    - `timeframe`: This sets how long SSE will score for
    - `services`: This will hold all the service settings
    ```
     "1": {
        "name": "testing",
        "logging": "DEBUG",
        "timeframe": {
          "hours": 0,
          "minutes": 1
        },
        "services": {
            ...
        }
    ```
    For example, logging is set at DEBUG and the test will only run for one minute.

4. View and configure `services`:
    - `enabled`: Determines if the SSE will score that service
    - Other Settings: Specific configuration settings to test
    ```
    "1": {
    "name": "testing",
    "logging": "DEBUG",
    "timeframe": {
      "hours": 0,
      "minutes": 1
    },
    "services": {
      "dns": {
        "enabled": 1,
        "servers": {
          "main": "8.8.8.8",
          "secondary": "8.8.4.4"
        },
        "hostnames": {
          "wcsc.usf.edu": "131.247.1.113",
          "webcse.csee.usf.edu": "131.247.3.5"
        }
      },
      "ad": {
        "enabled": 0
      },
    ```
    For example, `dns` is enabled and the service configuration to be tested is configured as `servers` and `hostnames`.
    `ad` is disabled and will not be tested.

<a id="contributing"></a>
### Contributing
##### Service Test
If you want to test another service that isn't in SSE by default you can easily add one yourself.
1. Within `main.json` add a service in `services` with the appropriate settings in both modes.
    ```
      "0": {
        "name": "production",
        "logging": "INFO",
        "timeframe": {
          ...
        },
        "services": {
          "dns": {
            ...
          }
    ----> "YOUR_SERVICE_NAME": {
    ---->   "enabled": 1,
    ---->   "SETTINGS_USED_IN_THE_PYTHON_FILE": "something"
          },
          ...
        }
      }
    ```

2. Create a python file based off `template.py` and store it in the `services` folder.
    - Follow the template guidelines
    - Import the necessary libraries
    - Ensure the decorator is on your function
    - Use the settings from the json to test your service
    - Return either a 1 or 0 which represent PASS/FAIL
    
3. Run the program and the service should be added.
    
##### Github
1.  Fork the project from github.
2.  Set the upstream repository.

    ```bash
    # Sets your git project upstream to this repository
    $ git remote add upstream https://github.com/SilexOne/ise.git
    ```

3. Ensure your fork's master mirrors the upstream repository. 
   That means you should not make any changes to your master, 
   all you need to create branches off it. You will also need to
   update your master when new changes occur in the overall project.
   
   ```bash
   # Updates your master branch to be the same as the upstream repository
   # Run this specific command everytime the upstream repository changes
   $ git pull upstream master
   
   # Show which branch you are on
   $ git branch
   * master

   # Create a new branch and use it
   $ git checkout -b new-branch-your-creating
   
   # Verify you are using that new branch
   $ git branch
     master
   * new-branch-your-creating

   # Make changes and add to the project
   
   # Add and commit the new changes
   $ git add .
   $ git commit - m "your commit message"

   # Push your branch to your github
   $ git push origin new-branch-your-creating

   # Go to github and do a pull request
   # Then wait for it to be merged in or denied
   ```
 
 4. How to merge your branch if you run into a merge conflict.
 
    ```bash
    # Updates your master branch to be the same as the upstream repository
    $ git pull upstream master
   
    # Your branch will rebase off the new master branch
    $ git rebase master new-branch-your-creating
    ```
    
 5. If your branch was merged in and you want to keep contributing.
 
    ```bash
    # Updates your master branch to be the same as the upstream repository
    $ git pull upstream master

    # Switch back to master
    $ git checkout master

    # Verify you are on master
    $ git branch
    * master
      new-branch-your-creating

    # Branch off master
    $ git checkout -b another-branch-you-created

    # Verify you are on that branch
    $ git branch
      master
      new-branch-your-creating
    * another-branch-you-created

    # Pretty much repeat step 3 with the changes and git add, and step 4 if applicable 
    ```
    
  
 and make your changes then do pull request.