# Notice
Snapchat is constantly changing how their backend returns information (for the worse). The script may stop working at any time and no updates are guaranteed.

# PySnapStories
A Python script to download public Snapchat user stories from verified accounts, subjects and Map events.

# How to use

Go to https://story.snapchat.com/ and search for Snapchat stories you wish to download.

PySnapStories supports the following input formats:

```
loren (Username story)
c:LCfi6UdStalK_e-T5_WEK3jtBlY8js6KCOiJu_psBtsyHdrvG1KzpxvL8GG094H6ceU (Subject story)
m:q4_OINadScux6p1c6OgxRwAAEQtp2S0W_3UVaAWXqb9GaAWXqb838AAFRgA/ (Single Map Event story)
p:219c05b1bb1c710f (Map Event story)
```

You can obtain the above IDs through the Share function in the Snapchat web client: https://map.snapchat.com/

Be aware that with usernames, only officially verified Snapchat accounts are publicly visible and available for download. You will not be able to download any stories from regular accounts.

Folder structure is as following:
```
pysnapstories.py
└───snapchat
    └───StoryId_StoryTitle
        └───embedded
        └───overlay
```
For each user or other type of story a new folder will be created with the appropriate name.  
Inside this folder the stories will be downloaded with visual overlays removed when possible.  
The `embedded` folder contains the same stories but with the overlays untouched, just as you would see them on Snapchat.  
When downloading usernames, an `overlay` folder will be created containing saved overlays whenever they are detected on Snapchat stories.

### Example

```
> python3 pysnapstories.py loren
-----------------------------------------------------------------------------------------------
[I] PYSNAPSTORIES (SCRIPT V2.0 - PYTHON V3.7.3) - 07:15:11 PM
-----------------------------------------------------------------------------------------------
[I] Treating input as username. (no ID was detected)
[I] Starting download for user: loren
-----------------------------------------------------------------------------------------------
[I] Story Id     : loren
[I] Story Title  : Loren Gray
[I] Story amount : 8
-----------------------------------------------------------------------------------------------
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAgVEPGUQK2HA6eAWxZR_PWAWxY7GSo_____w_media.mp4 (1/8)
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAg9V5xSA3j4u4wAWxZqP-dAWxZqPkT_____w_media.mp4 (2/8)
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAg9XpmNpYLjEecAWxapW7-AWxZwjTI_____w_media.jpg (3/8)
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAgSmP4GN5-QRFhAWxZ6KzWAWxZwo47_____w_media.jpg (4/8)
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAgCWU7JUt7_EycAWxZyBzrAWxZwxq7_____w_media.mp4 (5/8)
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAgVg2Qt-KWzso9AWxdLbueAWxdLboX_____w_media.jpg (6/8)
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAgRxcJG9KB8fvuAWxd5IQAAWxd5IBO_____w_media.mp4 (7/8)
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAg6zi1f6iU5Lv5AWxeA74VAWxeA7rn_____w_media.mp4 (8/8)
-----------------------------------------------------------------------------------------------
[I] Finished downloading 3 image(s) and 5 video(s). (Excluding embedded files)
-----------------------------------------------------------------------------------------------
```
