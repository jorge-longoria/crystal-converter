#!C:/Users/jorge/AppData/Local/Programs/Python/Python36/python.exe
import cgi
import tarfile

print("Content-Type: text/html\n")

print("""
<form method="post" enctype="multipart/form-data">
 <div>
   <label for="file">Choose file to upload</label>
   <input type="file" id="file" name="file" multiple>
 </div>
 <div>
   <button>Submit</button>
 </div>
</form>
""")

formData = cgi.FieldStorage()

if "file" in formData:
    fileContent = formData["file"].value

    with open("C:/Apache24/htdocs/parameters.properties", "wb") as file:
        file.write(fileContent)

    with tarfile.open("package.tar", "w") as tar:
        tar.add("parameters.properties")

        db2 = tarfile.TarInfo("db2")
        db2.type = tarfile.DIRTYPE
        tar.addfile(db2)

    print("<a href='/package.tar' download> Get file </a>")
