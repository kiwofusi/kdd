# -*- coding: utf-8 -*-

"""
from start import *

で読み込み


# クロール
hateusers = initializeUserList()
fillTables(hateusers)

# 計算
cluc_sim()

# テーブル設計
CREATE TABLE entry(
  id INT PRIMARY KEY AUTO_INCREMENT,
  url VARCHAR(255) UNIQUE,
  title VARCHAR(255)
);

CREATE TABLE tag(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) UNIQUE,
  frequency INT
);

CREATE TABLE entry_tags(
  id INT PRIMARY KEY AUTO_INCREMENT,
  e_id INT,
  t_id INT,
  UNIQUE(e_id, t_id),
  FOREIGN KEY(e_id) REFERENCES entry(id),
  FOREIGN KEY(t_id) REFERENCES tag(id)
);

CREATE TABLE tags_sim(
  id INT PRIMARY KEY AUTO_INCREMENT,
  sim FLOAT,
  t_id1 INT,
  t_id2 INT,
  weight INT,
  UNIQUE(t_id1, t_id2),
  FOREIGN KEY(t_id1) REFERENCES tag(id),
  FOREIGN KEY(t_id2) REFERENCES tag(id)
);

"""

from hatebu_rec import *
from hatebu_db import *
from hatebu_query import *

