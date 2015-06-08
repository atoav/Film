from wox import Wox
import re
import datetime
from Tkinter import Tk


class Film(Wox):

    def __init__(self):
        '''
        A list with Tuples that describe film Formats. Int or float is frames per foot
        '''
        self.formats = [("8mm", 80), ("Super8", 72), ("16mm", 40), ("35mm", 16), ("35mm 3-perf", 21.33333333333333333), ("65mm", 12.8)]
        self.bitdepths = [("16 bit", 16), ("24 bit", 24), ("32 bit", 32)]
        self.samplingrates = [("44.1 kHz", 44.1), ("48 kHz", 48), ("88.2 kHz", 88.2), ("96 kHz", 96), ("176.4 kHz", 176.4), ("192 kHz", 192)]
        self.channels = [("Mono", 1), ("Stereo", 2)]
        super(Film, self).__init__()
        

    def query(self, key):
        results = []
        lines = self.parse(key)

        for line in  lines:
            results.append({
            "Title": line.title ,
            "SubTitle": line.subtitle,
            "IcoPath":"Images/app.ico",
            "JsonRPCAction":{
              #You can invoke both your python functions and Wox public APIs .
              #If you want to invoke Wox public API, you should invoke as following format: Wox.xxxx
              #you can get the public name from https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs,
              #just replace xxx with the name provided in this url
              "method": "toclipboard",
              #you MUST pass parater as array
              "parameters":[line.clipboard],
              #hide the query wox or not
              "dontHideAfterAction":False
            }
            })

        return results


    def parse(self, key):
        results = []
        if self.filmlength(key):
            for result in self.filmlength(key):
                results.append(result)
        if self.timeops(key):
            for result in self.timeops(key):
                results.append(result)
        return results

    def spaceops(self, key):
        """
        Takes spaces and calculates the recordinglength
        """
        results = []
        # Default Frame Rate is 25
        fps = 25.0
         # Default Samplingrate for Audio
        khz = 48
        # Default Bitdepth for Audio
        bits = 24
        # Default Number of Audio Channels
        chn = 2

        bitratefound = False
        samplingratefound = False
        bitdepthfound = False
        framerate = False
        channelsfound = False

        # Check if key matches durations
        if not re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(b|Bytes?|kb|Kilobytes?|mb|Megabytes?|Megs?|gb|Gigs?|Gigabytes?|tb|Teras?|Terabytes?)($|\s+)", key, re.IGNORECASE):
            return False

        # Match the unit of the time and retrieve the number
        if re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(b|Bytes?)($|\s+)", key, re.IGNORECASE):
            unit="B"
            b = findfloat(key)
            kb = b/1000.
            mb = b/1000./1000.
            gb = b/1000./1000./1000.
            tb = b/1000./1000./1000./1000.
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(kb|Kilobytes?)($|\s+)", key, re.IGNORECASE):
            unit="KB"
            kb = findfloat(key)
            b = kb*1000.
            mb = kb/1000.
            gb = kb/1000./1000.
            tb = kb/1000./1000./1000.
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(mb|megabytes?|Megs?)($|\s+)", key, re.IGNORECASE):
            unit="MB"
            mb = findfloat(key)
            kb = mb*1000.
            b = mb*1000.*1000.
            gb = mb/1000.
            tb = mb/1000./1000.
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(gb|Gigabytes?|gigs?)($|\s+)", key, re.IGNORECASE):
            unit="GB"
            gb = findfloat(key)
            mb = gb*1000.
            kb = gb*1000.*1000.
            b = gb*1000.*1000.*1000.
            tb = gb/1000.
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(tb|Terr?aBytes?|Terr?as?)($|\s+)", key, re.IGNORECASE):
            unit="TB"
            tb = findfloat(key)
            gb = tb*1000.
            mb = tb*1000.*1000.
            kb = tb*1000.*1000.*1000.
            b = tb*1000.*1000.*1000.*1000.




    def timeops(self, key):
        """
        Takes Time as Input, outputs Frames, Timecode or Filesize if 
        a Bitrate is specified. Example: film 120min
        Possible Arguments:
        """
        results = []

        # Check if a Duration Statement is found in the keystring,
        # else return false
        if not re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(mins?|minutes?|s|secs?|seconds?|hr?|hrs?|hours?|ds?|days?|frames?|f)($|\s+)", key, re.IGNORECASE):
            return False

        # Match the unit of the time and retrieve the number
        if re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(mins?|minutes?)($|\s+)", key, re.IGNORECASE):
            unit="min"
            minutes = findfloat(key)
            seconds = minutes*60.
            hours = minutes/60.0
            days = hours/24.0
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(s|secs?|seconds?)($|\s+)", key, re.IGNORECASE):
            unit="s"
            seconds = findfloat(key)
            minutes = seconds/60.0
            hours = seconds/60.0/60.0
            days = hours/24.0
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(hr?|hrs?|hours?)($|\s+)", key, re.IGNORECASE):
            unit="h"
            hours = findfloat(key)
            minutes = hours*60.
            seconds = hours*60.0*60.0
            days = hours/24.0
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(ds?|days?)($|\s+)", key, re.IGNORECASE):
            unit="d"
            days = findfloat(key)
            hours = days*24.0
            minutes = days*24.0*60.0
            seconds = days*24.0*60.0*60.0
        elif re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(f|frames?)($|\s+)", key, re.IGNORECASE):
            unit="Frames"
            frames = findfloat(key)

        # Filter for all usable Statements, return values
        bitratefound, gigps, megps, gbps, mbps, kbps = filterbitrate(key)
        frameratefound, fps = filterframerate(key)
        samplingratefound, khz = filtersamplingrate(key)
        bitdepthfound, bits = filterbitdepth(key)
        channelsfound, chn = filterchannels(key)

        # Show basic Timecode Calculations
        if unit == "Frames" and (not samplingratefound and not bitdepthfound):
            seconds = frames/fps
            title = "Timecode:\t" + secondstotimecode(seconds, fps) + "\t@" + strfloat(fps) + " fps\t\t=\t"+readabletime(seconds)
            subtitle = ""
            clipboard = secondstotimecode(seconds, fps)
            results.append(Result(title, subtitle, clipboard))

        if not unit == "Frames" and (not samplingratefound and not bitdepthfound):
            title = "Timecode:\t" + secondstotimecode(seconds, fps)+"\t=\t"+readabletime(seconds)
            subtitle = ""
            clipboard = secondstotimecode(seconds, fps)
            results.append(Result(title, subtitle, clipboard))

        # Adds the calculated filesize to the result if a Bitrateformat is given
        if bitratefound and (not samplingratefound and not bitdepthfound):
            # Retrieve the chosen unit
            if bitratefound == "Gbps": ratetext = strfloat(gbps)+" Gb/s"
            if bitratefound == "Mbps": ratetext = strfloat(mbps)+" Mb/s"
            if bitratefound == "Kbps": ratetext = strfloat(kbps)+" Kb/s"
            if bitratefound == "MB/s": ratetext = strfloat(megps)+" MB/s"
            if bitratefound == "GB/s": ratetext = strfloat(gigps)+" GB/s"
            if bitratefound == "MB/min": ratetext = strfloat(megps)+" MB/s"
            if bitratefound == "GB/min": ratetext = strfloat(gigps)+" GB/s"
            filesize = seconds*kbps*1024.
            title = "Filesize:\t\t"+readablesize(filesize)
            subtitle = secondstotimecode(seconds, fps)+" at a Bitrate of "+ratetext
            clipboard = readablesize(filesize)
            results.append(Result(title, subtitle, clipboard))

        # Display Number of Frame for the specified Framerate 
        if not unit == "Frames" and (not samplingratefound and not bitdepthfound):
            frames = round(seconds*fps)
            title = "Frames:\t\t"+strfloat(frames)+" Frames\t\t@"+strfloat(fps)+" fps"
            subtitle = ""
            clipboard = int(frames)
            results.append(Result(title, subtitle, clipboard))

        if samplingratefound or bitdepthfound:
            # When no bitdepth is set, list all bitdepths for Mono and Stereo
            if not bitdepthfound and not channelsfound:
                for c in self.channels:
                    for bd in self.bitdepths:
                        bps = khz*1000*bd[1]/8.
                        size = bps*seconds*c[1]
                        title = c[0]+"\t\t"+bd[0]+"\tFilesize:\t"+readablesize(size)
                        subtitle = "Samplingrate:\t"+strfloat(khz)+" kHz"
                        clipboard = readablesize(size)
                        results.append(Result(title, subtitle, clipboard))

            # When no Samplingrate is set output Filesizes for Samplingrates and Stereo
            if not samplingratefound and not channelsfound:
                for smp in self.samplingrates:
                    bds = smp[1]*1000*bits/8.
                    size = bds*seconds*chn
                    if len(smp[0])>8:
                        spaces = "\t\t"
                    else:
                        spaces = "\t\t\t"
                    title = smp[0]+spaces+"Filesize:\t\t"+readablesize(size)
                    subtitle = strfloat(bits)+" bit,\tChannels:  "+str(chn)
                    clipboard = readablesize(size)
                    results.append(Result(title, subtitle, clipboard))

            if bitdepthfound and samplingratefound and not channelsfound:
                for c in self.channels:
                    bps = khz*1000*bits/8.
                    size = bps*seconds*c[1]
                    title = c[0]+"\t\t\t\tFilesize:\t\t"+readablesize(size)
                    subtitle = ""
                    clipboard = readablesize(size)
                    results.append(Result(title, subtitle, clipboard))

            # If Bitrate and Channel is specified
            if bitdepthfound and channelsfound and not samplingratefound :
                for smp in self.samplingrates:
                    bds = smp[1]*1000*bits/8.
                    size = bds*seconds*chn
                    if len(smp[0])>8:
                        spaces = "\t\t"
                    else:
                        spaces = "\t\t\t"
                    title = smp[0]+spaces+"Filesize:\t\t"+readablesize(size)
                    subtitle = strfloat(bits)+" bit,\tChannels:  "+str(chn)
                    clipboard = readablesize(size)
                    results.append(Result(title, subtitle, clipboard))

            # If Samplingrate and Channel is specified
            if samplingratefound and channelsfound and not bitdepthfound:
                for bd in self.bitdepths:
                    bps = khz*1000*bd[1]/8.
                    size = bps*seconds*chn
                    if chn == 1:
                        chnstring = "Mono"
                    elif chn == 2:
                        chnstring = "Stereo"
                    else:
                        chnstring = str(chn)+" Channels"
                    title = bd[0]+":\t\t\t"+chnstring+"\t\tFilesize:\t"+readablesize(size)
                    subtitle = "Samplingrate:\t"+strfloat(khz)+" kHz"
                    clipboard = readablesize(size)
                    results.append(Result(title, subtitle, clipboard))


            # If everything (Samplingrate, Bitrate, Channels) is specified:
            if bitdepthfound and samplingratefound and channelsfound:
                bps = khz*1000*bits/8.
                size = bps*seconds*chn
                title = "Uncompressed Audio Filesize:\t\t"+readablesize(size)
                subtitle = ""
                clipboard = readablesize(size)
                results.append(Result(title, subtitle, clipboard))

        return results


    def filmlength(self, key):
        # Checks if the key starts with a length (ft or m)
        # outputs runningtime for different formats
        results = []
        # Default Frame Rate for film is 24
        fps = 24.0    
        
        # Check if key matches the film-length (case insensitive)
        if not re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(m|meters?|ft|feet|foot)($|\s+)", key, re.IGNORECASE):
            return False

        # Check for units and calculate the missing unit
        if re.match(r"^(\s+)?(\d+|\d+[\.,]\d+)(\s+)?(m|meters?)($|\s+)", key, re.IGNORECASE):
            unit = "m"
            meters = findfloat(key)
            feet = meters*3.2808399
        else:
            unit = "ft"
            feet = findfloat(key)
            meters = feet/3.2808399

        frameratefound, fps = filterframerate(key)

        # Output a Result for each Format
        for format in self.formats:
            title = self.createtitle(format[0], format[1], feet, fps)
            subtitle = strfloat(meters) + " Meters (" + strfloat(feet) + " Feet) with " + strfloat(format[1])+" Frames per Foot"
            # Compose a text for clipboard
            clipboard = format[0]+" @"+strfloat(fps)+": "+str(self.calcruntime(feet, format[1], fps))+" seconds, " +secondstotimecode(self.calcruntime(feet, format[1], fps), fps)
            results.append(Result(title, subtitle, clipboard))
        return results


    def createtitle(self, name, factor, feet, fps):
        seconds = self.calcruntime(feet, factor, fps)
        timecode = secondstotimecode(seconds)
        if name == "35mm 3-perf":
            spaces = "\t"
        else:
            spaces = "\t\t"
        return name  + " @" + strfloat(fps) + "fps"+spaces+"=\t" + timecode + " (" + strfloat(seconds) + "s) \t=\t"+str(int(feet*factor))+" Frames"


    def calcruntime(self, feet, factor, fps=24):
        return feet*factor/float(fps)


    def toclipboard(self, content):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(content)
        r.destroy()


