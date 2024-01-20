import moviepy.editor as mpy
import moviepy.video.fx.all as vfx
import moviepy.video.tools.segmenting as mseg
import numpy as np

def supersample(clip, d, nframes, total_duration):
    """ Replaces each frame at time t by the mean of `nframes` equally spaced frames
        taken in the interval [t-d, t+d]. This results in motion blur."""
    def fl(gf, t):
        tt = np.linspace(max(t-d, 0), min(t+d, total_duration), nframes) 
        avg = np.mean(1.0*np.array([gf(t_) for t_ in tt]),axis=0)
        return avg.astype("uint8")
    return clip.fl(fl)

def slide_transition(clip1, clip2, speed, direction):
    w1, h1 = clip1.size
    clip1_tmp = clip1.copy().set_duration(speed)
    w2, h2 = clip2.size
    clip2_tmp = clip2.copy().set_duration(speed)
    if direction == "left":
        slide_out_clip1 = clip1_tmp.set_position(lambda t: (-w1/speed*t, 'center'))
        slide_in_clip2 = clip2_tmp.set_position(lambda t:  ('center', 'center') if t > speed else (w2-w2/speed*t, 'center'))
    else:
        slide_out_clip1 = clip1_tmp.set_position(lambda t: (w1+w1/speed*t, 'center'))
        slide_in_clip2 = clip2_tmp.set_position(lambda t:  ('center', 'center') if t > speed else (-w2+w2/speed*t, 'center'))
        
    return supersample(mpy.CompositeVideoClip([clip1_tmp, slide_out_clip1.set_start(speed).crossfadein(speed/2), slide_in_clip2.set_start(speed), clip2_tmp.set_start(speed*2).crossfadein(speed/2)]), speed/2, 10, speed)
    
def zoom_transition(clip1, clip2, speed):
    w1, h1 = clip1.size
    clip1_tmp = clip1.copy()
    w2, h2 = clip2.size
    clip2_tmp = clip2.copy()

    def resize1(t):
        return 1+t*5
    
    def resize2(t):
        return min(1, 0.01 + 0.99*t/speed)

    clip1_tmp = clip1_tmp.set_position(('center', 'center')).set_fps(25).set_duration(speed).resize(resize1)
    clip2_tmp = clip2_tmp.set_position(('center', 'center')).set_fps(25).set_duration(speed).resize(resize2)

    return mpy.CompositeVideoClip([clip1_tmp, clip2_tmp])


def rotate_zoom_transition(clip1, clip2, speed):
    w1, h1 = clip1.size
    clip1_tmp = clip1.copy().set_duration(speed)
    w2, h2 = clip2.size
    clip2_tmp = clip2.copy().set_duration(speed)
    def resize2(t):
        return min(1, 0.01 + 0.99*t/speed)
    clip2_tmp = clip2_tmp.add_mask().fx(mpy.vfx.rotate, lambda t: 360*t/speed, expand=False)
    clip2_tmp = clip2_tmp.set_position(('center', 'center')).set_fps(25).set_duration(speed).resize(resize2)
    return supersample(mpy.CompositeVideoClip([clip1_tmp, clip2_tmp]), speed/2, 10, speed)
