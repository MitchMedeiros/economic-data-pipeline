<h1>App Description &nbsp;&nbsp;
 <a href="https://pypi.org/project/vectorbt" alt="Python Versions">
 <img src="https://img.shields.io/pypi/pyversions/polars.svg?logo=python&logoColor=white">
 </a>
</h1>

This project is a web app built with Plotly Dash with the intent of being an interactive data pipeline.
It uses publicly available second-party economic data requested directly through the REST APIs of multiple
government agencies. These agencies include
the US Treasury Department, Bureau of Economic Analysis (BEA), and the Federal Reserve of St. Louis 
who maintain the Federal Reserve Economic Data (FRED).

The requested data is processed with Polars or Pandas and may be checked for cleanliness and cleaned in several ways.
The data can then be stored in a PostgreSQL database via raw SQL statements issued through Psycopg. The user can create a new table to insert the economic data into, with the freedom to specify
certain table conditions, or alternatively insert into an existing table. The user can also interact with
existing tables, efficiently loading them into DataFrames with ConnectorX, and verifying that they are free
from duplicate values, null values, etc. They can then choose to clean the data and rewrite the existing tables' data.

<h1>Core Dependencies</h1>

The core dependencies are:

<ol>
 <li>Python 3.7 - 3.11</li>
 <li>Python libraries in requirements.txt</li>
</ol>

Note that the requirements.txt file will install psycopg[binary] to reduce overhead. However, it's recommended
that you install psycopg "locally" to ensure system upgradability. Additionally, doing so will install a C-based
module for improved performance. For the system requirements see:
<a href=https://www.psycopg.org/psycopg3/docs/basic/install.html>
psycopg installation</a>

<h2>Cloning This Repository</h2>

To run this app locally you can simply clone this repository. Make sure you have
<a href="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git">
git installed</a>.
You can confirm this on Linux or Mac by typing `git --version` in a terminal. Navigate to the directory you want
the app in and use the command:

```shell
git clone https://github.com/MitchMedeiros/dashapp.git
```

<h2>Creating the Virtual Environment</h2>

If you have Anaconda installed you can create a virtual environment called "econ_venv" using:

```shell
conda create -n econ_venv python=3.10
```

and activate it with `conda activate econ_venv`. Note what default directory it's installed in if you plan to web host the app.

Alternately, you can use the Python venv module with the following command in the directory you want the environment in:

```shell
python3.10 -m venv econ_venv
```

Activate it on Linux/Mac using: `source econ_venv/bin/activate` or in Windows PowerShell: `econ_venv\Scripts\activate`.

<h2>requirements.txt</h2>

With your virutal environment active, navigate inside the app directory and install the libraries in requirements.txt with pip:

```shell
pip3 install -r requirements.txt
```

You can now run the main.py file and visit <a href=127.0.0.1:8050>127.0.0.1:8050</a> in a web browser to access the app.

<h1>Optional Dependencies</h1>

The optional dependencies to extend the functionality of this app are:

<ol>
 <li>PostgreSQL database - for custom data</li>
 <li>Redis database - for faster caching</li>
 <li>mod_wsgi - for web hosting</li>
 <li>Apache HTTP - for web hosting</li>
</ol>

<h2>PostgreSQL and Redis Databases</h2>

The app utilizes a postgreSQL and Redis backend. However, the default configuration file when cloning this repository will use Yahoo Finance for data as well as the local file system for caching between Dash callbacks. If you have either or both databases installed you can connect them by simply providing your connection credentials in config.py, located in the parent directory of this repository.

<h2>WSGI Setup for an Apache Server on Linux</h2>

This section explains how to web host the app on a server. It assumes you have an Apache virtual host set up and linked to a domain name.

You should first install the Apache header files for third-party modules. If you have Apache 2.4 then on Debian/Ubuntu run:

```shell
sudo apt install apache2-dev
```

Now, with your Python virtual environment active:

```shell
pip3 install mod-wsgi
```

Locate your newly created wsgi files with:

```shell
mod_wsgi-express module-config
```

and copy the output. Now create a new .load file in your /etc/apache2/mods-available directory and paste that output inside it

```shell
vim /etc/apache2/mods-available/wsgi.load
```

(If you're new to VIM press `i` to insert text, paste like normal, press `escape`, then `:wq` to save changes and exit. If you make a mistake press `escape` then `:q!` to exit without saving changes or creating a new file.)

Enable the new mod with `a2enmod wsgi`.

Navigate to the .config or .htaccess file (depending on your OS) that you have your virtual host information in. You'll need to add a `WSGIScriptAlias` specifying the location of the app.wsgi file.

If your site is only using HTTP, your virtual host info should look similar to the snippet below. Make sure to replace /path_to_cloned_repository with the appropriate path and yoursite.com with your domain name.

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    WSGIDaemonProcess economic_data python-home=your_python_virtual_env_directory user=www-data group=www-data

    WSGIProcessGroup economic_data
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias / /path_to_cloned_repository/economic_data/app.wsgi

    <Directory /path_to_cloned_repository/economic_data/>
        Require all granted
    </Directory>
</VirtualHost>
```

If your site is set up to use HTTPS via Let's Encrypt then your .config or .htaccess file should look like 

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    RewriteEngine on
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://yoursite.com/$1 [L,R=301]
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/yoursite.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yoursite.com/privkey.pem

    WSGIDaemonProcess economic_data python-home=/path_to_your_virtual_environment user=www-data group=www-data

    WSGIProcessGroup economic_data
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias / /path_to_cloned_repository/economic_data/app.wsgi

    <Directory /path_to_cloned_repository/economic_data/>
        Require all granted
    </Directory>
</VirtualHost>
</IfModule>
```

If you've created a new .config file in one of your ...-available folders rather than adding to an existing file then you'll also need to activate it with the appropriate `a2ensite`, `a2enmod`, or `a2enconf` command.

Now you will need to edit the app.wsgi file in the root directory of the repository. First change the shebang line at the top of the file to the location of your virtual environment and Python version:
```python
#!/path_to_your_virtual_environment/bin/python3.10
```
Also changing the sys.path line shown below to the appropriate root directory for your app

```python
sys.path.insert(0,"/path_to_cloned_repository/economic_data/")
```

Finally, insure that the Apache user: www-data has sufficient file permissions. At a minimum the entire app directory should have the group as www-data with read permissions on all files and also execute permission for app.wsgi. You should add further write or execute permissions to files only as necessary. For security reasons, the directory should be owned by a user other than root.

Restart Apache: `systemctl restart apache2` for all changes to take effect. The app should now be accessible through your domain name!
