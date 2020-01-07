# Donloading Files with IDM via Command Line (Terminal)

## idman_path  /d URL [/p local_path] [/f local_file_name] [/q] [/h][/n] [/a]

## Parameters:
### /d URL 
 **file direct download link**
e.g. IDMan.exe /d "http://www.internetdownloadmanager.com/path/FileName.zip"

---

### /s 
 **starts queue in scheduler**

---

### /p local_path 
  **defines the local path where to save the file**

---

### /f local_file_name 
 **defines the local file name to save the file**

---

### /q 
 **IDM will exit after the successful downloading. This parameter works only for the first copy**

---

### /h 
 **IDM will hang up your connection after the successful downloading**

---

### /n 
 **turns on the silent mode when IDM doesn't ask any questions**

---

### /a 
 **add a file specified with /d to download queue, but don't start downloading**

---

## Parameters /a, /h, /n, /q, /f local_file_name, /p local_path work only if you specified the file to download with /d URL

## The original documentation link
https://www.internetdownloadmanager.com/support/command_line.html