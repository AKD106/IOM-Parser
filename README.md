# IOM File Reader and Plotter

A Python library for reading, processing, and visualizing IOM (Intraoperative Monitoring) data files containing EEG, ECoG, stimulation data, and event logs.

## Features

- Read HDF5-formatted IOM files
- Parse EEG and ECoG data with timestamps
- Handle stimulation amplitude and duration data
- Process event logs with automatic timezone detection (EST/EDT)
- Visualize data using MNE-Python interactive plots
- Support for multiple EEG recording segments with automatic joining

## Installation

### Required Dependencies

```bash
pip install numpy pandas h5py mne
```

## Usage

### Basic Usage

```python
import iom

# Load an IOM file
file_path = r"C:\path\to\your\file.h5"
iom_file = iom.IOM_file(file_path)

# Read and format the data
iom_file.read_data(format=True)

# Plot EEG data
if iom_file.is_eeg_present:
    mne_arr, start_time, channels = iom_file.plot_eeg(title=iom_file.f_name)
```

### Advanced Usage

#### Plot Specific EEG Segment

```python
# Plot a specific EEG recording segment by index
mne_arr, start_time, channels = iom_file.plot_eeg(
    title="EEG Segment 0", 
    block=True, 
    idx=0
)
```

#### Plot ECoG Data

```python
if iom_file.is_ecog_present:
    iom_file.plot_ecog()
```

#### Access Raw Data

```python
# EEG data
eeg_data = iom_file.eeg_data  # List of numpy arrays
eeg_channels = iom_file.eeg_channels  # Channel names
eeg_timestamps = iom_file.eeg_timestamps  # Timestamps for each segment

# ECoG data
ecog_data = iom_file.ecog_data  # Numpy array
ecog_channels = iom_file.ecog_channels  # Channel names
ecog_timestamps = iom_file.ecog_timestamps  # Timestamps

# Event log
log_df = iom_file.log  # Pandas DataFrame with 'Time' and 'Comment' columns

# Stimulation data
stim_amp = iom_file.stim_amp  # Stimulation amplitudes
stim_duration = iom_file.stim_duration  # Stimulation durations
```

## Class: IOM_file

### Attributes

- `path` (str): Path to the IOM file
- `is_ecog_present` (bool): Whether ECoG data is available
- `is_eeg_present` (bool): Whether EEG data is available
- `offset_hours` (int): Timezone offset (4 for EDT, 5 for EST)
- `eeg_fs` (int): EEG sampling frequency (default: 500 Hz)
- `eeg_data` (list): List of EEG data arrays
- `eeg_channels` (list): EEG channel names
- `eeg_timestamps` (list): EEG timestamps
- `ecog_data` (numpy.ndarray): ECoG data array
- `ecog_channels` (list): ECoG channel names
- `ecog_timestamps` (list): ECoG timestamps
- `stim_amp` (numpy.ndarray): Stimulation amplitude data
- `stim_duration` (list): Stimulation duration data
- `log` (pandas.DataFrame): Event log with times and comments
- `f_name` (str): Extracted file name from path

### Methods

#### `read_data(format=True)`
Reads all data from the HDF5 file.

**Parameters:**
- `format` (bool): Whether to format the data after reading (default: True)

#### `format_data()`
Formats raw data into usable structures (timestamps, channel names, etc.)

#### `get_timezone_offset(dt)`
Determines if a datetime is in EST or EDT.

**Parameters:**
- `dt` (datetime): DateTime object to check

**Returns:**
- `int`: 4 for EDT (March-October), 5 for EST (November-February)

#### `set_events(sig)`
Adds event annotations from log to MNE Raw object.

**Parameters:**
- `sig` (mne.io.Raw): MNE Raw object

**Returns:**
- `mne.io.Raw`: Raw object with annotations added

#### `plot_eeg(title, block=True, idx=False)`
Plots EEG data using MNE visualization.

**Parameters:**
- `title` (str): Plot window title
- `block` (bool): Whether to block execution until plot is closed (default: True)
- `idx` (int or False): Index of specific segment to plot, or False to plot all joined segments

**Returns:**
- `tuple`: (mne_arr, start_time, channels)

#### `plot_ecog()`
Plots ECoG data using MNE visualization.

#### `join_eeg_timestamps()`
Joins multiple EEG recording segments into a single continuous array.

**Returns:**
- `tuple`: (full_eeg_data, start_time)

#### `fix_channels(eeg_data)`
Reorders channels, placing ECoG channels (e.g., Fz1-8, M1-8) first.

**Parameters:**
- `eeg_data` (numpy.ndarray): EEG data array

**Returns:**
- `tuple`: (reordered_data, reordered_channel_names)

## Timezone Handling

The library automatically detects and applies the correct timezone offset:
- **EDT (UTC-4)**: March through October
- **EST (UTC-5)**: November through February

This ensures event logs are correctly aligned with signal data regardless of when the recording took place.

## File Format

The library expects HDF5 files with the following structure:

```
/eeg_data/          - EEG signal data
/eeg_timestamp/     - EEG timestamps
/channel_names      - Channel name array
/ecog_data          - ECoG signal data
/ecog_channels      - ECoG channel names
/ecog_timestamp     - ECoG timestamps
/stim_amp_data      - Stimulation amplitude data
/stim_duration      - Stimulation duration data
/log                - Event log (comment, timestamp pairs)
```

## Example: Complete Workflow

```python
import iom

# Initialize
file_path = r"C:\data\IOM_ABC_123456.h5"
iom_file = iom.IOM_file(file_path)

# Read data
iom_file.read_data(format=True)

# Check what data is available
print(f"EEG Present: {iom_file.is_eeg_present}")
print(f"ECoG Present: {iom_file.is_ecog_present}")
print(f"Number of log entries: {len(iom_file.log)}")

# Plot EEG with events
if iom_file.is_eeg_present:
    print(f"Timezone offset: {iom_file.offset_hours} hours")
    mne_arr, start_time, channels = iom_file.plot_eeg(
        title=iom_file.f_name,
        block=True
    )
    print(f"Channels: {channels}")
```

