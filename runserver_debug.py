from pypass import app

app.debug = True
app.secret_key = 'keepthisverysecret'
app.run(host='0.0.0.0', port=5000)
