# jira2wordcloud

script for converting JIRA tickets to wordcloud.

Requires python3.

Currently script is made for handling Japanese.

Sample image is as follows. More text will be output in actual cases.
![](./jira2wordcloud.png)


## Usage

```
# for building virtual envrionment
$ pyenv install 3.7.2
$ pyenv local 3.7.2
$ python3 -m venv env
$ source env/bin/activate

# below is minimum
(env) $ pip install -r requirements.txt
(env) $ python main.py -f 2018-12-01 -t 2019-01-01
```
