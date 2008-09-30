# -*- coding: utf-8 -*-

import MySQLdb
	
# タグを検索する
# 文字コードがややこしい。ふつうの文字列を読み込んでユニコードに変換する。
def search_tags(word):
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# 中間一致
	# コマンドプロンプト用に？文字コード変換
	word = unicode("%" + word + "%", "cp932")
	sql = 'select id,name from tag where name LIKE %s;'
	cur.execute(sql, word);
	result = cur.fetchall()

	print "----------------------------------------"
	print "%7s | tag" % "id"
	print "----------------------------------------"
	for tag in result:
		print "%7d | %s" % (tag[0], tag[1])

	con.commit()
	cur.close()
	con.close()
	# return result


# あるタグに近いタグを表示する（名前入力）
def sim_tags(name):
	# nameからIDを特定する
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# 完全一致
	# コマンドプロンプト用に？文字コード変換
	name = unicode(name, "cp932")
	sql = 'select id,name from tag where name LIKE %s;'
	cur.execute(sql, name);
	result = cur.fetchone()
	if result == 0: return
	
	# sim_tags_by_id(t_id)に渡して表示する
	sim_tags_by_id(result[0])
	
	con.commit()
	cur.close()
	con.close()
	# return result


# あるタグに近いタグを表示する（ID入力）
def sim_tags_by_id(t_id):
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# リクエストをチェックする
	sql = "select name from tag where id=%d"
	cur.execute(sql % t_id)
	result = cur.fetchone()
	# タグが存在しない場合は終了
	if result == 0: return
	print "id:%d | %s" % (t_id, result[0])
	print "----------------------------------------"

	sql = '''select tags_sim.id, sim, t_id2, name
		  from tags_sim INNER JOIN tag ON tags_sim.t_id2 = tag.id
		  where sim>=1 AND tags_sim.t_id1=%d
		    ORDER BY sim DESC limit 15;'''
	cur.execute(sql % t_id)
	result = cur.fetchall()

	print"%4s | %7s | sim_tag" % ("sim", "tag_id")
	print "----------------------------------------"
	for tag in result:
		print "%4d | %7d | %s" % (tag[1], tag[2], tag[3])

	con.commit()
	cur.close()
	con.close()
	# return result


# 共起度ランキングを表示する
def sim_list(low=30,high=200,sort="DESC"):
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	sql = "select id,sim,t_id1,t_id2 from tags_sim \
		where sim>%d AND sim<%d ORDER BY sim %s limit 100;"
	cur.execute(sql % (low,high,sort))
	result = cur.fetchall()

	print "----------------------------------------"
	print"%3s | %5s | %5s | %15s | %15s" \
			% ("sim", "tag1", "tag2", "tag1_name", "tag2_name")
	print "----------------------------------------"
	for sim in result:
		sql = "select name from tag where id=%d;"
		cur.execute(sql % sim[2])
		tag1_name = cur.fetchone()[0]
		cur.execute(sql % sim[3])
		tag2_name = cur.fetchone()[0]
		print "%3d | %5d | %5d | %13s | %13s" \
			% (sim[1], sim[2], sim[3], tag1_name, tag2_name)

	con.commit()
	cur.close()
	con.close()
