# -*- coding: utf-8 -*-

import MySQLdb

# ユーザリストを取得する
def initializeUserList(count=29):
	user_list=[]
	for p1 in get_hot()[1:count]:
		for p2 in get_urlposts(p1['url']):
			user = p2['user']
			user_list.append(user)
	return user_list
	

# 記事、タグ、タグ付けをDBに追加する
def fillTables(user_list):
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')
	
	for user in user_list[100:200]:
	
		for item in get_userposts(user)[28:31]:
			url = item['url']
			# insert entry
			sql = "INSERT IGNORE INTO entry(url) VALUES(%s);"
			r = cur.execute(sql, url)
			# すでに登録されている記事は無視する
			if r == 0: break
			# 記事のIDを取得する
			cur.execute("select id from entry where url=%s;", url)
			e_id = cur.fetchone()[0]
			# e_id = cur.rowcount
			
			for tag in get_itemtags(url):
				# insert tag
				sql = "INSERT IGNORE INTO tag(name) VALUES(%s);"
				cur.execute(sql, tag)
				# タグのIDを取得する
				cur.execute("select id from tag where name=%s;", tag)
				t_id = cur.fetchone()[0]
				# insert entry_tags（タグ付けする）
				cur.execute("INSERT IGNORE INTO entry_tags(e_id, t_id) VALUES(%d, %d);" % (e_id, t_id))
				
	con.commit()
	cur.close()
	con.close()
	return


# タグの共起回数（ふたつのタグが記事をいくつ共有しているか）
def calc_sim():
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# 記事の数を取得する
	cur.execute("SELECT count(id) from entry;")
	entry_num = cur.fetchone()[0]
	# タグの数を取得する
	cur.execute("SELECT count(id) from tag;")
	tag_num = cur.fetchone()[0]

	# タグxとyに共通する記事を数える
	get_sim = '''SELECT count(z.set_entry) FROM
	  (SELECT x.t_id AS "tag1", y.t_id  AS "tag2", x.e_id  AS "set_entry"
	    FROM
	      (SELECT * from entry_tags where t_id=%d) AS x,
	      (SELECT * from entry_tags where t_id=%d) AS y
	    WHERE x.e_id = y.e_id) AS z;'''

	# すべてのタグの組み合わせを計算する
	cur.execute("SELECT id FROM tag ORDER BY id;")
	tag1 = tag2 = cur.fetchall()
	# 二次元の表の三角に切った半分側を計算する感じ n(n-1)/2
	n = 0
	for t1 in tag1:
		n = t1[0] + 1
		if t1[0]%1000 == 0: print "+1000 done"
		for t2 in tag2[n:]:
			cur.execute(get_sim % (t1[0], t2[0]))
			sim = cur.fetchone()[0]
			cur.execute("INSERT IGNORE INTO tags_sim(sim, t_id1, t_id2) ¥
					VALUES(%d, %d, %d);" % (sim, t1[0], t2[0]))
			# 値を更新するように修正

	con.commit()
	cur.close()
	con.close()
	return
