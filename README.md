Hi! This application was created to collect player statistics.

Before using, enter the command:```python3 -m pip install -r req.txt```

The application uses commands such as:
1. To divide teams by region:
```
python3 script.py grouped-teams  
```
2. Must answer with the tallest and shortest player of that name or surname. 
But there is almost no such data in the API, so the command is not very useful:
```
python3 script.py players-stats --name Michael
```
3. Command for summing up the statistics of teams for a certain season. 
You can use other formats instead of **strdout** to save, like:
- *json*
- *csv* 
- *sqlite3*

```
"python3 script.py teams-stats --season 2017 --output stdout"
```
