#!C:/Users/jorge/AppData/Local/Programs/Python/Python36/python.exe
import cgi
import os
import shutil
import tarfile
import crystal

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

<form method="post" enctype="multipart/form-data">
<div class="form">
 <div class="bodytext">
     <div>
        <label for="package">Report package name:</label> <br />
        <input class="input" type="text" id="package" name="package" required autofocus>
     </div>
     <br />
     <div>
       <label for="file">Choose files to upload:</label> <br />
       <input class="input subtext" type="file" id="userfile" name="userfile" required multiple>
     </div>
     <br /><br /><br />
     <div>
       <button class="submit">Submit</button>
     </div>
 </div>
</div>
</form>
""")

formData = cgi.FieldStorage()

if "package" in formData:
    packageName = formData["package"].value

if "userfile" in formData and isinstance(formData["userfile"], list):
    if os.path.exists("uploads/" + packageName):
        shutil.rmtree("uploads/" + packageName)

    if os.path.exists("downloads/" + packageName):
        shutil.rmtree("downloads/" + packageName)

    os.makedirs("uploads/" + packageName)
    os.makedirs("downloads/" + packageName)

    for resource in formData["userfile"]:
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
    print("<h2><a href='" +href+ "' download> " +packageName+ ".tar </a></h2>")
elif "userfile" in formData:
    print("<div class='warning'>*** Please upload both clean.sql and profile.sql. ***</div>")
else:
    pass
