# BOT_NAME='WtsHockeyTotal'
# BOT_ADRES='t.me/WtsHockeyTotalBot'
# BOT_TOKEN_HOCKEY='6122803732:AAF-o-g36cVXcjQ0rLqR1JaGo9zKxsBrtfA'
# BOT_TOKEN_FOOTBALL='5631889291:AAHZMPrvwFXZHcIzUje9uBIK3LyjX0SdnUc'
# BOT_TOKEN_BASKETBALL='6064784068:AAHhRMovJiF9WlBj2u4Trhc9gVP7xodAuIs'
# ------------------------------------------
BOT_NAME_FOOTBALL_WIN='Football bets on favorite'
BOT_ADRES_FOOTBALL_WIN='t.me/WtsFootballWinnerBot'
WTS_TOKEN_FOOTBALL_WIN='6402451866:AAFee2Pg_ZmC6GKc_pgf2RobFMwyr2ou5ds'
wts_api_id: int = 20591732
wts_api_hash: str = '19e456bf61c91fd26a29c4ee2b7f2eaa'

vim="""
root@WtsBetcityBots:/etc/systemd/system# systemctl enable MyFoots.service
root@WtsBetcityBots:/etc/systemd/system# systemctl start MyFoots.service
root@WtsBetcityBots:/etc/systemd/system# systemctl stop MyFoots.service

root@WtsBetcityBots:/etc/systemd/system# systemctl enable mainPyro.service
root@WtsBetcityBots:/etc/systemd/system# systemctl start mainPyro.service
root@WtsBetcityBots:/etc/systemd/system# systemctl stop mainPyro.service

# - MyFoots.service
[Service]
WorkingDirectory=/root/bc_football_win/
User=root
ExecStart=/usr/bin/python3 MyFoots.py

[Install]
WantedBy=multi-user.target

# - mainPyro.service
[Service]
WorkingDirectory=/root/bc_football_win/
User=root
ExecStart=/usr/bin/python3 mainPyro.py

[Install]
WantedBy=multi-user.target
EOF

"""