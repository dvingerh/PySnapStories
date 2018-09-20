# PySnapStories
A Python script to download public Snapchat user stories and events.

# How to use

Go to https://story.snapchat.com/ and search for Snapchat stories you wish to download.

PySnapStories supports at least the following input formats:

```
https://story.snapchat.com/s/loren (Username story)
https://story.snapchat.com/s/s:0bU-rX4FRxqPG4o5QScoFA (Single user story)
https://story.snapchat.com/s/c:LCfi6UdStalK_e-T5_WEK3jtBlY8js6KCOiJu_psBtsyHdrvG1KzpxvL8GG094H6ceU (Subject story)
https://story.snapchat.com/s/m:q4_OINadScux6p1c6OgxRwAAEQtp2S0W_3UVaAWXqb9GaAWXqb838AAFRgA/ (Single Map Event story)
https://play.snapchat.com/p:219c05b1bb1c710f (Map Event story)
```

Entering an username only will also download all available stories. Most plain IDs as input are (probably) supported as well.

Be aware that only officially verified Snapchat accounts are publicly visible and available for download. You will not be able to download any stories from regular accounts.

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
[I] PYSNAPSTORIES (SCRIPT V1.3 - PYTHON V3.6.4) - 12:20:17 PM                                  
-----------------------------------------------------------------------------------------------
[I] Starting download for user: loren                                                          
-----------------------------------------------------------------------------------------------
[I] Story Id     : loren                                                                       
[I] Story Title  : Loren Gray                                                                  
[I] Story amount : 8                                                                           
-----------------------------------------------------------------------------------------------
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAAbWnYjQtiHBRKAWXynQ_aAWXynQfaAAFRgA_media.mp4 (1/8) 
[I] Skipped image: iqGdye5oT8ylxcSlAVW3BwAAAtrENNhmxp4vAAWXyncNjAWXynb_aAAFRgA_media.jpg (2/8) 
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAAXc0wjfUWucIhAWXyqUNqAWXyqPZIAAFRgA_media.mp4 (3/8) 
[I] Skipped video: iqGdye5oT8ylxcSlAVW3BwAAAnbN0gxdDlXBVAWXyrlijAWXyrXZiAAFRgA_media.mp4 (4/8) 
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAAXnYNmXp24BuvAWXzKTirAWXzKR0FAAFRgA_media.mp4 (5/8) 
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAA3mBWgobzU_PcAWXzyBXSAWXzyBToAAFRgA_media.jpg (6/8) 
[I] Grabbed image: iqGdye5oT8ylxcSlAVW3BwAAAIx70L2O3uDq_AWX0F8bsAWX0F8MzAAFRgA_media.jpg (7/8) 
[I] Grabbed video: iqGdye5oT8ylxcSlAVW3BwAAAV4B4ssbnv_HEAWX0__dRAWX0_3z9AAFRgA_media.mp4 (8/8) 
-----------------------------------------------------------------------------------------------
[I] Finished downloading 2 image(s) and 2 video(s). (Excluding embedded files)                 
-----------------------------------------------------------------------------------------------
```
