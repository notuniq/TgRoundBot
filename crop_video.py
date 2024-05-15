import moviepy.editor as mp

def video_crop(base_video, out_video):
    clip = mp.VideoFileClip(base_video)
    width, height = clip.size
    xcenter = width // 2
    ycenter = height // 2
    min_size = height if height < width else width
    if min_size > 620:
        min_size = 620
    clip_resized = clip.crop(width=min_size, height=min_size, x_center=xcenter, y_center=ycenter)
    clip_resized.write_videofile(out_video)
    return min_size, clip.duration
