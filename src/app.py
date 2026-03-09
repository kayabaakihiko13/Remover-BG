from flask import Flask

app = Flask(__name__,template_folder="template")

if __name__ =="__main__":
    app.run(port=5000,debug=True)