import speedtest
import csv
import time
import argparse
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="speed_test.log",
        filemode="a"
    )

def speed_test():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping
    return download_speed, upload_speed, ping

def write_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

if __name__ == "__main__":
    setup_logger()

    parser = argparse.ArgumentParser(description="Internet speed test script.")
    parser.add_argument("--maxtime", type=int, default=600, help="Maximum running time in seconds (default: 600 seconds)")

    args = parser.parse_args()
    max_time = args.maxtime
    end_time = time.time() + max_time

    csv_file = "speed_test_results.csv"

    # Log and print script start message
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_message = f"Speed test script started at {start_time} with a maximum run time of {max_time} seconds."
    logging.info(start_message)
    print(start_message)

    # Write CSV header if the file doesn't exist
    with open(csv_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Download Speed (Mbps)", "Upload Speed (Mbps)", "Ping (ms)"])

    try:
        while time.time() < end_time:
            # Run speed test
            download_speed, upload_speed, ping = speed_test()

            # Print and log results to console
            result_str = f"Download Speed: {download_speed:.2f} Mbps | Upload Speed: {upload_speed:.2f} Mbps | Ping: {ping} ms"
            logging.info(result_str)
            print(result_str)

            # Write results to CSV
            write_to_csv(csv_file, [download_speed:.2f, upload_speed:.2f, ping])

            # Wait for 5 seconds before the next test
            time.sleep(5)

    except KeyboardInterrupt:
        logging.info("Speed test script terminated by user.")
        print("\nSpeed test script terminated.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

    # Log and print script end message
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end_message = f"Speed test script ended at {end_time}. Script ran for {max_time} seconds."
    logging.info(end_message)
    print(end_message)
