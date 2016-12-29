import os
import shutil

#-------------------------------------------------------------------------------
join_path = os.path.join

#-------------------------------------------------------------------------------
is_dir   = os.path.isdir
is_file  = os.path.isfile
is_exist = os.path.exists

#-------------------------------------------------------------------------------
get_filename = os.path.basename
get_dirname = os.path.basename

def get_filename_without_ext(src):
  """If filename does not contain an extension,
     just return the filename
  """
  filename = get_filename(src)
  return os.path.splitext(filename)[0]

#-------------------------------------------------------------------------------
copy_dir   = shutil.copytree
move_dir   = shutil.move
rename_dir = os.rename
remove_dir = shutil.rmtree

def make_dir(path):
  """If path is an existing directory, do nothing.
     If path is not an existing directory, make it a directory
  """
  if not is_dir(path):
    os.mkdir(path)

def make_dir_rec(path):
  """Refer to os.makedirs
  """
  if not is_dir(path):
    os.makedirs(path)

#-------------------------------------------------------------------------------
copy_file   = shutil.copy # dst can be either file path or the target directory path
move_file   = os.rename
rename_file = os.rename
remove_file = os.remove

def copy_files(file_path_list, dst_dir):
  assert is_dir(dst_dir)
  for file_path in file_path_list:
    copy_file(file_path, dst_dir)

#-------------------------------------------------------------------------------
def find_files_rec(root_path, key_word):
  """ Recursively find files that contain 'key_word'
  Args:
    root_path: root directory path containing files
    key_word: key word used for matching

  Returns:
    list of file pathes satisfying given condition
  """
  file_path_list = []
  for dir_root, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
      if filename.find(key_word):
        file_path_list.append(join_path(dir_root, filename))
  return file_path_list

def find_dirs_rec(root_path, key_word):
  """ Recursively find directories that contain 'key_word'
  Args:
    root_path: root directory path containing directories
    key_word: key word used for matching

  Returns:
    list of directory pathes satisfying given condition
  """
  dir_list = []
  for dir_root, dirnames, filenames in os.walk(root_path):
    for dirname in dirnames:
      if dirname.find(key_word):
        dir_list.append(join_path(dir_root, dirname))
  return dir_list

#-------------------------------------------------------------------------------
def bat_files_rec(in_dir, out_dir, func, ignore=None, keep_structure=True):
  """Recursively process all files in a given folder.
  Args:
    in_dir: input root directory
    out_dir: output root directory
    func: a callback for processing each file-> func(in_filepath, out_filepath)
    ignore: refer to ignore argument in shutil.copytree()
    keep_structure: If True, keep output folder structure as input folder structure.
                    Otherwise, output all items in output root directory
  """
  names = os.listdir(in_dir)
  if ignore is not None:
    ignored_names = ignore(in_dir, names)
  else:
    ignored_names = set()

  if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

  for name in names:
    if name in ignored_names:
      continue
    in_sub = join_path(in_dir, name)
    out_sub = join_path(out_dir, name) if keep_structure else out_dir
    if os.path.isdir(in_sub):
      bat_files_rec(in_sub, out_sub, func, ignore, keep_structure)
    else:
      func(in_sub, out_sub)