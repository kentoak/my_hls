# -*- coding: utf-8 -*-
import sys, os
import subprocess
import codecs

def create_hls(dir_path,filename):
    movieNum=len([f for f in os.listdir('./hls')])
    new_dir="./hls/movie"+str(movieNum)+"/"
    os.mkdir(new_dir)
    # 高画質m3u8の作成 (input.mp4 -> hls/h.m3u8)
    c = 'ffmpeg'
    c += ' -i '+dir_path+filename+'.mp4'
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 5'
    c += ' -segment_list '+new_dir+'/h.m3u8'
    c += ' '+new_dir+'hls/h_%5d.ts'
    code = subprocess.call(c.split())
    print('process=' + str(code))

    # 低画質mp4の作成 (input.mp4 -> input_low.mp4)
    c = 'ffmpeg'
    c += ' -i '+dir_path+filename+'.mp4'
    c += ' -f mp4 -vcodec h264 -vb 500k -s 640x360 -pix_fmt yuv420p'
    c += ' -ac 2 -ar 48000 -ab 128k -acodec aac -strict experimental'
    c += ' -movflags faststart'
    c += ' '+"./input/low/"+filename+'_low.mp4'
    code = subprocess.call(c.split())
    print('process=' + str(code))

    # 低画質m3u8の作成 (input_low.mp4 -> hls/l.m3u8)
    c = 'ffmpeg'
    c += ' -i '+"./input/low/"+filename+'_low.mp4'
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 5'
    c += ' -segment_list '+new_dir+'/l.m3u8'
    c += ' '+new_dir+'/l_%5d.ts'
    code = subprocess.call(c.split())
    print('process=' + str(code))

    # 低画質高画質を含めたm3u8の作成 (->hls/playlist.m3u8)
    t = '#EXTM3U'
    t += '\n##EXT-X-VERSION:3'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=500000'
    t += '\nl.m3u8'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4000000'
    t += '\nh.m3u8'
    f = codecs.open(new_dir+'playlist.m3u8', 'w', 'utf-8')
    f.write(t)
    f.close()

if __name__ == "__main__":
    dir_path = './input/'
    dir_path1 = './input/low/'
    filenames = [os.path.splitext(f)[0] for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    #filenames = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f != '.DS_Store']
    #print(filenames)
    for f in filenames:
        print(dir_path+f)
        if f+"_low.mp4" in os.listdir(dir_path1):
            continue
        create_hls(dir_path,f)
