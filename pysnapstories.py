import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import sys
import os
import time
import re
import shutil
import warnings

try:
    import urllib.request as urllib
except ImportError:
    import urllib as urllib

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
sep = "-" * 95
script_version = "2.1"
python_version = sys.version.split(' ')[0]
request_headers = {
    'authority': 'search.snapchat.com',
    'sec-ch-ua': '"Google Chrome 79"',
    'origin': 'https://story.snapchat.com',
    'sec-fetch-dest': 'empty',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'referer': 'https://story.snapchat.com/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'nl-NL,nl;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6'
}

story_endpoints = {
    "mapStory": "https://storysharing.snapchat.com/v1/fetch/{}",
    "userStory": "https://search.snapchat.com/lookupStory?id={}",
    "subjectStory": "https://search.snapchat.com/lookupStory?id={}"
}

story_type = ""

story_endpoint_final = ""
warnings.filterwarnings("ignore", category=DeprecationWarning)


def start():
    global story_endpoint_final
    log_seperator()
    log_info_blue('PYSNAPSTORIES (SCRIPT V{:s} - PYTHON V{:s}) - {:s}'.format(
        script_version, python_version, time.strftime('%I:%M:%S %p')))
    log_seperator()

    is_not_username = False
    if not len(sys.argv) > 1:
        log_warn("No input given. The script will now exit.")
        log_seperator()
        exit(1)
    given_input = sys.argv[1].replace("/", "")
    try:
        if given_input.startswith("p:"):
            is_not_username = True
            log_info_blue("Treating input as multiple map story.")
            story_endpoint_final = story_endpoints.get("mapStory")
            story_type = "MAPMULTI"
        elif given_input.startswith("m:"):
            is_not_username = True
            log_info_blue("Treating input as single map story.")
            story_endpoint_final = story_endpoints.get("mapStory")
            story_type = "MAPSINGLE"
        elif given_input.startswith("c:"):
            is_not_username = True
            log_info_blue("Treating input as subject story.")
            story_endpoint_final = story_endpoints.get("subjectStory")
            story_type = "SUBJECT"
        else:
            log_info_blue("Treating input as username. (no ID was detected)")
            story_endpoint_final = story_endpoints.get("userStory")
            story_type = "USERNAME"
    except IndexError:
        log_error("No input was given, exiting.")
        log_seperator()
        exit(1)

    if story_type == "MAPMULTI":
        log_info_green(
            "Starting download for multiple map story ID: \033[93m{:s}".format(given_input))
        download_map_stories(given_input)
    elif story_type == "MAPSINGLE":
        log_info_green(
            "Starting download for single map story ID: \033[93m{:s}".format(given_input))
        download_map_stories(given_input)
    elif story_type == "SUBJECT":
        log_info_green(
            "Starting download for subject story ID: \033[93m{:s}".format(given_input))
        download_subject_stories(given_input)
    elif story_type == "USERNAME":
        log_info_green(
            "Starting download for user: \033[93m{:s}".format(given_input))
        download_user_stories(given_input)


