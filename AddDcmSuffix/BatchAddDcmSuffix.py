import os
from AddDcmSuffix import AddDcmSuffix

# add .dcm suffix to dicom files which do not have a .dcm suffix

if __name__ == "__main__":
  root_path = r"D:\Data_Ex\Liver"

  for dir_root, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
      file_path = os.path.join(dir_root, filename)
      AddDcmSuffix(file_path)
