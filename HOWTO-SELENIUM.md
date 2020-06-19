# Installing Selenium for Chrome on IPC

## Prerequisites:

- Python, PIP installed
- Chrome webbrowser installed

## Steps

1. Download WebDriver for approriate Chrome version from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads)

2. Copy the executable to `C:\WebDriver\bin`

3. Add the WebDriver location to `PATH` (using `cmd.exe`):
        
        setx /m path "%path%;C:\WebDriver\bin\"
        
4. Install Selenium with PIP (also using `cmd.exe`):

        pip install selenium

## Usage

Test if everything worked in Python console:

        from selenium import webdriver
        
        # Instantiate driver (opens browser)
        driver = webdriver.Chrome('C:\\WebDriver\\bin\\chromedriver.exe')
        
        # Open a website
        driver.get('http://www.google.com/');
        
        # Execute javascript
        driver.execute_script("javascript:alert('hi!');")
        
        # Close browser
        driver.quit()
      
## References

- [Selenium](https://www.selenium.dev)

- [RealPython Tutorial](https://realpython.com/modern-web-automation-with-python-and-selenium/)