def readablesize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


""" Little Helpers """

def findfloat(key):
    # Pattern for float or integer
    refloat = re.compile(r"(\d+[\.,](\d+)?)|\d+")
   
    return float(refloat.search(key).group().replace(",","."))


def secondstotimecode(s, fps=25):
    remainderframes = s%fps
    return (str(datetime.timedelta(seconds=s)).split('.', 2)[0])+"."+str(int(remainderframes))


def strfloat(value):
    value = float(value)
    if value.is_integer():
        return str(int(value))
    else:
        return "%.2f" % value


def filterbitrate(key):
    # Filters a key string in order to find specified bitrates/datarates
    # returns all units
    gigps = False
    megps = False
    gbps = False
    mbps = False
    kbps = False
    bitratefound = False
    # Regexes for different Bitrate units (like @60Mbit or @ 60 MB/s and such)
    regbit = "[Gg]bps|[Gg]b(\s+)?/(\s+)?s|[Gg][Bb][Ii][Tt][Ss]?"
    rembit = "[Mm]bps|[Mm]b(\s+)?/(\s+)?s|[Mm][Bb][Ii][Tt][Ss]?"
    rekbit = "[Kk]bps|[Kk]b(\s+)?/(\s+)?s|[Kk][Bb][Ii][Tt][Ss]?"
    reMB =   "[Mm]Bps|[Mm]B(\s+)?/(\s+)?s|[Mm][Ee][Gg][Aa][Bb][Yy][Tt][Ee][Ss]?"
    reGB =   "[Gg]Bps|[Gg]B(\s+)?/(\s+)?s|[Gg][Ii][Gg][Aa][Bb][Yy][Tt][Ee][Ss]"
    reMBmin ="[Mm]Bpmin|[Mm]B(\s+)?/(\s+)?min"
    reGBmin ="[Gg]Bpmin|[Gg]B(\s+)?/(\s+)?min"
    rebitrate = re.compile("(\s+)?@?(\s+)?(\d+|\d+[\.,]\d+)(\s+)?("+regbit+"|"+rembit+"|"+rekbit+"|"+reMB+"|"+reGB+"|"+reMBmin+"|"+reGBmin+")")
    # Filter the key
    if rebitrate.search(key):
        match = rebitrate.search(key).group()
        # Retrieve the Numbers
        if re.search("(\d+|\d+[\.,]\d+)("+regbit+")", match):
            bitratefound = "Gbps"
            gbps = findfloat(match)
            mbps = gbps*1000.
            kbps = gbps*1000.*1000.
            gigps = gbps*8.
            megps = mbps*8.
        elif re.search("(\d+|\d+[\.,]\d+)("+rembit+")", match):
            bitratefound = "Mbps"
            mbps = findfloat(match)
            gbps = mbps/1000.
            kbps = mbps*1000.
            gigps = gbps*8.
            megps = mbps*8.
        elif re.search("(\d+|\d+[\.,]\d+)("+rekbit+")", match):
            bitratefound = "Kbps"
            kbps = findfloat(match)
            mbps = kbps/1000.
            gbps = kbps/1000./1000.
            gigps = gbps*8.
            megps = mbps*8.
        elif re.search("(\d+|\d+[\.,]\d+)("+reMB+")", match):
            bitratefound = "MB/s"
            megps = findfloat(match)
            gigps = megps/1000.
            mbps = megps/8.
            gbps = mbps/1000.
            kbps = mbps*1000.
        elif re.search("(\d+|\d+[\.,]\d+)("+reGB+")", match):
            bitratefound = "GB/s"
            gigps = findfloat(match)
            megps = gigps*1000. 
            mbps = megps/8.
            gbps = mbps/1000.
            kbps = mbps*1000.
        elif re.search("(\d+|\d+[\.,]\d+)("+reMBmin+")", match):
            bitratefound = "MB/min"
            megps = findfloat(match)/60.
            gigps = megps/1000.
            mbps = megps/8.
            gbps = mbps/1000.
            kbps = mbps*1000.
        elif re.search("(\d+|\d+[\.,]\d+)("+reGBmin+")", match):
            bitratefound = "GB/min"
            gigps = findfloat(match)/60.
            megps = gigps*1000. 
            mbps = megps/8.
            gbps = mbps/1000.
            kbps = mbps*1000.
        # Return GB/s, MB/s, Gbps, Mbps, kbps and Selection (bitratefound)
    return bitratefound, gigps, megps, gbps, mbps, kbps

