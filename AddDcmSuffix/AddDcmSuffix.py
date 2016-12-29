import dicom
import os


def isdicom(file_path):
  if not os.path.isfile(file_path):
    return False

  with open(file_path, 'rb') as f:
    preamble_magic_code = f.read(132)

  # if file length is less than preamble + magic_code size
  # it is not a valid dicom file
  if not preamble_magic_code:
    return False
    # magic code should be DICM, otherwise, not a valid dicom file
  magic_code = preamble_magic_code[128:132]
  if magic_code != 'DICM':
    return False

  return True


def AddDcmSuffix(file_path):
  if not isdicom(file_path):
    return

  DCM_SUFFIX = ".dcm"
  _, suffix = os.path.splitext(file_path)
  if suffix != DCM_SUFFIX:
    os.rename(file_path, file_path + DCM_SUFFIX)
