import os
import subprocess
import argparse


def DecodeJpegCompressedDicom(dcmfile_in, dcmfile_out):
  """
  Reads a JPEG-compressed DICOM image (dcmfile_in), decompresses the JPEG data
  (i. e. conversion to a native DICOM transfer syntax) and writes the converted
  image to an output file (dcmfile_out).
  """
  # check following url for dcmdjpeg.exe usage
  # http://support.dcmtk.org/docs-snapshot/dcmdjpeg.html
  TOOL_PATH = "dcmdjpeg.exe"
  try:
    print("processing: %s" % dcmfile_in)
    subprocess.check_call([TOOL_PATH, dcmfile_in, dcmfile_out])
  except subprocess.CalledProcessError:
    print("Call dcmdjpeg.exe failed.")


if __name__ == '__main__':
  parser = argparse.ArgumentParser("Decode JPEG-compressed dicom image")
  parser.add_argument("dcmfile_in", type=str, help="input JPEG-compressed dicom image")
  parser.add_argument("dcmfile_out", help="output decompressed dicom image")
  args = parser.parse_args()

  DecodeJpegCompressedDicom(args.dcmfile_in, args.dcmfile_out)