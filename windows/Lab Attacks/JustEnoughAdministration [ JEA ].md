# JustEnoughAdministration [ JEA ]

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled.png)

⇒ This my friend, is JEA ( Just Enough Administration ) which is a security technology that enables delegated administration for anything managed by powershell. 

- It limits what users can do by specifying which cmdlets, functions, and external commands they can run.
- It can only constrain powershell access.

---

## Lab Setup

### 1) Setting up Group

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%201.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%201.png)

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%202.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%202.png)

### 2) Setting up JEA

i) Creating Configuration file

```powershell
New-PSSessionConfigurationFile -Path 'C:\Program Files\WindowsPowerShell\endark_conf.pssc'

notepad C:\Program Files\WindowsPowerShell\endark_conf.pssc
```

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%203.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%203.png)

ii) Creating folder for JEA

```powershell
New-Item -Path 'C:\Program Files\WindowsPowerShell\Modules\JEA\RoleCapabilities' -ItemType Directory
```

iii) Creating the PS Role Capability File for the Endark Admins

```powershell
New-PSRoleCapabilityFile -Path 'C:\Program Files\WindowsPowerShell\Modules\JEA\RoleCapabilities\endark_admins.psrc'
notepad C:\Program Files\WindowsPowerShell\Modules\JEA\RoleCapabilities\endark_admins.psrc
```

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%204.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%204.png)

iv) Registering the Configuration

```powershell
Register-PSSessionConfiguration -Name Endark_Admins -Path 'C:\Program Files\WindowsPowerShell\endark_conf.pssc'
Restart-Service WinRM
```

v) Testing it

```powershell
Enter-PSSession -ComputerName vDC01 -credential Andrei -ConfigurationName endark_admins
```

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%205.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%205.png)

- So right now its running in no-language mode which is the safest language mode.

---

## JEA Bypasses

⇒ So there are couple of ways to bypass JEA and i will be showing a few of them

- Constrained Language Mode
- Command Injection
- Script Block Injection

---

### 1) Constrained Language Mode

- In ConstrainedLanguage you are allowed to create new functions and all you gotta do is create a new function that could run anything you want. That is no longer restricted and hence jea can be bypassed.
- NoLanguageMode is the only safe language mode

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%206.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%206.png)

- **`function CommandName { whoami | out-host }`**

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%207.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%207.png)

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%208.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%208.png)

---

### 2) Command Injection

⇒ So the following function takes user input and run Invoke-Expression with Get-Process on it. This function can be easily exploited by escaping the double quotes .

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%209.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%209.png)

- **`Check-Process " ; <command> "`**

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2010.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2010.png)

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2011.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2011.png)

---

### 3) Script Block Injection

⇒ So this script creates a script block which has Invoke-Expression command that includes the input we provided. It runs it on remote system vDC01 as Administrator.

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2012.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2012.png)

- **`Check-Process " ; <command> "`**

![JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2013.png](JustEnoughAdministration%20%5B%20JEA%20%5D/Untitled%2013.png)

---

- Reference : [https://www.youtube.com/watch?v=ahxMOAAani8](https://www.youtube.com/watch?v=ahxMOAAani8) [ Also a lot more attacks covered in the video and mitigation ]