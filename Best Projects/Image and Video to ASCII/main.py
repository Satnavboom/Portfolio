import math
import os
import time
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips, AudioFileClip

random_chars = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
chars = "@#8&%*WMB0QDLi|:,. "[::-1]
charArr = list(chars)
charLen = len(charArr)
interval = charLen / 256

sf = 0.25
font_path = "lucon.ttf"
font_size = 30
font = ImageFont.truetype(font_path, size=font_size)

def get_font_bbox(font):
    maxW = maxH = 0
    for char in chars:
        bbox = font.getbbox(char)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        maxW = max(maxW, w)
        maxH = max(maxH, h)
    return maxW, maxH

charW, charH = get_font_bbox(font)

def getChar(inputInt, mode, symbol=None):
    if mode == 'symbol':
        return symbol
    elif mode == "random":
        return random_chars[random.randint(0, len(random_chars) - 1)]
    else:
        return charArr[math.floor(inputInt * interval)]

def convert_frame_to_ascii(frame):
    # Convert Numpy array to PIL Image
    image = Image.fromarray(frame)
    w, h = image.size
    image = image.resize((int(sf * w), int(sf * h * (charW / charH))), Image.NEAREST)
    w, h = image.size
    pixelArr = image.load()

    outputImage = Image.new('RGB', (charW * w, charH * h), color=(0, 0, 0))
    draw = ImageDraw.Draw(outputImage)

    for y in range(h):
        for x in range(w):
            if x < w and y < h:
                r, g, b = pixelArr[x, y]
                greyVal = (r + g + b) // 3
                draw.text((x * charW, y * charH), getChar(greyVal, mode, symbol), font=font, fill=(r, g, b))
    
    return outputImage  # Return PIL Image object

def process_video(inputPath, outputPath, mode, symbol=None):
    # Load the video
    clip = VideoFileClip(inputPath)
    total_frames = int(clip.fps * clip.duration)
    start_time = time.time()

    # Extract audio
    audio = clip.audio
    if audio is not None:
        audio_path = outputPath.replace('.mp4', '_audio.mp3')
        audio.write_audiofile(audio_path)

    # Process video frames in batches
    batch_size = 50
    frames = []

    def process_frame(frame):
        return convert_frame_to_ascii(frame)
    
    def process_batch(start_index, end_index):
        batch_frames = []
        for i, frame in enumerate(clip.iter_frames()):
            if i >= start_index and i < end_index:
                batch_frames.append(process_frame(frame))
            elif i >= end_index:
                break
        return batch_frames
    
    for i in range(0, total_frames, batch_size):
        end_index = min(i + batch_size, total_frames)
        batch_frames = process_batch(i, end_index)
        frames.extend(batch_frames)
        
        # Progress reporting
        elapsed_time = time.time() - start_time
        percent = (end_index / total_frames) * 100
        avg_time_per_frame = elapsed_time / (end_index if end_index > 0 else 1)
        estimated_total_time = avg_time_per_frame * total_frames
        estimated_remaining_time = estimated_total_time - elapsed_time
        
        print(f"Processing video: {end_index}/{total_frames} frames. ETA: {estimated_remaining_time:.2f} seconds [{percent:.2f}%]", end='\r')

    try:
        clip_out = ImageSequenceClip([np.array(frame) for frame in frames], fps=clip.fps)
        
        # Save the ASCII video
        temp_video_path = outputPath.replace('.mp4', '_temp.mp4')
        clip_out.write_videofile(temp_video_path, codec='libx264', bitrate='5000k')
        
        # Combine with original audio
        final_clip = VideoFileClip(temp_video_path)
        if audio is not None:
            audio_clip = AudioFileClip(audio_path)
            final_clip = final_clip.set_audio(audio_clip)
        
        final_clip.write_videofile(outputPath, codec='libx264', audio_codec='aac')
        
        # Clean up temporary files
        os.remove(temp_video_path)
        if audio is not None:
            os.remove(audio_path)
        
    except Exception as e:
        print(f"\nError processing video: {e}")
    
    end_time = time.time()
    print(f"\n\nVideo saved to {outputPath}")
    print(f"Time taken to save the video: {end_time - start_time:.2f} seconds\n\n")

def process_gif(inputPath, outputPath, mode, symbol=None):
    gif = Image.open(inputPath)
    frames = []
    start_time = time.time()
    total_frames = 0
    
    while True:
        frame = convert_frame_to_ascii(np.array(gif.copy()))
        frames.append(frame)
        total_frames += 1
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break
    
    frames[0].save(outputPath, save_all=True, append_images=frames[1:], loop=0, duration=gif.info['duration'])

    end_time = time.time()
    print(f"\n\nGIF saved to {outputPath}")
    print(f"Time taken to save the GIF: {end_time - start_time:.2f} seconds\n\n")

def create_ascii_image(inputPath, outputPath, mode, symbol=None):
    file_ext = os.path.splitext(inputPath)[1].lower()
    
    if file_ext in ['.mp4']:
        process_video(inputPath, outputPath, mode, symbol)
    elif file_ext in ['.gif']:
        process_gif(inputPath, outputPath, mode, symbol)
    elif file_ext in ['.png', '.jpg', '.jpeg', '.webp']:
        start_time = time.time()
        image = Image.open(inputPath)
        w, h = image.size
        image = image.resize((int(sf * w), int(sf * h * (charW / charH))), Image.NEAREST)
        w, h = image.size
        pixelArr = image.load()

        outputImage = Image.new('RGB', (charW * w, charH * h), color=(0, 0, 0))
        draw = ImageDraw.Draw(outputImage)

        for y in range(h):
            for x in range(w):
                if x < w and y < h:
                    pixel = pixelArr[x, y]
                    if len(pixel) == 4:
                        r, g, b, _ = pixel
                    else:
                        r, g, b = pixel
                    
                    greyVal = (r + g + b) // 3
                    draw.text((x * charW, y * charH), getChar(greyVal, mode, symbol), font=font, fill=(r, g, b))
            
            # Progress reporting
            elapsed_time = time.time() - start_time
            rows_processed = y + 1
            rows_remaining = h - rows_processed
            
            if rows_processed > 0:
                avg_time_per_row = elapsed_time / rows_processed
                estimated_total_time = avg_time_per_row * h
                estimated_remaining_time = estimated_total_time - elapsed_time

                percent = (rows_processed / h) * 100
                percent = min(percent, 100)
                
                if rows_processed == 20:
                    print(f"\nEstimated total time: {estimated_total_time:.2f} seconds")
                
                if rows_processed > 20:
                    print(f"Progress: {rows_processed}/{h} rows processed. ETA: {estimated_remaining_time:.2f} seconds [{percent:.2f}%]", end='\r')

        outputImage.save(outputPath)
        end_time = time.time()
        
        print(f"\n\nColored ASCII image saved to {outputPath}")
        print(f"Time taken to save the image: {end_time - start_time:.2f} seconds\n\n")
        
        outputImage.show()
    else:
        print("Unsupported file format. Please provide a PNG, JPG, JPEG, WEBP, MP4, or GIF file.")

if __name__ == "__main__":
    file_path = input("\n\n\nEnter image/video path: ").strip()
    mode = "ascii" # Modes: ascii, symbol, random
    
    if mode == "symbol":
        symbol = input("Enter the symbol: ").strip()
    else:
        symbol = None

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    if os.path.isfile(file_path):
        output_path = os.path.join(os.path.dirname(file_path), f"{base_name}_ascii{os.path.splitext(file_path)[1].lower()}")
        create_ascii_image(file_path, output_path, mode, symbol)
    else:
        print("File does not exist. Please check the file path and try again.")
