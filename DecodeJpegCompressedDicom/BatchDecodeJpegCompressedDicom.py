import os
from file_utils import bat_files_rec
from DecodeJpegCompressedDicom import DecodeJpegCompressedDicom


def ignore(in_dir, names):
  ignore_set = set()
  for name in names:
    _, suffix = os.path.splitext(name)
    if suffix != ".dcm" and os.path.isfile(os.path.join(in_dir, name)):
      ignore_set.add(name)
  return ignore_set

def BatchDecodeJpegCompressedDicom(in_dir, out_dir):
  bat_files_rec(in_dir, out_dir, DecodeJpegCompressedDicom, ignore)


if __name__ == '__main__':
  # do not support Chinese characters in file paths (because of dcmdjpeg.exe do not support that)
  in_dir = r"D:\Data\Liver"
  out_dir = r"D:\DataEx\Liver"
  BatchDecodeJpegCompressedDicom(in_dir, out_dir)