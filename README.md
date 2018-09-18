# PySnapStories
A Python script to download public Snapchat user stories and events.

# How to use

PySnapStories supports at least the following input formats:

```
https://story.snapchat.com/s/loren (Username story)
https://story.snapchat.com/s/s:0bU-rX4FRxqPG4o5QScoFA (Single user story)
https://story.snapchat.com/s/c:LCfi6UdStalK_e-T5_WEK3jtBlY8js6KCOiJu_psBtsyHdrvG1KzpxvL8GG094H6ceU (Subject story)
https://story.snapchat.com/s/m:q4_OINadScux6p1c6OgxRwAAEQtp2S0W_3UVaAWXqb9GaAWXqb838AAFRgA/ (Single Map Event story)
https://play.snapchat.com/p:219c05b1bb1c710f (Map Event story)
```

Entering an username only will also download all available stories. Most plain IDs as input are (probably) supported as well.

Be aware that only business account's stories are publicly visible and available for download. You will not be able to download any stories from regular accounts.

Folder structure is as following:
```
root
└───snapchat
    └───StoryId_StoryTitle
        └───embedded
```
For each user or other type of story a new folder will be created with the appropriate name. Inside this folder the stories will be downloaded with visual overlays removed when possible. The `embedded` folder contains the same stories but with the overlays untouched, just as you would see them on Snapchat.

Example: `python3 pysnapstories.py https://story.snapchat.com/s/loren`

### Example

```
> python3 pysnapstories.py loren
-----------------------------------------------------------------------------------------------
[I] PYSNAPSTORIES (SCRIPT V1.1 - PYTHON V3.6.4) - 11:46:36 PM
-----------------------------------------------------------------------------------------------
[I] Input detected as Username.
[I] Starting download for user: loren
-----------------------------------------------------------------------------------------------
[I] Waiting for JSON response request..
[I] Got response, reading contents..
-----------------------------------------------------------------------------------------------
[I] Downloading a total of 9 stories..
-----------------------------------------------------------------------------------------------
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAAdDFLCvA96UlRAWXqWLEIAWXqWJ-gAAFRgA_media.mp4 (1/9)
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAA7vlgtjaFT28xAWXqWK3OAWXqWJ_FAAFRgA_media.mp4 (2/9)
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAA6_ItSBUTY4h7AWXqXH8mAWXqXHklAAFRgA_media.mp4 (3/9)
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAAdi2EJaUmc3JwAWXtd-C6AWXtd9-YAAFRgA_media.jpg (4/9)
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAAobqNM15eGJviAWXth8sBAWXth8cUAAFRgA_media.jpg (5/9)
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAAFp_e6Qf31clAAWXt124rAWXt11_1AAFRgA_media.mp4 (6/9)
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAAn94lRd2mye8zAWXt20-4AWXt2lCdAAFRgA_media.mp4 (7/9)
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAAd4ClQhHN8TOtAWXt57CWAWXt55DtAAFRgA_media.mp4 (8/9)
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAAN0jUGs_xpFAIAWXuMavjAWXuMZk-AAFRgA_media.jpg (9/9)
-----------------------------------------------------------------------------------------------
[I] Finished downloading 2 images and 2 videos. (Excluding embedded files)
-----------------------------------------------------------------------------------------------
```
