from .authors import router_authors
from .all_texts import router_all_texts
from .deadlines import router_deadlines
from .free_authors import router_free_authors
from .free_texts import router_free_texts
from .history import router_history
from .money import router_money
from .new_author import router_new_author
from .start import router_start
from .stats_month import router_stats_month
from .echo import router_echo


routers = [
    router_authors,
    router_all_texts,
    router_deadlines,
    router_free_authors,
    router_free_texts,
    router_history,
    router_money,
    router_new_author,
    router_start,
    router_stats_month,
    router_echo,
]
