from apps.api.modules.user import User
from apps.api.modules import recommendation as mod_rcmd

from apps.api.modules.travel import Travel, TravelGroup

haruki = User(email="haruki@hojohigh.edu.jp",
              pswd_hash="1ABE6B9D0EB94B39AFFF662292ACE2A7")
kazusa = User(email="kazusa@hojohigh.edu.jp",
              pswd_hash="18947B8CA05107CC128F5587D1BAC943")
setsuna = User(email="setsuna@hojohigh.edu.jp",
              pswd_hash="B784489EA12B0792D7E92C0FBA3F1B22")

mod_rcmd.recommend_friend_list(setsuna)

tg_46=TravelGroup(14,46)
t_56=Travel(14,56)

mod_rcmd.recommend_city_list_by_travel(kazusa,56)

mod_rcmd.recommend_city_list_by_travel_group(kazusa,46)

u9 = User(email="y@y.edu",
              pswd_hash="415290769594460E2E485922904F345D")