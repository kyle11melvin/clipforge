# 4x upscale with Real-ESRGAN (ONNX, CPU) in overlapping tiles. usage: upscale.py model.onnx in.png out.png
import sys, numpy as np, cv2, onnxruntime as ort
model, inp, outp = sys.argv[1:4]
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
img = cv2.imread(inp)[:, :, ::-1].astype(np.float32) / 255.0  # RGB
H, W = img.shape[:2]; T, P, S = 160, 16, 4
out = np.zeros((H*S, W*S, 3), np.float32)
for y in range(0, H, T):
    for x in range(0, W, T):
        y0, x0 = max(0, y-P), max(0, x-P); y1, x1 = min(H, y+T+P), min(W, x+T+P)
        tile = img[y0:y1, x0:x1].transpose(2,0,1)[None]
        res = sess.run(None, {sess.get_inputs()[0].name: tile})[0][0].transpose(1,2,0)
        oy, ox = (y-y0)*S, (x-x0)*S
        hh, ww = (min(H, y+T)-y)*S, (min(W, x+T)-x)*S
        out[y*S:y*S+hh, x*S:x*S+ww] = res[oy:oy+hh, ox:ox+ww]
out = (np.clip(out, 0, 1)*255).round().astype(np.uint8)[:, :, ::-1]
cv2.imwrite(outp, out); print(outp, out.shape[1], out.shape[0])
