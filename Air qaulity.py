import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import imageio

# Function to fetch air quality data for a given date and station
def fetch_air_quality_data(date, station_id):
    url = f'http://www.cpcb.gov.in/CAAQM/frmUserAvgReportCriteria.aspx?StationName=Delhi&StateId=6&CityId=85&StationId={station_id}&FromDateTime={date}%2000:00:00&ToDateTime={date}%2023:59:59'
    response = requests.get(url, verify=False)  # Disable SSL verification
    if response.status_code == 200:
        return pd.read_html(response.text)[0]
    else:
        return None

# Main function
def main():
    # Define the date range for the month
    start_date = '2024-01-01'
    end_date = '2024-01-31'
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Define station IDs for Delhi (you may need to get a list of station IDs)
    station_ids = [143, 140, 142]  '''RK Puram (RKP): Station ID - 143
                                      Punjabi Bagh (PB): Station ID - 140
                                      Mandir Marg (MM): Station ID - 142'''

    # Create a directory to store images
    output_dir = 'air_quality_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through each date
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        images = []  # To store images for each date

        for station_id in station_ids:
            air_quality_data = fetch_air_quality_data(date_str, station_id)
            
            if air_quality_data is not None:
                # Visualize air quality data for the current date and station
                plt.figure(figsize=(10, 6))
                # Your visualization code goes here
                plt.plot(air_quality_data['Time'], air_quality_data['PM2.5'], marker='o', linestyle='-')
                plt.title(f'Air Quality for Delhi - Station {station_id} - {date_str}')
                plt.xlabel('Time')
                plt.ylabel('PM2.5 (µg/m³)')
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Save the plot as an image
                image_path = os.path.join(output_dir, f'air_quality_{date_str}_station_{station_id}.png')
                plt.savefig(image_path)
                plt.close()

                images.append(image_path)

        # Create a GIF for the current date
        gif_path = os.path.join(output_dir, f'air_quality_{date_str}.gif')
        with imageio.get_writer(gif_path, mode='I', duration=1) as writer:
            for image in images:
                writer.append_data(imageio.imread(image))

if __name__ == "__main__":
    main()
