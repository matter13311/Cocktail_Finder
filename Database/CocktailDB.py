#12.42.205.8

from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import pymysql


app = Flask(__name__)
app.config['MYSQL_HOST'] ='35.184.2.237'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='Database435'
app.config['MYSQL_DB'] ='Recipes'

mysql = MySQL(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='POST':
        #fetch form data
        userDetails = request.form.getlist('name[]')  #stores form data in var called userDetails
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT distinct UserID FROM UserIngredients") #shows all id's in table
        idDetails = cursor.fetchall()
        counter = 1;
        for j in idDetails:
            counter = counter + 1
        for i in userDetails:
            cursor.execute("INSERT INTO UserIngredients(UserID,Ingredient) VALUES(%s, %s)", (counter, i))

        sqlstatement = "select distinct CocktailName.RecipeName, Spirits.SpiritName, Spirits.SpiritAmount,Syrups.SyrupName,Syrups.SyrupAmount,Juices.JuiceName, Juices.JuiceAmount, Fruits.FruitName,Fruits.FruitAmount from CocktailName join Spirits join Syrups join Juices join Fruits join UserIngredients on Spirits.SpiritName like UserIngredients.Ingredient and Spirits.RecipeID = CocktailName.RecipeID or Syrups.SyrupName like UserIngredients.Ingredient and Syrups.RecipeID = CocktailName.RecipeID or Juices.JuiceName like UserIngredients.Ingredient and Fruits.RecipeID = CocktailName.RecipeID or Fruits.FruitName like UserIngredients.Ingredient and Fruits.RecipeID = CocktailName.RecipeID where UserIngredients.UserID = 1;"
        #sqlstatement = "select distinct r1.RecipeName,r1.Spirit,r1.SpiritAmount,r1.Syrup,r1.SyrupAmount,r1.Juice,r1.JuiceAmount,r1.Fruit,r1.FruitAmount from Ingredients r1 join UserIngredients u1 on r1.Spirit like u1.Ingredient or r1.Syrup like u1.Ingredient or r1.Juice like u1.Ingredient or r1.Fruit like u1.Ingredient WHERE UserID = %s;"

        adr = (str(counter), )
        cursor.execute(sqlstatement)
        #cursor.execute(sqlstatement, adr)
        queryResults = cursor.fetchall()

        deleteStatement = "DELETE FROM UserIngredients WHERE UserID = %s;"
        cursor.execute(deleteStatement, adr)
        mysql.connection.commit()
        cursor.close()

        return render_template('displayResults.html', queryResults=queryResults, counter=counter)
        #return render_template('cocktails.html', idDetails=idDetails)
        #return render_template('displayList.html', your_list=userDetails)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