def calcmissingrates(rate, unit):
    # Unit with corresponding conversion factor
    units = {"GB/min" : 8589934592*60, "MB/min" : 503316480, "GB/s" : 8589934592, "MB/s" : 8388608, "Gbps" : 1000000000, "Mbps" : 1000000, "Kbps" : 1000, "Bps" : 1}
    # Multiply rate by conversion factor to get the Bits per Second
    bps = rate * units[unit]
    missingunits = units.copy()
    if (units[unit] in missingunits): del missingunits[exclude]
    for u in missingunits:
        pass




def filterframerate(key, fps=25.0):
    # Filters a key string for a specified framerate
    # outputs a boolean and a float
    # Check for Framerate
    frameratefound = False
    refps = re.compile(r"(\s+)?@?(\s+)?((\d+[\.,](\d+)?)|\d+)(\s+)?(fps)", re.IGNORECASE)
    if refps.search(key):
        match = refps.search(key).group()
        fps = findfloat(match)
        frameratefound = True
    return frameratefound, fps


def filtersamplingrate(key, khz=48.):
    # Check for AUDIO Samplingrate (eg. @48k or @44.1Hkz)
    samplingratefound = False
    resamp = re.compile(r"(\s+)?@?(\s+)?((\d+[\.,](\d+)?)|\d+)(\s+)?(k($|\s+)|khz)", re.IGNORECASE)
    if resamp.search(key):
        match = resamp.search(key).group()
        khz = findfloat(match)
        samplingratefound = True
    return samplingratefound, khz


