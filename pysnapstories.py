import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import sys
import os
import time
import re
import shutil

try:
	import urllib.request as urllib
except ImportError:
	import urllib as urllib

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
sep = "-" * 95
script_version = "1.1"
python_version = sys.version.split(' ')[0]
requests_ua = {'User-Agent': "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
story_json_base = "https://storysharing.snapchat.com/v1/fetch/{}?request_origin=ORIGIN_WEB_PLAYER"


def start():
	log_seperator()
	log_info_blue('PYSNAPSTORIES (SCRIPT V{:s} - PYTHON V{:s}) - {:s}'.format(script_version, python_version, time.strftime('%I:%M:%S %p')))
	log_seperator()

	is_not_username = False

	try:
		if ("story.snapchat.com/s/" in sys.argv[1]) and ("/s:" not in sys.argv[1]):
			snapchat_story_id = sys.argv[1].split('/')[-1]
			if len(snapchat_story_id) > 15:
				is_not_username = True
				log_info_blue("Input detected as Story ID.")
			else:
				log_info_blue("Input detected as Username.")
		elif "story.snapchat.com/s/s:" in sys.argv[1]:
			log_info_blue("Input detected as Single story.")
			snapchat_story_id = sys.argv[1].split('/')[-1]
			is_not_username = True
		elif "play.snapchat.com/p:" in sys.argv[1]:
			log_info_blue("Input detected as Event story.")
			snapchat_story_id = sys.argv[1].split('/')[-1]
			is_not_username = True
		elif "map.snapchat.com/ttp/" in sys.argv[1]:
			log_info_blue("Input detected as Map story.")
			snapchat_story_id = "m:" + sys.argv[1].split('/')[-2]
			is_not_username = True
		elif "map.snapchat.com/story/" in sys.argv[1]:
			log_info_blue("Input detected as Map story.")
			snapchat_story_id = "p:" + sys.argv[1].split('/')[-1]
			is_not_username = True
		elif "play.snapchat.com/m:" in sys.argv[1]:
			log_info_blue("Input detected as Single Map story.")
			snapchat_story_id = sys.argv[1].split('/')[-1]
			is_not_username = True
		else:
			log_info_blue("Input detected as Username.")
			snapchat_story_id = sys.argv[1]
	except IndexError:
		log_error("No argument was given, exiting.")
		log_seperator()
		exit(1)

	if not is_not_username:
		log_info_green("Starting download for user: \033[93m{:s}".format(snapchat_story_id))
	else:
		log_info_green("Starting download for ID: \033[93m{:s}".format(snapchat_story_id))
	log_seperator()
	download_snap_stories(snapchat_story_id)


def download_snap_stories(snapchat_story_id):
	try:
		log_info_blue("Waiting for JSON response request..")
		response = requests.get(story_json_base.format(snapchat_story_id), verify=True, headers={
					"User-Agent"    : requests_ua["User-Agent"]
				})
		log_info_blue("Got response, reading contents..")

		if "rpc error: code = NotFound desc = Not found." in response.text:
			log_seperator()
			log_error("This username does not belong to a business account.")
			log_error("The script cannot continue, exiting.")
			log_seperator()
			exit(1)
		else:
			response_json = json.loads(response.text)

		stories_image = 0
		stories_video = 0

		snapchat_story_id = response_json.get("story").get("id", "NoId")
		snapchat_story_name = slugify(response_json.get("story").get("metadata").get("title", "NoName"))

		download_path = os.getcwd() + "/snapchat/{}/".format('{:s}_{:s}'.format(snapchat_story_id, snapchat_story_name))
		download_path_embedded = os.path.join(download_path, "embedded")
		
		if not os.path.exists(download_path_embedded):
			os.makedirs(download_path_embedded)

		if check_directories('{:s}_{:s}'.format(snapchat_story_id, snapchat_story_name)):
			if response_json.get("story").get("snaps"):
				log_seperator()
				log_info_blue("Amount of available stories: {:d}".format(len(response_json.get("story").get("snaps"))))
				log_seperator()
				for index, snap in enumerate(response_json.get("story").get("snaps")):
					media_type = snap.get("media").get("type")
					media_url = snap.get("media").get("mediaUrl")
					media_ts = snap.get("captureTimeSecs")
					media_id = snap.get("id")

					is_embedded = media_url.endswith("embedded.mp4")
					downloaded_in_iteration = False


					if "VIDEO" in media_type:
						if is_embedded:
							download_path_with_file = os.path.join(download_path_embedded, "{:s}_embedded.mp4".format(media_id))
							download_result =  download_story(media_url, download_path_with_file)

						download_path_with_file = os.path.join(download_path, "{:s}_media.mp4".format(media_id))
						download_result =  download_story(media_url.replace("embedded", "media"), download_path_with_file)
						if download_result == "Error":
							pass
						elif download_result == True:
							downloaded_in_iteration = True
							stories_video += 1
							log_info_green("Grabbed video: \033[93m{:s}\033[0m ({:d}/{:d})".format(download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))
						else:
							log_info_blue("Skipped video: \033[93m{:s}\033[0m ({:d}/{:d})".format(download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))

					if "IMAGE" in media_type:
						download_path_with_file = os.path.join(download_path, "{:s}_media.jpg".format(media_id))
						download_result =  download_story(media_url, download_path_with_file)
						if download_result == "Error":
							pass
						elif download_result == True:
							downloaded_in_iteration = True
							stories_image += 1
							log_info_green("Grabbed image: \033[93m{:s}\033[0m ({:d}/{:d})".format(download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))
						else:
							log_info_blue("Skipped video: \033[93m{:s}\033[0m ({:d}/{:d})".format(download_path_with_file.split('/')[-1], index+1, len(response_json.get("story").get("snaps"))))


				log_seperator()
				if stories_image and stories_video:
					log_info_green("Finished downloading {:d} image(s) and {:d} video(s). (Excluding embedded files)".format(stories_image, stories_video))
				elif stories_image:
					log_info_green("Finished downloading {:d} image(s). (Excluding embedded files)".format(stories_image))
				elif stories_video:
					log_info_green("Finished downloading {:d} video(s). (Excluding embedded files)".format(stories_video))

				else:
					log_info_green("No new stories were downloaded. (Excluding embedded files)".format(stories_image, stories_video))
				log_seperator()
			else:
				log_seperator()
				log_warn("There are no stories available to download.")
				shutil.rmtree(download_path)
				log_seperator()
				exit(2)
		else:
			log_error("Could not make required directories. Ensure you have write permissions.")
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
			os.makedirs(os.getcwd() + "/snapchat/{}/".format(snapchat_story_id))
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
		supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

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

	for c in [' ', '-', '.', '/']:
		s = s.replace(c, '_')

	s = re.sub('\W', '', s)

	s = s.replace('_', ' ')

	s = re.sub('\s+', ' ', s)

	s = s.strip()

	s = s.replace(' ', '-')

	return s

start()
