# Comprehensive Dashboard Health Monitoring and Alert
# Created Date: 16th August 2024
# Last Update: -
# Python Developer: Sulaiha Subi
# Goals: Monitors dashboard health, detects errors, and sends automated alerts promptly
# Downloadable data through this link: https://app.selangkah.my/manage2/data_science/portal-dashboard-health-monitor/portal-dashboard-health-monitoring.csv

##################################################################### Process Start Here ###########################################################################

# import libraries
import requests
import csv
from datetime import datetime

############################   Python Class Definition   ############################

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
        Check the status of each dashboard URL, print the results, and save them to a CSV file.
        """
        results = []

        for url in self.urls:
            try:
                response = requests.get(url)
                status = "OK" if response.status_code == 200 else self.error_codes.get(response.status_code, f"Error {response.status_code}")
            except requests.exceptions.RequestException as e:
                status = f"Error: {str(e)}"
            
            # Append the result for each URL
            result = {
                'URL': url,
                'Status': status,
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)

            # Print the result
            print(f"URL: {result['URL']}, Status: {result['Status']}, Timestamp: {result['Timestamp']}")

        self.save_results_to_csv(results)

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
    403: "Forbidden",
    401: "Unauthorized",
    400: "Bad Request"
}

output_csv_file = "/var/www/app-selangkah-my/public_html/manage2/data_science/portal-dashboard-health-monitor/portal-dashboard-health-monitoring.csv"  # Path to the CSV file where results will be saved

# Instantiate the monitor and run the check
monitor = DashboardMonitor(urls_to_monitor, error_codes_to_monitor, output_csv_file)
monitor.check_dashboard_status()
