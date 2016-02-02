# Facebook API wrapper

 * `db` - contains models (`models.py`) and database connection config (`config.py`)
 * `constraints.py` - file with API credentials
 * `feed_wrapper.py` - parses Facebook posts feed
 * `wrapper.py <MODE>` - receives a rest of facebook data. Has two possible modes:
 	- `wrapper.py historical` - parses historical engagement and users data
 	- `wrapper.py country` - parses historical users data broken down by country

## Launch instructions


 * to launch scripts
    - `wrapper.py`:

    ```
	python wrapper.py <historical|country>
    ```

   - `feed_wrapper.py`:

   ```
	python feed_wrapper.py
   ```
   
## Crontab script

```
/usr/bin/python <PATH_TO_SCRIPTS>/wrapper.py country
/usr/bin/python <PATH_TO_SCRIPTS>/wrapper.py historical
/usr/bin/python <PATH_TO_SCRIPTS>/feed_wrapper.py

```