def download_subject_stories(snapchat_story_id):
    try:
        response = requests.get(story_endpoint_final.format(
            snapchat_story_id), verify=True, headers=request_headers)
        try:
            response_json = json.loads(response.text)
        except ValueError:
            log_seperator()
            log_error("The given username did not return any stories.")
            log_error("The script cannot continue, exiting.")
            log_seperator()
            exit(1)

        stories_image = 0
        stories_video = 0

        snapchat_story_id = slugify(sys.argv[1])
        snapchat_story_name = slugify(
            response_json.get("storyTitle", "NoTitle"))

        download_path = os.getcwd() + \
            "/snapchat/{}/".format('{:s}_{:s}'.format(snapchat_story_id,
                                                      snapchat_story_name))
        download_path_overlay = os.path.join(download_path, "overlay")

        if not os.path.exists(download_path_overlay):
            os.makedirs(download_path_overlay)

        if check_directories('{:s}_{:s}'.format(snapchat_story_id, snapchat_story_name)):
            if response_json.get("snapList"):
                log_seperator()
                log_info_blue("Story Id     : {:s}".format(
                    snapchat_story_id if snapchat_story_id != "NoId" else "Not available"))
                log_info_blue("Story Title  : {:s}".format(
                    snapchat_story_name if snapchat_story_name != "NoTitle" else "Not available"))
                log_info_blue("Story amount : {:d}".format(
                    len(response_json.get("snapList"))))
                log_seperator()
                for index, snap in enumerate(response_json.get("snapList")):
                    media_url = snap.get("snapUrls").get("mediaUrl")
                    media_overlay_url = snap.get("snapUrls").get("overlayUrl")
                    media_type = "VIDEO" if ".mp4" in media_url else "IMAGE"
                    media_ts = snap.get("timestampInSec")
                    media_id = snap.get("snapId")

                    downloaded_in_iteration = False

                    if "VIDEO" in media_type:
                        if media_overlay_url:
                            download_path_with_file = os.path.join(
                                download_path_overlay, "{:s}_{:d}_overlay.png".format(media_id, media_ts))
                            download_result = download_story(
                                media_overlay_url, download_path_with_file)
                            if download_result == "Error":
                                pass
                            elif download_result == True:
                                log_info_green("Grabbed other: \033[92m{:s}\033[0m".format(
                                    "{:s}_overlay.png".format(media_id)))
                            else:
                                log_info_blue("Skipped other: \033[92m{:s}\033[0m".format(
                                    "{:s}_overlay.png".format(media_id)))

                        download_path_with_file = os.path.join(
                            download_path, "{:s}_{:d}_media.mp4".format(media_id, media_ts))
                        download_result = download_story(media_url.replace(
                            "overlay", "media"), download_path_with_file)
                        if download_result == "Error":
                            pass
                        elif download_result == True:
                            downloaded_in_iteration = True
                            stories_video += 1
                            log_info_green("Grabbed video: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("snapList"))))
                        else:
                            log_info_blue("Skipped video: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("snapList"))))

                    if "IMAGE" in media_type:
                        download_path_with_file = os.path.join(
                            download_path, "{:s}_{:d}_media.jpg".format(media_id, media_ts))
                        download_result = download_story(
                            media_url, download_path_with_file)
                        if download_result == "Error":
                            pass
                        elif download_result == True:
                            downloaded_in_iteration = True
                            stories_image += 1
                            log_info_green("Grabbed image: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("snapList"))))
                        else:
                            log_info_blue("Skipped image: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("snapList"))))

                log_seperator()
                if stories_image and stories_video:
                    log_info_green("Finished downloading {:d} image(s) and {:d} video(s).".format(
                        stories_image, stories_video))
                elif stories_image:
                    log_info_green(
                        "Finished downloading {:d} image(s).".format(stories_image))
                elif stories_video:
                    log_info_green(
                        "Finished downloading {:d} video(s).".format(stories_video))

                else:
                    log_info_green("No new stories have been downloaded.".format(
                        stories_image, stories_video))
                log_seperator()
            else:
                log_seperator()
                log_warn("There are no stories available to download.")
                shutil.rmtree(download_path)
                log_seperator()
                exit(2)
        else:
            log_seperator()
            log_error(
                "Could not make required directories. Ensure you have write permissions.")
            log_error("The script cannot continue, exiting.")
            exit(1)
    except Exception as e:
        log_seperator()
        log_error("Something went wrong: {:s}".format(str(e)))
        log_error("The script cannot continue, exiting.")
        exit(1)



####
# Currently not working for certain usernames
####

def download_user_stories(snapchat_story_id):
    download_subject_stories(snapchat_story_id)

# def download_user_stories(snapchat_story_id):
#     try:

#         response = requests.get(story_endpoint_final.format(snapchat_story_id), verify=True, headers=request_headers)

#         if "rpc error" in response.text:
#             log_seperator()
#             log_error("The given ID did not return any stories.")
#             log_error("The script cannot continue, exiting.")
#             log_seperator()
#             exit(1)
#         else:
#             response_json = json.loads(response.text)

#         stories_image = 0
#         stories_video = 0

#         snapchat_story_id = slugify(
#             response_json.get("story").get("id", "NoId"))
#         snapchat_story_name = slugify(response_json.get(
#             "story").get("metadata").get("title", "NoTitle"))

#         download_path = os.getcwd() + \
#             "/snapchat/{}/".format('{:s}_{:s}'.format(snapchat_story_id,
#                                                       snapchat_story_name))
#         download_path_embedded = os.path.join(download_path, "embedded")

#         if not os.path.exists(download_path_embedded):
#             os.makedirs(download_path_embedded)

#         if check_directories('{:s}_{:s}'.format(snapchat_story_id, snapchat_story_name)):
#             if response_json.get("story").get("snaps"):
#                 log_seperator()
#                 log_info_blue("Story Id     : {:s}".format(
#                     snapchat_story_id if snapchat_story_id != "NoId" else "Not available"))
#                 log_info_blue("Story Title  : {:s}".format(
#                     snapchat_story_name if snapchat_story_name != "NoTitle" else "Not available"))
#                 log_info_blue("Story amount : {:d}".format(
#                     len(response_json.get("story").get("snaps"))))
#                 log_seperator()
#                 for index, snap in enumerate(response_json.get("story").get("snaps")):
#                     media_type = snap.get("media").get("type")
#                     media_url = snap.get("media").get("mediaUrl")
#                     media_ts = int(snap.get("captureTimeSecs"))
#                     media_id = snap.get("id")

#                     is_embedded = media_url.endswith("embedded.mp4")
#                     downloaded_in_iteration = False

#                     if "VIDEO" in media_type:
#                         if is_embedded:
#                             download_path_with_file = os.path.join(
#                                 download_path_embedded, "{:s}_{:d}_embedded.mp4".format(media_id, media_ts))
#                             download_result = download_story(
#                                 media_url, download_path_with_file)

#                         download_path_with_file = os.path.join(
#                             download_path, "{:s}_{:d}_media.mp4".format(media_id, media_ts))
#                         download_result = download_story(media_url.replace(
#                             "embedded", "media"), download_path_with_file)
#                         if download_result == "Error":
#                             pass
#                         elif download_result == True:
#                             downloaded_in_iteration = True
#                             stories_video += 1
#                             log_info_green("Grabbed video: \033[93m{:s}\033[0m ({:d}/{:d})".format(
#                                 download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))
#                         else:
#                             log_info_blue("Skipped video: \033[93m{:s}\033[0m ({:d}/{:d})".format(
#                                 download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))

#                     if "IMAGE" in media_type:
#                         download_path_with_file = os.path.join(
#                             download_path, "{:s}_{:d}_media.jpg".format(media_id, media_ts))
#                         download_result = download_story(
#                             media_url, download_path_with_file)
#                         if download_result == "Error":
#                             pass
#                         elif download_result == True:
#                             downloaded_in_iteration = True
#                             stories_image += 1
#                             log_info_green("Grabbed image: \033[93m{:s}\033[0m ({:d}/{:d})".format(
#                                 download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))
#                         else:
#                             log_info_blue("Skipped image: \033[93m{:s}\033[0m ({:d}/{:d})".format(
#                                 download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))

#                 log_seperator()
#                 if stories_image and stories_video:
#                     log_info_green("Finished downloading {:d} image(s) and {:d} video(s). (Excluding embedded files)".format(
#                         stories_image, stories_video))
#                 elif stories_image:
#                     log_info_green(
#                         "Finished downloading {:d} image(s). (Excluding embedded files)".format(stories_image))
#                 elif stories_video:
#                     log_info_green(
#                         "Finished downloading {:d} video(s). (Excluding embedded files)".format(stories_video))

#                 else:
#                     log_info_green("No new stories have been downloaded. (Excluding embedded files)".format(
#                         stories_image, stories_video))
#                 log_seperator()
#             else:
#                 log_seperator()
#                 log_warn("There are no stories available to download.")
#                 shutil.rmtree(download_path)
#                 log_seperator()
#                 exit(2)
#         else:
#             log_error(
#                 "Could not make required directories. Ensure you have write permissions.")
#             log_error("The script cannot continue, exiting.")
#             exit(1)
#     except Exception as e:
#         log_error("Something went wrong: {:s}".format(str(e)))
#         log_error("The script cannot continue, exiting.")
#         exit(1)


def download_map_stories(snapchat_story_id):
    try:

        response = requests.get(story_endpoint_final.format(snapchat_story_id), verify=True, headers={
            "User-Agent": request_headers["User-Agent"]
        })

        if "rpc error: code = NotFound desc = Not found." in response.text:
            log_seperator()
            log_error("The given ID did not return any stories.")
            log_error("The script cannot continue, exiting.")
            log_seperator()
            exit(1)
        else:
            response_json = json.loads(response.text)

        stories_image = 0
        stories_video = 0

        snapchat_story_id = slugify(
            response_json.get("story").get("id", "NoId"))
        snapchat_story_name = slugify(response_json.get(
            "story").get("metadata").get("title", "NoTitle"))

        download_path = os.getcwd() + \
            "/snapchat/{}/".format('{:s}_{:s}'.format(snapchat_story_id,
                                                      snapchat_story_name))
        download_path_embedded = os.path.join(download_path, "embedded")

        if not os.path.exists(download_path_embedded):
            os.makedirs(download_path_embedded)

        if check_directories('{:s}_{:s}'.format(snapchat_story_id, snapchat_story_name)):
            if response_json.get("story").get("snaps"):
                log_seperator()
                log_info_blue("Story Id     : {:s}".format(
                    snapchat_story_id if snapchat_story_id != "NoId" else "Not available"))
                log_info_blue("Story Title  : {:s}".format(
                    snapchat_story_name if snapchat_story_name != "NoTitle" else "Not available"))
                log_info_blue("Story amount : {:d}".format(
                    len(response_json.get("story").get("snaps"))))
                log_seperator()
                for index, snap in enumerate(response_json.get("story").get("snaps")):
                    media_type = snap.get("media").get("type")
                    media_url = snap.get("media").get("mediaUrl")
                    media_ts = int(snap.get("captureTimeSecs"))
                    media_id = snap.get("id")

                    is_embedded = media_url.endswith("embedded.mp4")
                    downloaded_in_iteration = False

                    if "VIDEO" in media_type:
                        if is_embedded:
                            download_path_with_file = os.path.join(
                                download_path_embedded, "{:s}_{:d}_embedded.mp4".format(media_id, media_ts))
                            download_result = download_story(
                                media_url, download_path_with_file)

                        download_path_with_file = os.path.join(
                            download_path, "{:s}_{:d}_media.mp4".format(media_id, media_ts))
                        download_result = download_story(media_url.replace(
                            "embedded", "media"), download_path_with_file)
                        if download_result == "Error":
                            pass
                        elif download_result == True:
                            downloaded_in_iteration = True
                            stories_video += 1
                            log_info_green("Grabbed video: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))
                        else:
                            log_info_blue("Skipped video: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))

                    if "IMAGE" in media_type:
                        download_path_with_file = os.path.join(
                            download_path, "{:s}_{:d}_media.jpg".format(media_id, media_ts))
                        download_result = download_story(
                            media_url, download_path_with_file)
                        if download_result == "Error":
                            pass
                        elif download_result == True:
                            downloaded_in_iteration = True
                            stories_image += 1
                            log_info_green("Grabbed image: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))
                        else:
                            log_info_blue("Skipped image: \033[93m{:s}\033[0m ({:d}/{:d})".format(
                                download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))

                log_seperator()
                if stories_image and stories_video:
                    log_info_green("Finished downloading {:d} image(s) and {:d} video(s). (Excluding embedded files)".format(
                        stories_image, stories_video))
                elif stories_image:
                    log_info_green(
                        "Finished downloading {:d} image(s). (Excluding embedded files)".format(stories_image))
                elif stories_video:
                    log_info_green(
                        "Finished downloading {:d} video(s). (Excluding embedded files)".format(stories_video))

                else:
                    log_info_green("No new stories have been downloaded. (Excluding embedded files)".format(
                        stories_image, stories_video))
                log_seperator()
            else:
                log_seperator()
                log_warn("There are no stories available to download.")
                shutil.rmtree(download_path)
                log_seperator()
                exit(2)
        else:
            log_error(
                "Could not make required directories. Ensure you have write permissions.")
            log_error("The script cannot continue, exiting.")
            exit(1)
    except Exception as e:
        log_error("Something went wrong: {:s}".format(str(e)))
        log_error("The script cannot continue, exiting.")
        exit(1)


def download_story(media_url, save_path):
    if not os.path.exists(save_path):
        try:
            urllib.URLopener().retrieve(media_url, save_path)
            return True
        except Exception as e:
            log_warn("The story could not be downloaded: {:s}".format(str(e)))
            return "Error"
    else:
        return False


def check_directories(snapchat_story_id):
    try:
        if not os.path.isdir(os.getcwd() + "/snapchat/{}/".format(snapchat_story_id)):
            os.makedirs(
                os.getcwd() + "/snapchat/{}/".format(snapchat_story_id))
        return True
    except Exception:
        return False


# Logging functions

def supports_color():
    try:
        """
        from https://github.com/django/django/blob/master/django/core/management/color.py
        Return True if the running system's terminal supports color,
        and False otherwise.
        """

        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (
            plat != 'win32' or 'ANSICON' in os.environ)

        # isatty is not always implemented, #6223.
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if not supported_platform or not is_a_tty:
            return "No", False
        return "Yes", True
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_seperator():
    try:
        print(sep)
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_info_green(string):
    try:
        if supports_color()[1] == False:
            print(ansi_escape.sub('', string))
        else:
            print('[\033[92mI\033[0m] {:s}\033[0m'.format(string))
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_info_blue(string):
    try:
        if supports_color()[1] == False:
            print(ansi_escape.sub('', string))
        else:
            print('[\033[94mI\033[0m] {:s}\033[0m'.format(string))
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_warn(string):
    try:
        if supports_color()[1] == False:
            print(ansi_escape.sub('', string))
        else:
            print('[\033[93mW\033[0m] {:s}\033[0m'.format(string))
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_error(string):
    try:
        if supports_color()[1] == False:
            print(ansi_escape.sub('', string))
        else:
            print('[\033[91mE\033[0m] {:s}\033[0m'.format(string))
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_whiteline():
    try:
        print("")
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


def log_plain(string):
    try:
        print(ansi_escape.sub('', string))
        sys.stdout.flush()
    except Exception as e:
        print("Error while logging: {}" + str(e))


# Slugifying method https://blog.dolphm.com/slugify-a-string-in-python/

def slugify(s):

    s.lower()

    for c in [' ', '-', '.', '/', ':', '<', '>', '?', '|', '*', '"', '\\', '\'']:
        s = s.replace(c, '_')

    s = re.sub('\W', '', s)

    s = s.replace('_', ' ')

    s = re.sub('\s+', ' ', s)

    s = s.strip()

    s = s.replace(' ', '-')

    return s


start()
