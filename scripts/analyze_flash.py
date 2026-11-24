#!/usr/bin/env python3
"""Blind-friendly analysis of 1–2-frame overlay in Puzzle 1 solved reveal.

Outputs original frames, horizontal mirrors, and absolute differences. It does
not transcribe any text or preload the expected Puzzle 2 address.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path


def run():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--frames',type=int,nargs='+',default=[726,727,728,729])
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    import cv2
    cap=cv2.VideoCapture(str(args.video));frames={}
    for n in sorted(set(args.frames)):
        cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,frame=cap.read()
        if not ok: raise RuntimeError(f'Frame {n} unavailable')
        frames[n]=frame
        cv2.imwrite(str(args.output/f'frame_{n:04d}.png'),frame)
        cv2.imwrite(str(args.output/f'frame_{n:04d}_mirror.png'),cv2.flip(frame,1))
    cap.release()
    for i,n in enumerate(sorted(frames)):
        if i==0: continue
        prev=sorted(frames)[i-1]
        diff=cv2.absdiff(frames[n],frames[prev])
        gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(str(args.output/f'diff_{n:04d}_minus_{prev:04d}.png'),gray)
    (args.output/'README.txt').write_text('BLIND TRANSCRIPTION: inspect mirrored frames and differences without importing a known destination string. All indices are zero based.\n',encoding='utf-8')
    print('Saved',len(frames),'raw/mirrored frames and adjacent differences; no text inferred.')

if __name__=='__main__':run()
