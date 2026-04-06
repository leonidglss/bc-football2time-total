import sqlite3


# --------- basket.db---------------------------------------
# id, user_id, nickname, role, date_regist
class Database:
    def __init__(self, db_file):
        self.connection=sqlite3.connect(db_file)
        self.cursor=self.connection.cursor()

# id, user_id, nick, role, date_regist, is_online, lang, is_ban
# --------- Добавление юзера -------------------------------
    def add_user(self,user_id, name, role, to_day):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `nick`, `role`, `date_register`) VALUES (?, ?, ?, ?)", (user_id, name, role, to_day))
# --------- Проверка юзера на существование -----------------
    def user_exists(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
# --------- Получение всех юзеров -----------------
    def get_users(self):
        rr=[]
        with self.connection:
            result=self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()
            for res in result:
                rr.append(res[0])
            return rr
# --------- Получение юзеров с is_online = 1 -----------------
    def users_is_online(self):
        rr=[]
        with self.connection:
            result=self.cursor.execute("SELECT `user_id` FROM `users` WHERE `is_online` != 0").fetchall()
            for res in result:
                rr.append(res[0])
            return rr
# --------- Добавление юзеру is_online -----------------------
    def set_is_online(self,user_id, is_online):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `is_online` = ? WHERE `user_id` = ?", (is_online, user_id) )
# --------- Установка всем юзерам is_play=0 -----------------------
    def reset_is_online(self):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `is_online` = 0 ")
# --------- Добавление юзеру lang -----------------------
    def set_lang(self,user_id, lang):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `lang` = ? WHERE `user_id` = ?", (lang, user_id) )
# --------- Получение у юзера lang -----------------------
    def get_lang(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `lang` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0]
# --------- Добавление юзеру is_ban -----------------------
    def set_is_ban(self,user_id, is_ban):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `is_ban` = ? WHERE `user_id` = ?", (is_ban, user_id) )
# --------- Получение у юзера is_ban -----------------------
    def get_is_ban(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `is_ban` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0]
# --------- Добавление юзеру nick -----------------------
    def set_nickname(self,user_id, nick):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nick` = ? WHERE `user_id` = ?", (nick, user_id) )
# --------- Получение у юзера nick -----------------------
    def get_nickname(self,user_id):
        with self.connection:
            result=self.cursor.execute("SELECT `nick` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return result[0]

# id_game,id_ch,name_ch,time_rec_str,time_rec_ts,time_begin_str,time_begin_ts,maximum,team_1,team_2,P1,P2,FF,F1,F2,TT,TB,TM
# --------- Добавление ставки -------------------------------
    def save_bet_in_db(self,id_game,id_ch,name_ch,time_rec_str,time_rec_ts,time_begin_str,time_begin_ts,maximum,team_1,team_2,P1,X,P2,FF,F1,F2,TT,TB,TM):
        if self.game_exists(id_game)==False:
            with self.connection:
                return self.cursor.execute("INSERT INTO `bets_morning` (`id_game`, `id_ch`, `name_ch`, `time_rec_str`, `time_rec_ts`, `time_begin_str`, `time_begin_ts`, `maximum`, `team_1`, `team_2`, `P1`, `X`, `P2`, `FF`, `F1`, `F2`, `TT`, `TB`, `TM`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id_game,id_ch,name_ch,time_rec_str,time_rec_ts,time_begin_str,time_begin_ts,maximum,team_1,team_2,P1,X,P2,FF,F1,F2,TT,TB,TM))
        else:
            return
# --------- Проверка игры на существование в бд ---------------------------
    def game_exists(self,id_game):
        with self.connection:
            result=self.cursor.execute("SELECT * FROM `bets_morning` WHERE `id_game` = ?", (id_game,)).fetchall()
            return bool(len(result))
# --------- Удаление ставки из бд по времени -------------------------------
    def delete_game_by_time(self, to_day_ts):
        with self.connection:
            return self.cursor.execute("DELETE FROM `bets_morning` WHERE `time_begin_ts` < ?", (to_day_ts - 3*60*60,))
# --------- Удаление ставки из бд по id_game -------------------------------
    def delete_game_by_id(self, id_game):
        with self.connection:
            return self.cursor.execute("DELETE FROM `my_bets` WHERE `id_game` = ?", (id_game,))
# --------- Удаление всех моих ставок из бд --------------------------------------
    def delete_games(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM `my_bets` ")
# --------- Получение массива всех ставок -----------------------------------
    def get_all_bets(self):
        with self.connection:
            result=self.cursor.execute("SELECT * FROM `bets_morning` ").fetchall()
            return result
# --------- Получение массива всех моих ставок -----------------------------------
    def get_all_my_bets(self):
        with self.connection:
            result=self.cursor.execute("SELECT * FROM `my_bets` ").fetchall()
            return result

# --------- Получение массива номеров всех ставок ----------------------------
    def get_num_bets(self):
        with self.connection:
            result=self.cursor.execute("SELECT id_game FROM `bets_morning` ").fetchall()
            return result
# --------- Получение текущих голов ----------------------------
    def get_score(self,id_game):
        with self.connection:
            result=self.cursor.execute("SELECT score_tec FROM `bets_morning` WHERE `id_game` = ?", (id_game,)).fetchone()
            return result[0]
# --------- Запись текущих голов ----------------------------
    def set_score(self,id_game,score_tec):
        with self.connection:
            result=self.cursor.execute("UPDATE `bets_morning` SET score_tec=(?) WHERE `id_game` = ?", [score_tec,id_game])
            return result
# --------- Получение массива номеров чемпа ставки ----------------------------
    def get_ch_bet(self,id_game):
        with self.connection:
            result=self.cursor.execute("SELECT id_ch FROM `bets_morning` WHERE `id_game` = ?", (id_game,)).fetchone()
            return result
# --------- Получение массива номеров моих ставок ----------------------------
    def get_num_mybets(self):
        with self.connection:
            result=self.cursor.execute("SELECT id_game FROM `my_bets` ").fetchall()
            return result
# --------- Получение массива чемпов моих ставок ----------------------
    def get_mybets_ch(self):
        with self.connection:
            result=self.cursor.execute("SELECT id_ch FROM `my_bets` ").fetchall()
            return result
# --------- Получение массива времени начала матча  ----------------------------
    def get_times_begin(self):
        with self.connection:
            result=self.cursor.execute("SELECT time_begin_ts FROM `bets_morning`").fetchall()
            return result
# --------- Получение ставки по ее номеру -----------------------
    def get_bet(self,id_game):
        with self.connection:
            result=self.cursor.execute("SELECT * FROM `bets_morning` WHERE `id_game` = ?", (id_game,)).fetchone()
            return result
# --------- Получение результата ставки по ее номеру -----------------------
    def update_res(self, id_game,score):
        with self.connection:
            return self.cursor.execute(""" UPDATE my_bets SET res_game=(?) WHERE id_game=(?) """, [score,id_game])
        # with self.connect:
        #     return self.cursor.execute("UPDATE my_bets SET res_game=(?) WHERE id_game=(?)", (score,id_game))

# id_game,id_ch,name_ch,time_begin_str,team_1,team_2,P1,P2,FF,F1,F2,TT,TB,TM,bet,score,score_ext,bet_res
# --------- Добавление в мои ставки -------------------------------
    def save_my_bet(self,id_game,id_ch,name_ch,time_begin_str,team_1,team_2,bet,koef):
        if self.game_exists_in_myDb(id_game, bet)==False:
            with self.connection:
                return self.cursor.execute("INSERT INTO `my_bets` (`id_game`, `id_ch`, `name_ch`, `time_begin_str`, `team_1`, `team_2`, `bet`, `koef`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id_game,id_ch,name_ch,time_begin_str,team_1,team_2,bet,koef))
        else:
            return
        
    def game_exists_in_myDb(self,id_game,bet):
        with self.connection:
            result=self.cursor.execute("SELECT * FROM `my_bets` WHERE `id_game` = ? AND `bet` = ?", (id_game,bet)).fetchall()
            return bool(len(result))

# num=12998311
# db=Database('basket.db')
# dbgame=db.get_bet(num)
# print(dbgame)