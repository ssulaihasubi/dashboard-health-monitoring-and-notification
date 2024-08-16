# Comprehensive Dashboard Health Monitoring and Alert
# Created Date: 16th August 2024
# Last Update: -
# Python Developer: Sulaiha Subi
# Goals: Monitors dashboard health, detects errors, and sends automated alerts promptly


##################################################################### Process Start Here ###########################################################################

# import libraries
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

############################   Python Class Definition   ############################

import requests
import csv
from datetime import datetime

class DashboardMonitor:
    def __init__(self, urls, error_codes, output_file):
        """
        Initialize the DashboardMonitor with a list of URLs, error codes to monitor, and the output CSV file.
        :param urls: List of dashboard URLs to monitor.
        :param error_codes: Dictionary mapping HTTP status codes to error messages.
        :param output_file: Path to the output CSV file where results will be saved.
        """
        self.urls = urls
        self.error_codes = error_codes
        self.output_file = output_file

    def check_dashboard_status(self):
        """
        Check the status of each dashboard URL and save the results to a CSV file.
        """
        print("Checking dashboard status...")
        results = []

        for url in self.urls:
            print(f"Checking URL: {url}")
            try:
                response = requests.get(url)
                status = "OK" if response.status_code == 200 else self.error_codes.get(response.status_code, f"Error {response.status_code}")
                print(f"Status code for {url}: {response.status_code} - Status: {status}")
            except requests.exceptions.RequestException as e:
                status = f"Error: {str(e)}"
                print(f"Error while checking {url}: {str(e)}")
            
            # Append the result for each URL
            results.append({
                'URL': url,
                'Status': status,
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        self.save_results_to_csv(results)
        print("Status check and saving results completed.")

    def save_results_to_csv(self, results):
        """
        Save the monitoring results to a CSV file.
        :param results: List of dictionaries containing URL monitoring results.
        """
        # Define the CSV headers
        headers = ['URL', 'Status', 'Timestamp']

        # Write to the CSV file
        try:
            with open(self.output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(results)
            print(f"Results saved to {self.output_file}")
        except Exception as e:
            print(f"Failed to save results to CSV: {str(e)}")

# Configuration
urls_to_monitor = [
    # 'https://dashboard-url-1.com',
    # 'https://dashboard-url-2.com',
    'https://ekonomi-penjagaan.myhayat.life/'
]

error_codes_to_monitor = {
    502: "502 Bad Gateway",
    500: "500 Internal Server Error",
    404: "404 Not Found",
    403: "403 Forbidden",
    401: "401 Unauthorized",
    400: "400 Bad Request"
}

output_csv_file = "dashboard_status.csv"  # Path to the CSV file where results will be saved

# Instantiate the monitor and run the check
monitor = DashboardMonitor(urls_to_monitor, error_codes_to_monitor, output_csv_file)
monitor.check_dashboard_status()
