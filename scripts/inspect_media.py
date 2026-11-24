#!/usr/bin/env python3
"""Inventory hashes and frame-by-frame differences without sampling/omitting frames."""
from __future__ import annotations
import argparse, csv, hashlib, json, subprocess
from pathlib import Path


def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def probe(path: Path) -> dict:
    cmd=['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]
    return json.loads(subprocess.check_output(cmd, text=True))


def run() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--save-frames',action='store_true',help='WARNING: many full-resolution PNG files; only for local research')
    args=p.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    import cv2
    import numpy as np
    report=[]
    for vid in sorted(args.input_dir.glob('*.mp4')):
        meta={'name':vid.name,'sha256':sha256_file(vid),'size':vid.stat().st_size,'ffprobe':probe(vid)}
        cap=cv2.VideoCapture(str(vid)); prev=None; n=0
        frame_dir=args.output/(vid.stem+'_frames')
        if args.save_frames: frame_dir.mkdir(parents=True,exist_ok=True)
        with (args.output/(vid.stem+'_frame_diffs.csv')).open('w',newline='') as fd:
            writer=csv.writer(fd);writer.writerow(['frame_zero_based','timestamp_seconds','mean_abs_difference_from_previous'])
            while True:
                ok,frame=cap.read()
                if not ok: break
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                diff=float(np.mean(cv2.absdiff(gray,prev))) if prev is not None else 0.0
                writer.writerow([n,f'{n/60:.9f}',f'{diff:.8f}'])
                if args.save_frames: cv2.imwrite(str(frame_dir/f'f_{n:04d}.png'),frame)
                prev=gray; n+=1
        cap.release();meta['frames_decoded']=n;report.append(meta)
        print(vid.name, n, 'frames; SHA256',meta['sha256'])
    (args.output/'manifest_runtime.json').write_text(json.dumps(report,indent=2),encoding='utf-8')


if __name__=='__main__': run()
