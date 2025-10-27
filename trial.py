import iom

# Specify the file path to your IOM file
file_path = r"C:\path\to\your\file.h5"  # Update this path

# Create IOM_file object
iom_file = iom.IOM_file(file_path)

# Read and format the data
iom_file.read_data(format=True)

# Plot the EEG data
if iom_file.is_eeg_present:
    print(f"Processing file: {iom_file.f_name}")
    mne_arr, start_time, channels = iom_file.plot_eeg(title=iom_file.f_name, block=True)
    print(f"EEG channels: {len(channels)}")
else:
    print("No EEG data found in this file")
