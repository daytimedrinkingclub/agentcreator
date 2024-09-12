from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key in production

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    flash('Error: Division by zero is not allowed', 'error')
                else:
                    result = num1 / num2
            else:
                flash('Error: Invalid operation', 'error')

        except ValueError:
            flash('Error: Please enter valid numbers', 'error')

    return render_template('calculator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')