from .all_texts import router_all_text
from .check import router_check
from .content_watch import router_content_watch
from .eldo import router_eldo
from .free_texts import router_free_texts
from .get_ids import router_get_ids
from .history import router_history
from .mvideo import router_mvideo
from .receipt import router_receipt
from .start import router_start
from .turgenev_check import router_turgenev
from .unique import router_unique
from .vacation import router_vacation
from .echo import router_echo

routers = [
    router_all_text,
    router_check,
    router_content_watch,
    router_eldo,
    router_free_texts,
    router_get_ids,
    router_history,
    router_mvideo,
    router_receipt,
    router_start,
    router_turgenev,
    router_unique,
    router_vacation,
    router_echo,
]
