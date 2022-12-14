from pytube import YouTube
from pathlib import Path
import os
import sys

path_to_folder = str(os.path.join(Path.home(), "Videos"))
if not os.path.exists(path_to_folder + "/Downloaded YouTube stuff"):
    os.makedirs(path_to_folder + "/Downloaded YouTube stuff/Video")
    os.makedirs(path_to_folder + "/Downloaded YouTube stuff/Audio")

path_to_folder = path_to_folder + "/Downloaded YouTube stuff"

download_types = ['video', 'audio']
#download_resolutions = ["highest", "720p", "480p", "360p", "240p", "144p"]
download_resolutions = ["highest", "720p", "360p"]

base_select_message = "Your choice: "
multiple_files = ''
user_input = ''
selected_resolution = ''
selected_type = ''
link = ''
links = []


def SetupDownload(multiple_files, link, links, type, resolution):
    if multiple_files:
        for single_link in links:
            Download(single_link, type, resolution)
    else:
        Download(link, type, resolution)

    print("Program finished (;")


def Download(link, type, resolution):
    yt = YouTube(link)

    print(yt.streams[0].title)

    if type == 'audio':
        yt = yt.streams.get_audio_only()
        try:
            out_file = yt.download(
                output_path=path_to_folder + "/Audio")
            print("Download Succes")
        except:
            print("Connection Error")

        base = os.path.splitext(out_file)
        new_file = base[0] + '.mp3'
        os.rename(out_file, new_file)

    elif type == 'video':
        if resolution == "highest":
            yt = yt.streams.filter(
                file_extension='mp4').get_highest_resolution()
        else:
            yt = yt.streams.filter(
                file_extension="mp4").get_by_resolution(resolution)

        try:
            out_file = yt.download(
                output_path=path_to_folder + "/Video")
            print("Download Succes")
        except:
            print("Not Found")


# Let user choose amount of downloads
while multiple_files not in [True, False]:
    multiple_files = input("Download multiple files? (y/n): ").lower()
    if multiple_files == "y":
        multiple_files = True
    elif multiple_files == "n":
        multiple_files = False

# Get video link
if multiple_files == True:
    while link != 'd':
        link = ''
        link = input("Enter video link (if done type (d)): ")
        if link != "d":
            links.append(link)
else:
    link = input("Enter video link: ")

# Let user choose between download types
input_message_downloadtype = "Pick a type:\n"
for index, item in enumerate(download_types):
    input_message_downloadtype += f'{index+1}) {item}\n'
input_message_downloadtype += base_select_message

while user_input not in map(str, range(1, len(download_types) + 1)):
    user_input = input(input_message_downloadtype)
selected_type = download_types[int(user_input) - 1]

# Let chooser choose between resolutions (video only)
if selected_type == "video":
    user_input = ''
    input_message_resolution = "Pick a resolution:\n"
    for index, item in enumerate(download_resolutions):
        input_message_resolution += f'{index+1}) {item}\n'

    input_message_resolution += base_select_message

    while user_input not in map(str, range(1, len(download_resolutions) + 1)):
        user_input = input(input_message_resolution)
    selected_resolution = download_resolutions[int(user_input) - 1]

# Download content from link
SetupDownload(multiple_files, link, links, selected_type, selected_resolution)

os.execl(sys.executable, sys.executable, *sys.argv)
