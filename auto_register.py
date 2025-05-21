import requests
import random
import string
import time
from faker import Faker
from bs4 import BeautifulSoup
import logging
import os
import csv
import re
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("registration.log"),
        logging.StreamHandler()
    ]
)

class ReferralRegistration:
    def __init__(self, target_url, referral_code=None):
        self.target_url = target_url
        # Extract referral code from URL if present
        parsed_url = urlparse(target_url)
        url_params = parse_qs(parsed_url.query)
        if 'ref' in url_params and not referral_code:
            self.referral_code = url_params['ref'][0]
            logging.info(f"Extracted referral code from URL: {self.referral_code}")
        else:
            self.referral_code = referral_code
            
        self.faker = Faker()
        self.session = requests.Session()
        self.success_count = 0
        self.failure_count = 0
        self.consecutive_failures = 0
        self.daily_limit = 500
        self.proxies = []
        self.working_proxies = []
        self.load_socks5_proxies()  # Load the SOCKS5 proxies
        self.user_agents = self.load_user_agents()
        self.use_proxy = True  # Always use proxy by default
        
    def test_proxy(self, proxy):
        """Test if a proxy is working by making a request to ipinfo.io"""
        try:
            session = requests.Session()
            proxy_url = self.format_proxy_url(proxy)
            session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            session.headers.update({"User-Agent": self.rotate_user_agent()})
            # Use a 5 second timeout for quick testing
            response = session.get("https://ipinfo.io/json", timeout=5, verify=False)
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logging.debug(f"Proxy {proxy} failed test: {str(e)}")
            return False
            
    def load_socks5_proxies(self):
        """Load the provided SOCKS5 proxies"""
        logging.info("Loading SOCKS5 proxies...")
        
        # New list of reliable SOCKS5 proxies
        socks5_proxies = [
            # New proxies from user request (May 21, 2025)
            "176.57.69.177:16379",
            "187.63.9.62:63253",
            "183.96.222.70:28572",
            "51.158.70.246:16379",
            "212.119.236.86:1080",
            "176.120.26.112:1080",
            "212.47.251.132:16379",
            "95.188.79.3:1080",
            "8.218.39.40:10800",
            "5.172.24.68:1080",
            "209.97.169.41:13108",
            "198.244.147.24:1212",
            "178.32.202.54:5330",
            "69.202.164.128:1080",
            "34.166.117.165:1080",
            "51.15.210.52:16379",
            "103.189.218.158:1080",
            "161.49.116.131:1338",
            "103.179.124.10:1080",
            "103.169.254.155:1080",
            "46.146.196.217:1080",
            "103.189.218.83:6969",
            "115.127.124.234:1080",
            "37.157.217.144:10810",
            "192.111.137.35:4145",
            "199.229.254.129:4145",
            "67.201.39.14:4145",
            "192.252.215.5:16137",
            "68.71.251.134:4145",
            "192.111.139.162:4145",
            "68.71.240.210:4145",
            "162.253.68.97:4145",
            "31.42.185.134:1080",
            "62.171.176.129:27290",
            "72.37.216.68:4145",
            "166.62.36.126:45982",
            "192.111.135.17:18302",
            "142.54.236.97:4145",
            "67.201.33.10:25283",
            "45.79.203.254:48388",
            "198.199.86.11:1080",
            "51.158.71.156:16379",
            "209.141.45.119:56666",
            "138.68.60.8:1080",
            "206.189.57.182:1080",
            "78.37.113.27:5555",
            "51.158.65.148:16379",
            "212.47.249.56:16379",
            "172.234.67.180:1080",
            "213.226.122.5:7788",
            "104.200.152.30:4145",
            "149.202.80.220:29768",
            "174.77.111.196:4145",
            "167.71.171.141:1080",
            "93.187.188.30:1080",
            "95.164.44.14:1080",
            "199.102.107.145:4145",
            "68.71.252.38:4145",
            "68.71.242.118:4145",
            "147.45.170.65:1080",
            "167.172.138.48:49167",
            "51.15.206.101:16379",
            "51.15.232.175:16379",
            "173.212.239.181:11001",
            "93.184.5.121:1080",
            "89.46.249.248:5432",
            "163.172.187.22:16379",
            "212.47.254.121:16379",
            "119.148.39.241:9990",
            "142.54.237.34:4145",
            "67.201.59.70:4145",
            "178.32.202.54:39188",
            "24.249.199.12:4145",
            "192.252.220.89:4145",
            "67.201.58.190:4145",
            "68.71.245.206:4145",
            "134.199.159.23:1080",
            "212.47.235.189:16379",
            "159.65.128.194:1080",
            "142.54.232.6:4145",
            "82.223.165.28:38245",
            "160.19.16.86:1080",
            "68.1.210.189:4145",
            "109.135.16.145:49879",
            "51.158.105.157:16379",
            "143.110.190.60:1080",
            "172.104.164.41:1080",
            "45.117.62.33:6250",
            "43.134.123.32:1090",
            "213.169.39.234:31098",
            "198.8.94.170:4145",
            "142.54.229.249:4145",
            "47.242.195.255:8888",
            "174.77.111.197:4145",
            "172.233.254.134:1080",
            "142.54.239.1:4145",
            "98.175.31.222:4145",
            "27.254.67.114:19902",
            "163.172.164.115:16379",
            "103.135.139.121:6969"
        ]
        
        # Try to load previously saved working proxies
        try:
            if os.path.exists('working_proxies.txt'):
                logging.info("Loading previously saved working proxies...")
                with open('working_proxies.txt', 'r') as f:
                    working_count = 0
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and line not in socks5_proxies:
                            socks5_proxies.append(line)
                            working_count += 1
                logging.info(f"Added {working_count} proxies from working_proxies.txt")
        except Exception as e:
            logging.error(f"Error loading working proxies: {str(e)}")
        
        # Also attempt to load proxies from the proxies.txt file
        try:
            if os.path.exists('proxies.txt'):
                logging.info("Loading additional proxies from proxies.txt")
                with open('proxies.txt', 'r') as f:
                    added_count = 0
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            # Add the proxy if it's not already in the list
                            if line not in socks5_proxies:
                                socks5_proxies.append(line)
                                added_count += 1
                logging.info(f"Added {added_count} proxies from proxies.txt")
        except Exception as e:
            logging.error(f"Error loading proxies from proxies.txt: {str(e)}")
        
        self.proxies = socks5_proxies
        self.working_proxies = socks5_proxies.copy()  # Consider all proxies working initially
        
        logging.info(f"Loaded {len(self.proxies)} SOCKS5 proxies total")
    
    def load_user_agents(self):
        """Return a list of realistic user agents"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/96.0.4664.53 Mobile/15E148 Safari/604.1"
        ]
    
    def generate_user_info(self):
        """Generate random human-like user information"""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        name = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 9999)}@{self.faker.free_email_domain()}"
        password = self.generate_secure_password()
        
        return {
            "name": name,
            "email": email,
            "password": password,
            "password_confirmation": password,
            "first_name": first_name,
            "last_name": last_name
        }
    
    def generate_secure_password(self):
        """Generate a secure password"""
        length = random.randint(10, 14)
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def rotate_user_agent(self):
        """Select a random user agent"""
        return random.choice(self.user_agents)
    
    def get_random_proxy(self):
        """Get a random proxy from the list of working proxies"""
        if not self.use_proxy:
            return None
            
        # Use a working proxy
        if self.working_proxies:
            return random.choice(self.working_proxies)
        elif self.proxies:  # Fall back to all proxies if no working ones
            return random.choice(self.proxies)
        
        return None
    
    def remove_non_working_proxy(self, proxy):
        """Remove a non-working proxy from the working proxies list"""
        if proxy and proxy in self.working_proxies:
            self.working_proxies.remove(proxy)
            logging.info(f"Removed non-working proxy from list: {proxy}")
    
    def save_account(self, user_info):
        """Save account information to CSV file"""
        file_exists = os.path.isfile('accounts.csv')
        
        with open('accounts.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['name', 'email', 'password', 'date_registered'])
            
            writer.writerow([
                user_info['name'],
                user_info['email'], 
                user_info['password'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            logging.info(f"Account saved to accounts.csv: {user_info['name']} / {user_info['email']}")
    
    def test_website_access(self):
        """Test if we can access the website through proxy"""
        try:
            proxy = self.get_random_proxy()
            if proxy:
                # Format proxy URL based on whether it has authentication
                proxy_url = self.format_proxy_url(proxy)
                self.session.proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
                logging.info(f"Testing with proxy: {proxy.split(':')[0]}:{proxy.split(':')[1]}")
            else:
                logging.error("No proxies available for website testing.")
                return False
                
            self.session.headers.update({"User-Agent": self.rotate_user_agent()})
            response = self.session.get(self.target_url, timeout=12, verify=False)
            if response.status_code == 200:
                logging.info("Successfully accessed website through proxy!")
                return True
            else:
                logging.warning(f"Failed to access website. Status code: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Error accessing website: {str(e)}")
            return False
    
    def extract_form_fields(self, soup):
        """Extract all form fields and their values from the HTML"""
        form_data = {}
        form = soup.find('form')
        
        if form:
            fields = form.find_all(['input', 'select', 'textarea'])
            for field in fields:
                field_name = field.get('name')
                if field_name:
                    # Skip submit buttons
                    if field.get('type') == 'submit':
                        continue
                    
                    # Get default value if present
                    field_value = field.get('value', '')
                    form_data[field_name] = field_value
                    
        return form_data
    
    def is_authenticated_proxy(self, proxy):
        """Check if the proxy string contains authentication credentials"""
        return len(proxy.split(':')) >= 3
    
    def format_proxy_url(self, proxy):
        """Format proxy URL correctly, handling authentication if present"""
        parts = proxy.split(':')
        if len(parts) >= 4:  # IP:PORT:USER:PASS format
            ip, port, username, password = parts[:4]
            return f"socks5://{username}:{password}@{ip}:{port}"
        else:  # Regular IP:PORT format
            return f"socks5://{proxy}"
    
    def register_account(self, user_info):
        """Attempt to register an account on the target website"""
        # Reset session
        self.session = requests.Session()
        
        # Set a random user agent
        self.session.headers.update({"User-Agent": self.rotate_user_agent()})
        
        # Set a random proxy
        proxy = None
        proxy = self.get_random_proxy()
        if proxy:
            # Format proxy URL based on whether it has authentication
            proxy_url = self.format_proxy_url(proxy)
            self.session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            logging.info(f"Using proxy: {proxy.split(':')[0]}:{proxy.split(':')[1]}")  # Only log IP:PORT part for security
        else:
            logging.error("No proxies available. Cannot proceed without a proxy.")
            return False
        
        try:
            # First, visit the registration page to get any CSRF tokens
            response = self.session.get(self.target_url, timeout=12, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Debug for form fields
            logging.info("Analyzing registration form...")
            form = soup.find('form')
            
            # Collect field names dynamically
            field_names = {}
            
            if form:
                for input_field in form.find_all('input'):
                    field_name = input_field.get('name')
                    field_type = input_field.get('type')
                    if field_name:
                        logging.info(f"Found form field: {field_name} (type: {field_type})")
                        field_names[field_type] = field_name
            
            # Find CSRF token
            csrf_token = None
            token_field = soup.find('input', {'name': '_token'}) or soup.find('meta', {'name': 'csrf-token'})
            if token_field:
                if token_field.get('value'):
                    csrf_token = token_field.get('value')
                elif token_field.get('content'):
                    csrf_token = token_field.get('content')
                
                if csrf_token:
                    logging.info(f"Found CSRF token: {csrf_token[:10]}...")
            
            # Find form action URL
            form_action = self.target_url
            if form and form.get('action'):
                if form['action'].startswith('http'):
                    form_action = form['action']
                else:
                    # Handle relative URLs
                    parsed_url = urlparse(self.target_url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    form_action = f"{base_url}{form['action']}"
                logging.info(f"Form action URL: {form_action}")
            
            # Start with all existing form fields and default values
            form_data = self.extract_form_fields(soup)
            
            # Add our generated user info - using the correct field names from the form
            form_data.update({
                'name': user_info['name'],
                'email': user_info['email'],
                'password': user_info['password'],
                'password_confirmation': user_info['password_confirmation']
            })
            
            # Add CSRF token if found and not already in form_data
            if csrf_token and '_token' not in form_data:
                form_data['_token'] = csrf_token
            
            # Add referral code if provided
            if self.referral_code:
                form_data['referral_code'] = self.referral_code
            
            logging.info(f"Submitting registration for: {user_info['name']} / {user_info['email']}")
            
            # Submit registration
            time.sleep(random.uniform(1, 3))  # Random delay to appear human-like
            response = self.session.post(form_action, data=form_data, timeout=12, verify=False)
            
            # Reset consecutive failures counter
            self.consecutive_failures = 0
            
            # Check if registration was successful
            success_indicators = [
                "success", "thank you", "welcome", "dashboard", 
                "successfully", "account created", "verification", "home"
            ]
            
            # Debug response
            logging.debug(f"Response status: {response.status_code}")
            logging.debug(f"Response URL: {response.url}")
            
            # Check if we were redirected to a success page or dashboard
            was_redirected = response.url != form_action
            if was_redirected:
                logging.info(f"Redirected to: {response.url}")
            
            success = False
            for indicator in success_indicators:
                if indicator in response.text.lower():
                    success = True
                    logging.info(f"Found success indicator: '{indicator}' in response")
                    break
                    
            if success or (response.status_code == 302) or was_redirected:
                logging.info(f"Successfully registered: {user_info['email']}")
                self.save_account(user_info)
                self.success_count += 1
                return True
            else:
                logging.warning(f"Failed to register: {user_info['email']} - Status: {response.status_code}")
                
                # Try to extract error message
                error_msg = ""
                error_elems = [
                    soup.find('div', {'class': 'alert-danger'}),
                    soup.find('div', {'class': 'error'}),
                    soup.find('span', {'class': 'invalid-feedback'})
                ]
                
                # Try parsing response for error messages
                response_soup = BeautifulSoup(response.text, 'html.parser')
                for selector in ['.alert-danger', '.error', '.invalid-feedback', '.text-danger']:
                    error_elems += response_soup.select(selector)
                
                for error_elem in error_elems:
                    if error_elem:
                        msg = error_elem.text.strip()
                        if msg:
                            error_msg += msg + " | "
                
                if error_msg:
                    logging.warning(f"Error message: {error_msg}")
                
                # Save the HTML response for debugging
                with open("last_failed_response.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                logging.info("Saved failed response HTML to last_failed_response.html")
                    
                self.failure_count += 1
                return False
                
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            self.failure_count += 1
            self.consecutive_failures += 1
            
            # If the proxy failed, remove it from working proxies
            if proxy:
                self.remove_non_working_proxy(proxy)
            
            return False
    
    def save_working_proxies(self):
        """Save working proxies to a file for future use"""
        try:
            with open('working_proxies.txt', 'w') as f:
                for proxy in self.working_proxies:
                    f.write(f"{proxy}\n")
            logging.info(f"Saved {len(self.working_proxies)} working proxies to working_proxies.txt")
        except Exception as e:
            logging.error(f"Error saving working proxies: {str(e)}")
    
    def run_campaign(self, num_registrations=100):
        """Run registration campaign with specified number of accounts"""
        # Always use proxies
        self.use_proxy = True
        logging.info("Starting with proxy enabled to avoid IP detection")
            
        daily_count = 0
        
        for i in range(num_registrations):
            if daily_count >= self.daily_limit:
                logging.info(f"Daily limit reached ({self.daily_limit}). Stopping.")
                break
                
            # Generate new user info
            user_info = self.generate_user_info()
            success = self.register_account(user_info)
            
            if success:
                daily_count += 1
            
            # Random delay between registrations - longer delays to avoid detection
            delay = random.uniform(15, 35)  # Increased delay to avoid IP detection
            logging.info(f"Waiting {delay:.2f} seconds before next registration")
            time.sleep(delay)
            
            # Summary at regular intervals
            if (i + 1) % 10 == 0 or success:
                logging.info(f"Progress: {i+1}/{num_registrations} - Success: {self.success_count}, Failures: {self.failure_count}")
    
            # Save working proxies periodically
            if (i + 1) % 20 == 0:
                self.save_working_proxies()
    
        # Save working proxies at the end
        self.save_working_proxies()
        logging.info(f"Campaign completed - Total: {num_registrations}, Success: {self.success_count}, Failures: {self.failure_count}")

if __name__ == "__main__":
    # Configuration - using the specific HostingKarle URL with referral code
    TARGET_URL = "https://client.hostingkarle.com/register?ref=Hz4shhcR"
    
    # Create and run the registration bot
    bot = ReferralRegistration(TARGET_URL)
    
    # Number of registrations to attempt (max 500 per day recommended)
    bot.run_campaign(num_registrations=2000) 