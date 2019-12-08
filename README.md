Server log reader

This is a simple python code which reads server logs and creates a blacklist of IPs that are spamming or taking unusually long times to load.

How to setup ?
==

This code is just for educational purposes.

1. Clone the repo using command  
```git clone <download url found at right corner (green button)>```

2. Open up a terminal  
   ```cd <project directory>```  
   ```py ser[press-tab].py```  

    hit Enter
3. Output will consist of 
    two lists containing IP addresses first list will consist of top 10 requesting IPs.
    Second will consist of blacklisted IPs.
    Blacklisted IPs will be written to a .txt file.

4. Edit log.txt and goodPath.txt for varying the logs and paths.