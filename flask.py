
from flask import Flask, request

from processing import do_calculation

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        if 'eng' in request.form:
            result = do_calculation(request.form["flightnumber"].upper(),"e")
        else:
            result = do_calculation(request.form["flightnumber_chi"].upper(),"c")
        return '''
                <html>
                    <body>
                        <p>{result}</p>
                        <p><a href="/">Back/返回</a>
                    </body>
                </html>
             '''.format(result=result)

    return '''
        <html>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <body>
                {errors}
                <img src="/img/stayhomesavelives.jpg" style="width:100%;">
                <font size="4">

                <p>Together, we fight.<br><br>
                If you are in concern of recent flights taken back to Hong Kong, check your flight (eg CX851/BA27) below.<br><br>
                It provides 14 days data about the corona status of your flight.  </p>
                <form id="english" method="post" action=".">
                    <p><input type="text" name="flightnumber" maxlength="5" size="40" required="required">
                    <p><input type="submit" name="eng" value="Submit"  /></p>
                </form>

                <p>閣下可查詢14日內回港航班確診情況。請輸入航班編號，例如 CX851/BA27<br>
                <form id="chinese" method="post" action=".">
                    <p><input type="text" name="flightnumber_chi" maxlength="5" size="40" required="required">
                    <p><input type="submit" name="chi" value="提交"  /></p>
                </form>

                </font>
            </body>
        </html>
    '''.format(errors=errors)