from PIL import Image
import os,zipfile,shutil
from django.core.files import File



def rea(dir,pdf_name):
  if pdf_name.endswith(".pdf"):
    pdf_name=pdf_name
  else:
    pdf_name="{0}.pdf".format(pdf_name)
  file_list = os.listdir(dir)
  pic_name = [ os.path.join(dir,im) for im in file_list if "jpg" in im or "png" in im]
  if not pic_name: return False
  pic_name.sort()
  im_list = []
  im1 = Image.open(pic_name[0])
  pic_name.pop(0)
  for i in  pic_name:
    img = Image.open(i)
    if img.mode == "RGBA":
      img = img.convert('RGB')
      im_list.append(img)
    else:
      im_list.append(img)
  im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
  return True

def un_zip(filename):

  if not filename.endswith('.zip'):return False
  dir = os.path.splitext(filename)[0]
  if not os.path.isdir(dir):
    os.mkdir(os.path.splitext(filename)[0])
  zip_file = zipfile.ZipFile(filename)
  for names in zip_file.namelist():
    zip_file.extract(names, dir)
  zip_file.close()
  return dir

def get_imgdir(dir):
  file_list = os.listdir(dir)
  secdir=os.path.join(dir,file_list[0])

  if len(file_list)==1 and os.path.isdir(secdir):
    return get_imgdir(secdir)
  else:
    return dir

def zip_include_jpg_or_pnp_to_pdf(zip):
  unzip_dir = un_zip(zip)#解压为同名文件夹，如果不是zip文件，解压失败，那么就不继续执行
  if unzip_dir:
    redir = get_imgdir(unzip_dir)
    #如果生成PDF成功，删除之前的ZIP文件，如果不成功则不用删除
    try:
      pdf_pathname=zip.replace('.zip','.pdf')
      if rea(redir, pdf_pathname):
        os.remove(zip)
        return pdf_pathname
      else:
        return False
    except:
      pass
    finally:
      #不管是否成功，都必须删除解压的文件夹
      shutil.rmtree(unzip_dir)



def convert_all_zip(request):
  from contract.models import Contract
  qs=Contract.objects.filter(file__contains='.zip')
  for obj in qs:
    file = obj.file
    pdf = zip_include_jpg_or_pnp_to_pdf(file.path)
    if pdf:
      file.save(os.path.basename(pdf), File(open(pdf, "rb")))
      os.remove(pdf)
      obj.save()
