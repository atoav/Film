# Film
A Wox Plugin for Film related calculations
<br><br>

## Usage
Enter `film` to start the Plugin
<br><br>

### Time Operations
With Time Operations you can calculate different things based on time
You enter `film 120min` and it will output the timecode and the number of frames.
<br><br>

#####Default Behaviour

The input value can be in (most inputs are case insensitive and ignore spaces and tenses (you can enter `Minute` and `Minutes`):
- Frames (`120 f`/`120 Frames`)
- Seconds (`120s`/`120 seconds`/`120sec`)
- Minutes (`120min`/`120 Minutes`/`120mins`)
- Hours (`2.5h`/`2.5 Hours`/`2.5 hr`)
- Days (`0.5d`/`0.5 Days`)
You can specify the Framerate (`120min 24fps` or `120min @30fps`).
<br><br>

#####Bitrate Behaviour

If you specify the Bitrate (`120min 20Mbps`), it will output the resulting filesize for the stream.
It takes the formats: `Gbps`|`Gb/s`|`Gigabit` and `Mbps`|`Mb/s`|`Mbit` and `Kbps`|`Kb/s`|`Kbit` and `MBps`|`MB/s`|`Megabyte` and `GBps`|`GB/s`|`Gigabytes` and `MBpmin`|`MB/min` and `GBpmin`|`GB/min`. The bitrates are "half" caseinsensitive, note that 1 mb and 1mB are not the same unit (Megabit vs Megabyte).
<br><br>

#####Audio Calculations

You can also calculate the file sizes for uncompressed Audio:
`120min 48khz` will output the resulting filesizes for different Bitdepths for Mono and Stereo Files. You can also use the shortcut: `120min 48k`
`120min 24bit` will output the resulting filesizes for different Samplingrates (Default: Stereo). You can also use the shortcut: `120min 24b`
You can additionally specify the number of channes with `Mono`|`Stereo`|`4chn`|`4 channels`

You may specify any combination of the above `120min 48k 24b 4chn`
<br><br><br><br>


## Length Operations
Takes an Input of Film-Length and outputs the runtime for different formats like `120m` or `120ft`.
You may use any of the forms: `m`|`meter`|`meters` or `ft`|`foot`|`feet`. Case insensitive.

You can also specify your own framerate like `120m 16fps` (this defaults to 24fps for Length Operations)
<br><br><br><br>


## Installation
Install the Film Plugin like you would do with any other WOX-Plugin:

1. Download the Plugin
2. Create a Directory called ´Film´ in `Wox/Plugins/`
3. Extract the contents of the downloaded zip into the created Folder `Wox/Plugins/Film
