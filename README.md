Blocklenium
===========

*Blocklenium* provides a means of starting a remote-controlled browser and running a
bookmarklet through a Beckhoff PLC. It was created to control [franka emika robots](https://www.franka.de/)
with a web-based user interface using bookmarklets created with 
[blockly-desk](http://blockly-desk.comemak.at/demos/code/index.html). Other uses are
not recommended, as it performs some rather specific operations on the loaded website
which are characteristic for franka desk.

Prerequisites
=============

This project is intended to run on a [Beckhoff IPC](https://www.beckhoff.com/IPC/) with
a softPLC supporting [ADS](https://infosys.beckhoff.com/english.php?content=../content/1033/cx8190_hw/5091854987.html&id=) running. Also, the following additional Software needs to be installed on the IPC:

- Python >3.6 with PIP
- Chrome Webbrowser
- Selenium Webdriver (See `HOWTO-SELENIUM.md` for instructions)

Installation
============

To install on the IPC, download the `.zip` File from github. Open the `cmd.exe` command utility and type

        pip install C:\Path\to\blocklenium-master.zip
        
Make sure that the IPC has a working internet connection. At the end, you should see
something like this:

        Successfully installed blocklenium-0.0.1
        
The installation process creates a command line executable and registers it to the
appropriate paths. To test if the installation was successful, type

        blocklenium --help
        
You should see a list of the command line parameters. The options `-b` and `-u` are
mandatory (see below).

Intended Use
============

blocklenium is intended to be started by the PLC, and stay active as long as the PLC
is in *Run Mode*. It will terminate on it's own when it loses contact to the ADS
service (i.e. when the PLC is put in *Config Mode*).

blocklenium requires the PLC to provide a boolean flag `GVL.bStartBlockly`. The name
of the flag can be changed using the command line option `--plc_flag`. Setting this
flag to `TRUE` on the PLC starts the browser, loads the web page given with the option
`-u` and then runs the bookmarklet.

If desk requires a login, you must include the `--login-required` flag. blocklenium
will then attempt to read the login credentials from the PLC variables `GVL.sDeskUsername`
and `GVL.sDeskPassword` and enter them in the appropriate fields. If the login page is
not displayed, this is ignored.

Creating bookmarklets
---------------------

When using `blockly-desk` to create bookmarklets, just drag the finished bookmarklet
(marked "V.1" or similar) onto the desktop. This will create a bookmark file with the
ending `.url`. Just pass the path to this file using the command line parameter `-b`.

If you are writing the bookmarklet in javascript from scratch, you can also save the
plain javascript code in a text file with the ending `.js` or `.txt`.

Starting from the PLC
---------------------

**Important:** blocklenium expects the PLC to be in Run Mode **before** it is started.
If you want to test different command line parameters, make sure that the PLC is running
before you start blocklenium.

To start blocklenium from the PLC, use [NT_StartProcess](https://infosys.beckhoff.com/english.php?content=../content/1033/tcplclibutilities/html/tcplclibutilities_nt_startprocess.htm&id),
which needs the `TC2_Utilities` Library enabled on the PLC. See the following example
PLC code:

        PROGRAM MAIN
        VAR
            bStartscript : BOOL := TRUE;
            bBusy : BOOL := FALSE;
            Start_py_script : NT_StartProcess;
        END_VAR

        IF bStartscript = TRUE AND bBusy = FALSE THEN
            Start_py_script(
                NETID := '',
                PATHSTR := 'blocklenium',
                DIRNAME := 'C:\Users\Administrator\Desktop',
                COMNDLINE := '-b V.1.url -u http://robot.franka.de',
                    START := TRUE,
                BUSY => bBusy
            );
            bStartscript := FALSE;
        END_IF

**Please note:** The above code only starts the script, but does not yet open the
browser. To run the bookmarklet, you must set `GVL.bStartBlockly` to `TRUE`.
