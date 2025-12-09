import mysql.connector
import yaml
import asyncio

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

async def find_reg(tg_id):
	tg_id = tg_id
	tablename = 'users'
	database = config['authbot']['db']['reg_database']
	cnx = mysql.connector.connect(user=config['authbot']['db']['reg_username'], password=config['authbot']['db']['reg_password'], host=config['authbot']['db']['reg_host'], database=config['authbot']['db']['reg_database'], autocommit=True )
	mycursor = cnx.cursor()
	sql = f"SELECT EXISTS (SELECT 1 FROM {tablename} WHERE {tg_id});"
	mycursor.execute(sql)
	responce = mycursor.fetchall()[0][0]
	mycursor.close()
	cnx.close()
	return responce

async def register(tg_id, pnum, nickname, name, gender, birthday):
	tg_id, pnum, nickname, name, gender, birthday = tg_id, pnum, nickname, name, gender, birthday
	tablename = 'users'
	database = config['authbot']['db']['reg_database']
	cnx = mysql.connector.connect(user=config['authbot']['db']['reg_username'], password=config['authbot']['db']['reg_password'], host=config['authbot']['db']['reg_host'], database=config['authbot']['db']['reg_database'], autocommit=True )
	mycursor = cnx.cursor()
	sql = f"INSERT INTO 'users'('tg_id', 'pnum', 'nickname', 'name', 'gender', 'birthday') VALUES ({tg_id}, {pnum}, {nickname}, {name}, {gender}, {birthday});"
	mycursor.execute(sql)
	mycursor.close()
	cnx.close()