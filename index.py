#!C:/Users/jorge/AppData/Local/Programs/Python/Python36/python.exe
import cgi
import os
import shutil
import tarfile
import crystal

print("Content-Type: text/html\n")

print("""
<form method="post" enctype="multipart/form-data">
<div style="border: solid 1px black; width: 50%;">
 <div style="margin: 0.25in;">
     <div>
        <label for="package">Report package name:</label>
        <input type="text" id="package" name="package" required autofocus>
     </div>
     <br />
     <div>
       <label for="file">Choose files to upload</label>
       <input type="file" id="file" name="file" required multiple>
     </div>
     <br />
     <div>
       <button style="font-size: 20px">Submit</button>
     </div>
 </div>
</div>
</form>
""")

formData = cgi.FieldStorage()

packageName = formData["package"].value

if os.path.exists("uploads/" + packageName):
    shutil.rmtree("uploads/" + packageName)

if os.path.exists("downloads/" + packageName):
    shutil.rmtree("downloads/" + packageName)

os.makedirs("uploads/" + packageName)
os.makedirs("downloads/" + packageName)

if "file" in formData:
    for resource in formData["file"]:
        fileName = resource.filename
        fileContent = resource.value

        path = "C:/Apache24/htdocs/uploads/" +packageName+ "/"

        with open(path + fileName, "wb") as file:
            file.write(fileContent)

    crystal.convert(packageName)

    with tarfile.open("downloads/" +packageName+ "/" +packageName+ ".tar", "w") as tar:
        parameters = "downloads/" +packageName+ "/parameters.properties"
        drop_down = "downloads/" +packageName+ "/drop_down.properties"

        tar.add(parameters, arcname="parameters.properties")
        tar.add(drop_down, arcname="drop_down.properties")

        db2 = tarfile.TarInfo("db2")
        db2.type = tarfile.DIRTYPE
        tar.addfile(db2)

    print("* created .tar package <br /><br />")
    print("<b>Your download is ready: </b>")

    href = "downloads/" +packageName+ "/" +packageName+ ".tar"
    print("<h3><a href='" +href+ "' download> " +packageName+ ".tar </a></h3>")
