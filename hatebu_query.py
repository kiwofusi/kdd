# -*- coding: utf-8 -*-

import MySQLdb
	
# �^�O����������
# �����R�[�h����₱�����B�ӂ��̕������ǂݍ���Ń��j�R�[�h�ɕϊ�����B
def search_tags(word):
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# ���Ԉ�v
	# �R�}���h�v�����v�g�p�ɁH�����R�[�h�ϊ�
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


# ����^�O�ɋ߂��^�O��\������i���O���́j
def sim_tags(name):
	# name����ID����肷��
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# ���S��v
	# �R�}���h�v�����v�g�p�ɁH�����R�[�h�ϊ�
	name = unicode(name, "cp932")
	sql = 'select id,name from tag where name LIKE %s;'
	cur.execute(sql, name);
	result = cur.fetchone()
	if result == 0: return
	
	# sim_tags_by_id(t_id)�ɓn���ĕ\������
	sim_tags_by_id(result[0])
	
	con.commit()
	cur.close()
	con.close()
	# return result


# ����^�O�ɋ߂��^�O��\������iID���́j
def sim_tags_by_id(t_id):
	con = MySQLdb.connect(db="db",
		host="localhost", user="user", passwd="passwd", charset="utf8")
	cur = con.cursor()
	cur.execute('SET NAMES utf8')

	# ���N�G�X�g���`�F�b�N����
	sql = "select name from tag where id=%d"
	cur.execute(sql % t_id)
	result = cur.fetchone()
	# �^�O�����݂��Ȃ��ꍇ�͏I��
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


# ���N�x�����L���O��\������
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
