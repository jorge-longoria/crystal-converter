#!C:/Users/jorge/AppData/Local/Programs/Python/Python36/python.exe
import cgi
import os
import shutil
import tarfile
import crystal

formData = cgi.FieldStorage()

#Used in form validation warning.
if "userfile" in formData and not isinstance(formData["userfile"], list):
    visibility = "visible"
else:
    visibility = "hidden"

if "package" in formData:
    packageName = formData["package"].value


print("Content-Type: text/html; charset=utf-8\n")

print("""
<link rel="stylesheet" type="text/css" href="style.css">

<div class="wrapper">
 <div class="title">
     Crystal Converter
 </div>
 <div class="superscript">
     <sup title="1) Enter package name\n2) Upload clean.sql and profile.sql\n3) Download .properties files.">
        <a href="/about.html">What's this?</a>
     </sup>
 </div>
</div>

<div class="form">
 <div class="bodytext">
 <form method="post" enctype="multipart/form-data">
     <div>
        <label for="package">Report package name:</label> <br />
        <input class="input" type="text" id="package" name="package" required autofocus>
     </div>
     <br />
     <div>
       <label for="file">Choose files to upload:</label> <br />
       <input class="input subtext" type="file" id="userfile" name="userfile" required multiple>
       <div class='warning' """+visibility+""">*** Please upload both clean.sql and profile.sql. ***</div>
     </div>
     <br />
     <div>
       <button class="submit">Submit</button>
     </div>
 </form>
 </div>
</div>
""")

if "userfile" in formData and isinstance(formData["userfile"], list):
    for directory in ["uploads", "downloads"]:
        dir = directory +"/"+ packageName
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

    for resource in formData["userfile"]:
        fileName = resource.filename
        fileContent = resource.value

        path = "C:/Apache24/htdocs/uploads/" +packageName+ "/"

        with open(path + fileName, "wb") as file:
            file.write(fileContent)

    crystal.convert(packageName)

    packageTar = "downloads/" +packageName+ "/" +packageName+ ".tar"

    with tarfile.open(packageTar, "w") as tar:
        for config in ["report", "parameters", "drop_down"]:
            filepath = "downloads/" +packageName+ "/" +config+ ".properties"
            tar.add(filepath, arcname=str(config + ".properties"))

        for db in ["db2", "mssql", "oracle"]:
            directory = tarfile.TarInfo(db)
            directory.type = tarfile.DIRTYPE
            tar.addfile(directory)

    print("<div class='success'>Your download is ready: </div>")
    print("<div class='success'><a href='" +packageTar+ "' download> " +packageName+ ".tar </a></div>")
else:
    pass