def filterbitdepth(key, bits=24.):
    # Check for AUDIO Bitdepth (eg. @24b or @ 32 bits)
    bitdepthfound = False
    rebits = re.compile(r"(\s+)?@?(\s+)?\d+(\s+)?(b|bits?)", re.IGNORECASE)
    if rebits.search(key):
        match = rebits.search(key).group()
        bits = findfloat(match)
        bitdepthfound = True
    return bitdepthfound, bits


def filterchannels(key, chn=2):
    # Check for AUDIO Channels (eg. Mono, Stereo, 2chn or 6 Channels)
    channelsfound = False
    rechns = re.compile(r"(\s+)?((Mono|Stereo)|\d+(\s+)?(c|chn?|channels?))", re.IGNORECASE)
    if rechns.search(key):
        match = rechns.search(key).group()
        if re.search("mono", match, re.IGNORECASE):
            chn = 1
        elif re.search("stereo", match, re.IGNORECASE):
            chn = 2
        else:
            chn = int(re.search("\d+", match).group())
        channelsfound = True
    return channelsfound, chn


def readabletime(amount, units = 'Seconds'):    
    def process_time(amount, units):
        INTERVALS = [   1, 60, 
                        60*60, 
                        60*60*24, 
                        60*60*24*7, 
                        60*60*24*7*4, 
                        60*60*24*7*4*12, 
                        60*60*24*7*4*12*100,
                        60*60*24*7*4*12*100*10]
        NAMES = [('Second', 'Seconds'),
                 ('Minute', 'Minutes'),
                 ('Hour', 'Hours'),
                 ('Day', 'Days'),
                 ('Week', 'Weeks'),
                 ('Month', 'Months'),
                 ('Year', 'Years'),
                 ('Century', 'Centuries'),
                 ('Millennium', 'Millennia')]

        result = []

        unit = map(lambda a: a[1], NAMES).index(units)
        # Convert to seconds
        amount = amount * INTERVALS[unit]

        for i in range(len(NAMES)-1, -1, -1):
            a = amount // INTERVALS[i]
            if a > 0: 
                result.append( (a, NAMES[i][1 % a]) )
                amount -= a * INTERVALS[i]
        return result

    rd = process_time(int(amount), units)
    cont = 0
    for u in rd:
        if u[0] > 0:
            cont += 1

    buf = ''
    i = 0
    for u in rd:
        if u[0] > 0:
            buf += "%d %s" % (u[0], u[1])
            cont -= 1

        if i < (len(rd)-1):
            if cont > 1:
                buf += ", "
            else:
                buf += " and "

        i += 1
    return buf


class Result():
    def __init__(self, title, subtitle="", clipboard=""):
        self.title = title
        self.subtitle = subtitle
        self.clipboard = clipboard



#Following statement is necessary
if __name__ == "__main__":
    Film()