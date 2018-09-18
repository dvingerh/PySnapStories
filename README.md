# PySnapStories
A Python script to download public Snapchat user stories and events.

# How to use

PySnapStories supports at least the following input formats:

```
https://story.snapchat.com/s/loren (Username story)
https://story.snapchat.com/s/s:0bU-rX4FRxqPG4o5QScoFA (Single user story)
https://story.snapchat.com/s/c:LCfi6UdStalK_e-T5_WEK3jtBlY8js6KCOiJu_psBtsyHdrvG1KzpxvL8GG094H6ceU (Subject story)
https://story.snapchat.com/s/m:q4_OINadScux6p1c6OgxRwAAEQtp2S0W_3UVaAWXqb9GaAWXqb838AAFRgA/ (single Map Event story)
https://play.snapchat.com/p:219c05b1bb1c710f (Map Event story)
```

Entering an username only will also download all available stories. Most plain IDs as input are (probably) supported as well.

Example: `python3 pysnapstories.py https://story.snapchat.com/s/loren`

### Example

```
> python3 pysnapstories.py https://story.snapchat.com/s/loren
----------------------------------------------------------------------
[I] PYSNAPSTORIES (SCRIPT V1.0 - PYTHON V3.6.3) - 02:53:18 PM
----------------------------------------------------------------------
[I] Input detected as Username.
[I] Starting download for user: loren
----------------------------------------------------------------------
[I] Waiting for JSON response request..
[I] Got response, reading contents..
----------------------------------------------------------------------
[I] Downloading a total of 12 stories..
----------------------------------------------------------------------
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAApB4n7Z-hvq7kAWXot0CkAWXotywqAAFRgA_media.mp4  (1/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAAWordVSgzxOqxAWXoyqCSAWXouEtcAAFRgA_media.mp4  (2/12)
[I] Downloaded image: iqGdye5oT8ylxcSlAVW3BwAAAgjlOOB_nDaA5AWXoywUiAWXoywPOAAFRgA_media.jpg  (3/12)
[I] Downloaded image: iqGdye5oT8ylxcSlAVW3BwAAATr0afw-gZcowAWXo1bFRAWXo1a1xAAFRgA_media.jpg  (4/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAA4u07aKWtlQH8AWXo4ksoAWXo4kRAAAFRgA_media.mp4  (5/12)
[I] Downloaded image: iqGdye5oT8ylxcSlAVW3BwAAAWx8LQrcRrDTqAWXo-2UmAWXo-2GRAAFRgA_media.jpg  (6/12)
[I] Downloaded image: iqGdye5oT8ylxcSlAVW3BwAAAH184C6YLEchoAWXpGj6xAWXpGjmGAAFRgA_media.jpg  (7/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAAFa7lLQ6YqCBaAWXpKD-PAWXpKCSpAAFRgA_media.mp4  (8/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAA2gOefORNCo7-AWXpSNPfAWXpSMa7AAFRgA_media.mp4  (9/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAAdDFLCvA96UlRAWXqWLEIAWXqWJ-gAAFRgA_media.mp4  (10/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAA7vlgtjaFT28xAWXqWK3OAWXqWJ_FAAFRgA_media.mp4  (11/12)
[I] Downloaded video: iqGdye5oT8ylxcSlAVW3BwAAA6_ItSBUTY4h7AWXqXH8mAWXqXHklAAFRgA_media.mp4  (12/12)
----------------------------------------------------------------------
[I] Successfully download 4 images and 8 videos.
----------------------------------------------------------------------
```
